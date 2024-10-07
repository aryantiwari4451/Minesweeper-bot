import random

n = int(input("Enter number of rows and column: "))
safe_count = 0;
safe_guessed = 0;


def generategrid (n, arr):
  for i in range (n):
    for j in range (n):
      arr[i][j] = random.int()%2
      if (arr[i][j] == 0):
        safe_count += 1
      
def print_mine_visible (n, arr_visible, arr):
  for k in range (n):
    temp_counter = 0
    for z in range (n):
      temp_counter += arr[k][z]
    print(" ",temp_counter," ")

