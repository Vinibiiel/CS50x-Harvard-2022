#include<cs50.h>
#include<stdio.h>

int calc_sum(bool is_odd,long card_number);
int firstDigit(long numb);
int main() {
    long numberCard = get_long("Number: ");

    int count = 0;
    long aux = numberCard;
    while(aux>0){
        aux = aux / 10;
        count++;
    }

    int result = calc_sum(count % 2 == 0, numberCard);
    int digit = firstDigit(numberCard);
    if(digit == 4 && (result % 10 == 0 || result % 10 == 4)){
        printf("VISA\n");
    }else if(digit == 3 && (result % 10 == 7 || (result % 10 == 5))){
        printf("AMEX\n");
    }else if((digit == 2 || digit == 5) && (result % 10 == 4 || result % 10 == 7)){
        printf("MASTERCARD\n");
    }
    else{
        printf("INVALID\n");
    }

    return 0;
}
int calc_sum(bool is_odd,long card_number){
    int rest = is_odd ? 0 : 1;
    int count = 0,sum = 0;

    while(card_number > 0) {
        int mod = card_number % 10;
        if (count % 2 == rest) {
            if ((mod*2)> 10){
                int numb = mod;
                while(numb>0){
                    sum += numb % 10;
                    numb = numb / 10;
            }
            }else{
                sum += mod;
            }
        }else{
            if ((mod*2)> 10){
                int numb = mod*2;
                while(numb>0){
                    sum += numb % 10;
                    numb = numb / 10;
            }
            }else{
                sum += mod*2;
            }
        }
        card_number = card_number / 10;
        count++;
    }
    if(count >= 12){
        return sum;
    }
    else{
        return -5;
    }
}
int firstDigit(long numb){
    long primeiro = numb;
    while(primeiro >= 10)
    {
       primeiro = primeiro / 10;
    }
    return primeiro;

}