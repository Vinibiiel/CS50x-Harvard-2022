#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    if (argc != 2) {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    for (int a = 0;a<strlen(argv[1]);a++){
        if(!isdigit(argv[1][a])){
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    int cripto_key = atoi(argv[1]);
    string plain_text = get_string("plaintext:  ");

    printf("ciphertext:  ");
    for (int i = 0;i<strlen(plain_text);i++){
        if (plain_text[i]<97 && plain_text[i] >= 65){ // quer dizer que a letra é maiuscula
            int Pi = plain_text[i] - 64;
            // Transformando a letra para inteiro
            int Ci = ((Pi + cripto_key) % 26) + 64;
            printf("%c",Ci);
        }else if(plain_text[i]>=97 && plain_text[i]<=122){ // quer dizer que a letra é maiuscula
            int Pi = plain_text[i] - 96;
            // Transformando a letra para inteiro
            int Ci = ((Pi + cripto_key) % 26) + 96;
            printf("%c",Ci);
        }else{
            printf("%c",plain_text[i]);
        }
    }
    printf("\n");
    return 0;
}