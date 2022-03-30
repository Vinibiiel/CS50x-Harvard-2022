#include<cs50.h>
#include<stdio.h>
#include <string.h>
#include <ctype.h>
int count_letters(string text);
int count_words(string text);
int count_setences(string text);
int main() {
    string text = get_string("Text: ");
    double numb_of_letters = count_letters(text);
    double numb_of_words = count_words(text);
    double numb_of_sentences = count_setences(text);
    double average_numb_of_letter_per_words = numb_of_letters / numb_of_words*100;
    double average_numb_of_sentences = numb_of_sentences / numb_of_words*100;
    double index = (0.0588 * average_numb_of_letter_per_words) - (0.296 * average_numb_of_sentences) - 15.8;
    int grade = 0;
    grade = (int)(index < 0 ? (index- 0.5) : (index+ 0.5));

    if (grade < 1){
        printf("Before Grade 1\n");
    }else if(grade>16){
        printf("Grade 16+\n");
    }else{
        printf("Grade %d\n",grade);
    }
    return 0;
}
int count_letters(string text){
    int count = 0;
    for (int i= 0;i<strlen(text);i++){
        char letra = text[i];
        if (isalpha(letra)) {
            count++;
        }
    }
    return count;
}
int count_words(string text){
    int count_words = 1;
    for (int i= 0;i<strlen(text);i++){
        char letra = text[i];
        if (letra == ' ') {
            count_words++;
        }

    }
    return count_words;
}
int count_setences(string text){
    int count_setences = 0;
    for (int i= 0;i<strlen(text);i++){
        char letra = text[i];
        if (letra == '.' || letra == '!' || letra == '?') {
            count_setences++;
        }

    }
    return count_setences;
}
