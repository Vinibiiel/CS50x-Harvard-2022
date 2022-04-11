// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include "dictionary.h"
#include <string.h>
#include <stdlib.h>

#define HASHTABLE_SIZE 1024

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;


// Define array pointer to hash table
node *hashtable[HASHTABLE_SIZE];
int word_count = 0;

// TODO: Choose number of buckets in hash table
const unsigned int N = 10000;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // dictionary has only words in lowercase, so we need convert the word to lower
    int word_length = strlen(word);
    char word_lower[word_length+1];

    // We need make a terminator in the word, so that the computer understands that the word is over
    for (int i = 0;i<word_length;i++){
        word_lower[i] = tolower(word[i]);
    }
    word_lower[word_length] = '\0';

    // Generate a hash for the word
    int hash_word_index = hash(word_lower);

    // We are working with linked list, so we need start at a point in the list
    node *start = hashtable[hash_word_index];

    node *data = start; // We need read the data, and then jump to the next with the pointer in the node struct.

    while(data != NULL){
        if(strcmp(word_lower,data->word) == 0){
            return true;
        }else{
            data = data->next;
        }
    }
    return false;
}

// Hash function adapted from https://stackoverflow.com/questions/7666509/hash-function-for-string
unsigned int hash(const char *word)
{
    unsigned int secret = 53;
    int c;

    while ((c = *word++))
    {
        secret = ((secret << 5) + secret) + c;
    }
    // Return the hashed value mod the size of hashtable to be used as index
    return secret % HASHTABLE_SIZE; // Index of HashTable
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *dict = fopen(dictionary, "r");
    if(dict == NULL){
        printf("Could not open file.\n");
        return false;
    }

    char word_dict[LENGTH+1];
    while(fgets(word_dict,LENGTH+2,dict) != NULL){
        word_dict[strlen(word_dict) - 1] = '\0';
        int hash_word_index = hash(word_dict);

        node *word = malloc(sizeof(node));
        strcpy(word->word, word_dict);
        word->next = hashtable[hash_word_index];

        hashtable[hash_word_index] = word;
        word_count++;
    }
    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0;i<1024;i++){
        node *now = hashtable[i];
        while(now != NULL){
            node *before = now;
            now = before->next;
            free(before);
        }
    }
    return true;
}
