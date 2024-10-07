#include <stdio.h>
#include <stdlib.h>
//generates grid
//prints hidden grid

int n;
int safe_count=0;
int safe_guessed=0;

void generategrid(int n, int* arr)
{
    for (int i=0; i<n; i++)
    {
        for (int j=0; j<n; j++)
        {
            (*(arr+j+(i*n)))=(rand())%2;
            if ((*(arr+j+(i*n)))==0)
            {
                safe_count+=1;
            }
        }
    }
}

void print_mine_visible(int n, int *arr_visible, int* arr)
{
    for (int k=0; k<n; k++)
    {
        int temp_counter=0;
        for (int z=0; z<n;z++)
        {
            temp_counter+=(*(arr+(z*n)+k));
        }
        printf(" %d ",temp_counter);
    }
    printf("\n-");
    for (int k=0; k<3*n; k++)
    {
        printf("-");
    }
    printf("\n");
    for (int i=0; i<n; i++)
    {
        printf("|");
        int counter_temp=0;
        for (int j=0; j<n; j++)
        {
            counter_temp+=(*(arr+j+(i*n)));
            if ((*(arr_visible+j+(i*n)))==1)
            {
                if ((*(arr+j+(i*n)))==1)
                {
                    printf("💣|");
                }
                else
                {
                    printf("✅|");
                }
            }
            else
            {
                printf("❓|");
            }
        }
        printf("%d",counter_temp);
        printf("\n");
        printf("-");
        for (int k=0; k<3*n; k++)
        {
            printf("-");
        }
        printf("\n");
    }
}

void print_asnwer(int n, int *arr_visible, int* arr)
{
    for (int k=0; k<n; k++)
    {
        int temp_counter=0;
        for (int z=0; z<n;z++)
        {
            temp_counter+=(*(arr+(z*n)+k));
        }
        printf(" %d ",temp_counter);
    }
    printf("\n-");
    for (int k=0; k<3*n; k++)
    {
        printf("-");
    }
    printf("\n");
    for (int i=0; i<n; i++)
    {
        printf("|");
        int counter_temp=0;
        for (int j=0; j<n; j++)
        {
            if ((*(arr+j+(i*n)))==1)
            {
                printf("💣|");
            }
            else
            {
                printf("✅|");
            }
        }
        printf("%d",counter_temp);
        printf("\n");
        printf("-");
        for (int k=0; k<3*n; k++)
        {
            printf("-");
        }
        printf("\n");
    }
}

int main()
{
    printf("ENTER NUMBER OF ROWS IN THE GRID (GREATER THAN 1): ");
    scanf("%d",&n);
    int grid[n][n];
    int guessed[n][n];
    int* startptr1;
    int* startptr2;
    startptr1=(&grid[0][0]);
    startptr2=(&guessed[0][0]);
    generategrid(n,startptr1);
    printf("\nENTER DIFFICULTY LEVEL:\n1.NOOB\n2.INTERMEDIAATE\n3.ADVANCED \nENTER YOUR OPTION NUMBER: ");
    int choice;
    scanf("%d",&choice);
    int mistake;
    switch (choice)
    {
        case 1:
            mistake=n*n;
            break;
        case 2:
            mistake=2*n;
            break;
        case 3:
            mistake=n;
            break;
    }
    printf("\nTHE NUMBER OF MINES IN EACH COLUMN ARE DISPLAYED ON TOP OF THE COLUMN\nTHE NUMBER OF MINES IN EACH ROW ARE DISPLAYED ON RIGHT OF THE ROW");
    printf("\nYOU HAVE %d LIVES TO COMPLETE THE GAME\nEVERYTIME YOU GUESS A TILE WITH A BOMB YOUR LFE GOES DOWN BY 1",mistake);
    printf("\n");
    for (int r=0;r<(n*n);r++) {(*(startptr2+r))=0;}
    print_mine_visible(n,startptr2,startptr1);
    while ((mistake>0)&&(safe_count!=safe_guessed))
    {
        printf("\nYOU HAVE %d LIVES LEFT",mistake);
        int guessed_row, guessed_column;
        printf("\nENTER THE ROW YOU THINK IS SAFE: ");
        scanf("%d",&guessed_row);
        printf("ENTER THE COLUMN YOU THINK IS SAFE: ");
        scanf("%d",&guessed_column);
        if (guessed[guessed_row-1][guessed_column-1]==0)
        {
            guessed[guessed_row-1][guessed_column-1]=1;
            if (grid[guessed_row-1][guessed_column-1]==1)
            {
                mistake-=1;
                printf("BOOOOOM\nTHE TILE HAD A BOMB\nYOU LOST A LIFE\n");
            }
            else
            {
                safe_guessed+=1;
                printf("WELL PLAYED\nTHIS WAS A SAFE SQUARE\n");
            }
        }
        else {printf("ENTER A SQUARE YOU HAVEN'T TRIED BEFORE\n");}
        print_mine_visible(n,startptr2,startptr1);
    }
    if (mistake==0) 
    {
        printf("\nYOU LOST\nTHE FOLLOWING IS HOW THE BOMBS WERE ARRANGED\n");
        print_asnwer(n,startptr2,startptr1);
    }
    else
    {
        printf("\nYOU WON\nWELL PLAYED\nTHE FOLLOWING IS HOW THE BOMBS WERE ARRANGED\n");
        print_asnwer(n,startptr2,startptr1);
    }
    return 0;
}