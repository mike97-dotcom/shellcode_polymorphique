import os
import subprocess

# Paths to the files
asm_file = 'shellcode.asm'
c_file = 'test_gen-chiffré.c'
py_file = 'gen-chiffré.py'
compiled_file = 'shellcode'

# Step 1: Generate the shellcode using the ASM file and Python script
def generate_shellcode(asm_file, py_file):
    command = f"python3 {py_file} {asm_file}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    shellcode = process.stdout.read().decode('utf-8').strip()
    return shellcode

# Step 2: Insert the shellcode into the C file
def insert_shellcode_into_c(shellcode, c_file):
    with open(c_file, 'r') as file:
        c_code = file.read()

    # Replace the placeholder in the C code with the shellcode
    c_code = c_code.replace('<SHELLCODE_PLACEHOLDER>', shellcode)

    temp_c_file = 'temp.c'
    with open(temp_c_file, 'w') as file:
        file.write(c_code)
    
    return temp_c_file

# Step 3: Compile the C file
def compile_c_file(c_file, output_file):
    command = f"gcc {c_file} -o {output_file}"
    os.system(command)

# Generate the shellcode
shellcode = generate_shellcode(asm_file, py_file)
print(f"Generated Shellcode: {shellcode}")

# Insert the shellcode into the C file
temp_c_file = insert_shellcode_into_c(shellcode, c_file)
print(f"Shellcode inserted into C file: {temp_c_file}")

# Compile the C file
compile_c_file(temp_c_file, compiled_file)
print(f"Compiled executable created: {compiled_file}")

