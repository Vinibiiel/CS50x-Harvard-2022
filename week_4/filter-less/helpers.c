#include "helpers.h"
#include <math.h>
#include <string.h>
#include <cs50.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0;i<height;i++){
        for(int j = 0;j<width;j++){
            float grayColor = round((image[i][j].rgbtBlue+image[i][j].rgbtRed+image[i][j].rgbtGreen)/3.00);
            // Primeiro pega o tom de cinza do pixel
            //Depois aplica
            image[i][j].rgbtBlue = grayColor;
            image[i][j].rgbtRed = grayColor;
            image[i][j].rgbtGreen = grayColor;
        }
    }
    return;
}

int limit(int RGB){
    if(RGB>255){
        RGB = 255;
    }
    return RGB;
}
// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
     for (int i = 0;i<height;i++){
        for(int j = 0;j<width;j++){
            float sepiaRed = (0.393*image[i][j].rgbtRed) + (0.769*image[i][j].rgbtGreen) + (0.189*image[i][j].rgbtBlue);
            float sepiaBlue = (0.272*image[i][j].rgbtRed) + (0.534*image[i][j].rgbtGreen )+ (0.131*image[i][j].rgbtBlue);
            float sepiaGreen = (0.349*image[i][j].rgbtRed) + (0.686*image[i][j].rgbtGreen) + (0.168*image[i][j].rgbtBlue);

            int colorRed = limit(round(sepiaRed));;
            int colorGreen = limit(round(sepiaGreen));
            int colorBlue = limit(round(sepiaBlue));
            image[i][j].rgbtBlue = colorBlue;
            image[i][j].rgbtRed = colorRed;
            image[i][j].rgbtGreen = colorGreen;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int auxiliar[3]; // Array que vai guardar o pixel temporariamente para trocar as linhas da imagem
     for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++) {

            auxiliar[0] = image[i][j].rgbtBlue;
            auxiliar[1] = image[i][j].rgbtGreen;
            auxiliar[2] = image[i][j].rgbtRed;

            image[i][j].rgbtBlue = image[i][width-j-1].rgbtBlue;
            image[i][j].rgbtGreen = image[i][width-j-1].rgbtGreen;
            image[i][j].rgbtRed = image[i][width-j-1].rgbtRed;

            image[i][width-j-1].rgbtBlue = auxiliar[0];
            image[i][width-j-1].rgbtGreen = auxiliar[1];
            image[i][width-j-1].rgbtRed = auxiliar[2];
        }
    }
    return;
}
int do_blur(int row,int column,int height,int width,RGBTRIPLE image[height][width],string color){

    float count = 0;
    int sum_of_colors = 0; // Soma as cores do pixel e depois subtrai pelo total, para ter o blur

    // Ou seja vai começar 1 linha antes do pixel, imagine um bloco 3x3, o primeiro está na diagonal superior esquerda, 1 linha antes, e 1 coluna antes
    int before_row = row-1;
    int before_column = column-1;
    for (int i = before_row; i < (row+2);i++)
    {
        for (int j = before_column; j < (column+2); j ++)
        {
            if((i < 0 || j < 0 || i >= height || j >= width))
            {
                continue;
            }
            if (strcmp(color,"red") == 0)
            {
                sum_of_colors += image[i][j].rgbtRed;
            }
            else if (strcmp(color,"green") == 0)
            {
                sum_of_colors += image[i][j].rgbtGreen;
            }
            else if(strcmp(color,"blue") == 0)
            {
                sum_of_colors += image[i][j].rgbtBlue;
            }
            else{
                return 0;
            }
            count++;
        }
    }
    return round(sum_of_colors/count);

}
// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Como aplicaremos um filtro pixel por pixel, necessitamos de uma imagem que não será mexida, para usar de espelho para o blur
    RGBTRIPLE copy_image[height][width];

    for (int row = 0; row < height; row++)
    {
        for (int column = 0; column < width; column++)
        {
            copy_image[row][column] = image[row][column];
        }
    }

    for (int row = 0; row < height; row++)
    {
        for (int column = 0; column < width; column++)
        {
            image[row][column].rgbtRed = do_blur(row, column, height, width, copy_image, "red");
            image[row][column].rgbtGreen = do_blur(row, column, height, width, copy_image, "green");
            image[row][column].rgbtBlue = do_blur(row, column, height, width, copy_image, "blue");
        }
    }
}

 // Essa função vai receber as informações necessarias e retornará o blur necessário a ser aplicado no pixel
// Para aplicar um efeito de blur é necessario aplicar uma mesclagem nos pixel em volta ao pixel selecionado, como se fosse um 3x3.
