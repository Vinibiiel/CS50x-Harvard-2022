#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <cs50.h>

const int BLOCK_SIZE = 512;
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }
    BYTE buffer[BLOCK_SIZE];
    FILE *file = fopen(argv[1], "r");
    if (file == NULL){
        return 2;
    }
    FILE *output = NULL;
    char filename[8];
    int count = 0;
    while(fread(buffer, 1, BLOCK_SIZE, file) == BLOCK_SIZE){
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
        (buffer[3] & 0xf0) == 0xe0){
            if(count!=0){
                fclose(output);
            }
            sprintf(filename,"%03i.jpg",count);
            output = fopen(filename, "w");
            count++;
        }
        if(count!=0){
            fwrite(&buffer,1,BLOCK_SIZE,output);
        }
    }
    fclose(output);
    fclose(file);

    return 0;

}