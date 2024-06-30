import os
import random
import subprocess
import hashlib

def xor_encrypt(data, key):
    """Chiffre les données en utilisant l'algorithme XOR avec la clé donnée."""
    encrypted_data = bytearray()
    for i in range(len(data)):
        encrypted_data.append(data[i] ^ key[i % len(key)])
    return encrypted_data

def read_asm_code():
    # Liste d'instructions assembleur pour mettre les registres à zéro
    random_code = [
        '\txor rcx,rcx\n',
        '\txor rax,rax\n',
        '\txor rbx,rbx\n',
        '\txor rdi,rdi\n',
        '\txor rdx,rdx\n'
    ]

    # Mélanger les instructions pour qu'elles soient dans un ordre aléatoire
    number = random.randint(3,6)
    random.shuffle(random_code)
    selected_code = random_code[:number]

    # Ouvrir le fichier 'shellcodeT.asm' en mode lecture et écriture
    with open('shellcode.asm', 'r+') as file:
        # Lire et ignorer les trois premières lignes du fichier
       content = file.readlines()
        specific_xor = {'xor rax,rax', 'xor rbx,rbx', 'xor rcx,rcx', 'xor rdx,rdx', 'xor rdi,rdi'}
        content = [line for line in content if not any(line.strip() == xor for xor in specific_xor)]

        insert_pos = 3
        for code in selected_code:
            content.insert(insert_pos, code)
            insert_pos += 1
        file.seek(0)
        file.writelines(content)
        file.truncate()

    # Utiliser NASM et ld pour assembler le fichier assembleur en un fichier objet puis en exécutable
    subprocess.run(["nasm", "-f", "elf64", "shellcode.asm", "-o", "shellcode.o"])
    subprocess.run(["ld", "shellcode.o", "-o", "shellcodeT"])
    objdump_output = subprocess.run(
        "objdump -d shellcodeT | grep '^ ' | cut -f2 | awk '{for(i=1;i<=NF;i++) printf \"\\\\x%s\",$i} END {print\"\"}'",
        shell=True, capture_output=True, text=True
    ).stdout.strip()

    # Convertir le shellcode en bytes
    shellcode_bytes = bytes.fromhex(objdump_output.replace('\\x', ''))

    # Clé de chiffrement (vous pouvez choisir une clé plus sécurisée)
    encryption_key = b'secretkey'

    # Chiffrer le shellcode
    encrypted_shellcode = xor_encrypt(shellcode_bytes, encryption_key)

    # Convertir le shellcode chiffré en format d'affichage
    encrypted_shellcode_str = ''.join([f'\\x{byte:02x}' for byte in encrypted_shellcode])

    # Calculer la longueur du shellcode chiffré
    shellcode_length = len(encrypted_shellcode)

    # Calculer les hachages SHA-256 et MD5 du shellcode chiffré
    sha256_hash = hashlib.sha256(encrypted_shellcode).hexdigest()
    md5_hash = hashlib.md5(encrypted_shellcode).hexdigest()

    # Retourner le shellcode chiffré, sa longueur et les hachages
    return encrypted_shellcode_str, shellcode_length, sha256_hash, md5_hash

# Appeler la fonction pour obtenir le shellcode chiffré, sa longueur et les hachages, puis les afficher
shellcode, shellcode_length, sha256_hash, md5_hash = read_asm_code()
print(f"shellcode chiffré: {shellcode}")
print(f"taille du shellcode: {shellcode_length}")
print(f"SHA-256: {sha256_hash}")
print(f"MD5: {md5_hash}")
