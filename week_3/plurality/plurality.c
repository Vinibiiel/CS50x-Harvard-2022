#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    for(int i = 0;i<candidate_count;i++){
        if(strcmp(candidates[i].name,name) == 0){
            candidates[i].votes++;
            return true;
        };
    }


    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    candidate maior = candidates[0];
    string winners[MAX] = {NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL};
    int count = 0;
    bool not_has_more = true;
    for(int i = 1;i<=candidate_count;i++){
        if(candidates[i].votes > maior.votes){
            maior = candidates[i];
        }
    }
    for(int j = 0;j<=candidate_count;j++){
        if(candidates[j].votes == maior.votes){
            winners[count] = candidates[j].name;
            not_has_more = false;
            count++;
        }
    }
    if(not_has_more){
        printf("%s\n",maior.name);
    }else{
        for(int k = 0;k<=candidate_count;k++){
            if (winners[k]){
                printf("%s\n",winners[k]);
            }
        }
    }

}