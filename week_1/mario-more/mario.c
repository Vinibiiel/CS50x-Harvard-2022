/*
  WEEK 1

  this version of Mario if feeling more comfortable.
  CODE MADE BY: Vinicius Gabriel
  Github: https://github.com/Vinibiiel
*/

#include <stdio.h>
#include <cs50.h>

int main(void) {
  int hashes,aux;
  printf("Height: ");
  scanf("%d",&hashes);
  // While verificador se o valor de hashes é aceitavel
  while(hashes <=0 || hashes > 8){
    printf("Height: ");
    scanf(""); // Limpeza de buffer, o \n do enter
    scanf("%d",&hashes);
  }
  // Variavel auxiliar usada a controlar o numero de linhas no for
  aux = hashes;
  for (int i = 1;i<=aux;i++){
      for (int j = hashes;j>1;j--){
          printf(" ");
      }
    hashes--;
    for(int k = hashes-i;k<hashes;k++){
      printf("#");
    }

    // Agora a parte do "espelho" dos #
    printf("  ");
    for(int k = hashes-i;k<hashes;k++){
      printf("#");
    }
    printf("\n");
  }
}