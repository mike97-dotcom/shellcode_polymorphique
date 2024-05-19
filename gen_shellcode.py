import os
import random
import subprocess

def read_asm_code():
    #Liste d'instructions assembleur pour mettre les registres à zéro
    random_code = [
        '\txor rcx, rcx\n', # Met le registre RCX à zéro
        '\txor rax, rax\n', # Met le registre RAX à zéro
        '\txor rbx, rbx\n', # Met le registre RBX à zéro
        '\txor rsi, rsi\n', # Met le registre RSI à zéro
        '\txor rdi, rdi\n', # Met le registre RDI à zéro
        '\txor rdx, rdx\n'  # Met le registre RDX à zéro
    
    ]

    #Mélanger les instructions pour qu'elles soient dans un ordre aléatoire
    random.shuffle(random_code)

    #Ouvrir le fichier 'shellcode.asm' en mode lecture et écriture
    with open('shellcode.asm', 'r+') as file:
        #Lire et ignorer les trois premières lignes du fichier
        for _ in range(3):
            file.readline()

        # Obtenir la position actuelle dans le fichier après les trois premières lignes
        position = file.tell()

        # Revenir à cette position pour insérer le code aléatoire
        file.seek(position)

        #Écrire les instructions aléatoires dans le fichier
        for code in random_code:
         file.write(code)
        file.seek(0)
        content = file.readlines()

    #Utiliser NASM et ld  pour assembler le fichier assembleur en un fichier objet puis en executable 
    subprocess.run(["nasm", "-f", "elf64", "shellcode.asm", "-o", "shellcode.o"])
    subprocess.run(["ld", "shellcode.o", "-o", "shellcode"])
    objdump_output = subprocess.run(
        "objdump -d shellcode| grep '^ ' | cut -f2 | awk '{for(i=1;i<=NF;i++) printf \"\\\\x%s\",$i} END {print\"\"}'",
        shell=True, capture_output=True, text=True
    ).stdout

    #calculer la longueur du shellcode (chaque séquence \xHH fait 4 caractères)
    shellcode_length = len(objdump_output) // 4 

    # Retourner le shellcode et sa longueur
    return objdump_output

#Appeler la fonction pour obtenir le shellcode et sa longueur et les afficher
shellcode, shellcode_length = read_asm_code()
print(f"shellcode: {shellcode}")
print(f"taille du shellcode: {shellcode_length}")