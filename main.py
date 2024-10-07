import os
import discord
import numpy as np
from keep_alive import keep_alive

my_secret = os.environ['token']

valid_responses = [[3, 4, 5, 6, 7, 8, 9, 10], ["easy", "medium", "hard"]]


def safe_counter(game_grid, n):
    count = 0
    for i in range(n):
        for j in range(n):
            if game_grid[i][j] == 0:
                count += 1
    return (count)


def print_grid(game_grid, guess_grid, n):
    column_sum = []
    row_sum = []
    for i in range(n):
        temp1 = 0
        temp2 = 0
        for j in range(n):
            temp1 += int(game_grid[j][i])
            temp2 += int(game_grid[i][j])
        column_sum.append(temp1)
        row_sum.append(temp2)

    ans = "  "
    for i in range(n):
        ans += str(column_sum[i])
        ans += "      "
    ans += "\n"

    ans += ("-" * 5 * n)
    ans += "\n"
    for i in range(n):
        ans += '|'
        for j in range(n):
            if guess_grid[i][j] == 0:
                ans += '❓|'
            else:
                if game_grid[i][j] == 0:
                    ans += '✅|'
                else:
                    ans += "💣|"
        ans += " " + str(row_sum[i]) + " |"
        ans += "\n"
        ans += ("-" * 5 * n)
        ans += "\n"
    return (ans)


player_list = {}

error_message = "Please enter in the following format \nmine <grid_size> <difficulty>\nGrid size must be greater than or equal to 3 \nand lesser than or equal to 10 \nValid difficulty level are <easy> / <medium> / <hard>"

wrong_move_message = "Please enter your move in the following format \nmine <column number> <row number> \nTo quit playing use the following command \nmine quit"

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if (message.content.lower()).startswith('mine'):
        current_player = message.author
        if message.content.lower() == "mine help":
            await message.channel.send("The number of top of the columns represent the total number of bombs in that particular column. \nThe number on the right represents the total number of bombs in that particular row. \nThe objective of the goal is to select all the safe tiles. \nTo start playing enter in the following format \nmine <grid_size> <difficulty>\nGrid size must be greater than or equal to 3 \nand lesser than or equal to 10 \nValid difficulty level are <easy> / <medium> / <hard> \nMake your move in the following format \nmine <column number> <row number> \nTo quit playing use the command <mine quit>\n")
        elif current_player not in player_list:
            current_message = message.content.split()
            if (len(current_message) < 3):
                await message.channel.send(error_message)
            elif ((int(current_message[1]) not in valid_responses[0]) or (current_message[2] not in valid_responses[1])):
                await message.channel.send(error_message)
            else:
                game_grid = np.random.randint(2, size=(int(current_message[1]),int(current_message[1])))
                guessed_grid = np.random.randint(1, size=(int(current_message[1]), int(current_message[1])))
                if current_message[2].lower() == "easy":
                    life = (int(current_message[1])) * 3
                if current_message[2].lower() == "medium":
                    life = (int(current_message[1])) * 2
                if current_message[2].lower() == "hard":
                    life = (int(current_message[1]))
                grid_size = int(current_message[1])
                player_list[current_player] = [grid_size, life, game_grid, guessed_grid, safe_counter(game_grid, grid_size)]
                await message.channel.send(print_grid(game_grid, guessed_grid, grid_size))
        else:
            current_message = message.content.split()
            game_grid = player_list[current_player][2]
            guessed_grid = player_list[current_player][3]
            grid_size = player_list[current_player][0]
            flag = 0
            if message.content.lower() == "mine quit":
                await message.channel.send("You quit the game")
                player_list.pop(current_player)
                flag = 1
            elif (len(current_message) < 3):
                await message.channel.send(wrong_move_message)
                flag = 1
            if flag == 1:
                await message.channel.send(print_grid(game_grid, guessed_grid, grid_size))
            column = int(current_message[1]) - 1
            row = int(current_message[2]) - 1
            if ((row >= player_list[current_player][1]) or (column >= player_list[current_player][1]) ) and ((row <= 0) or (column <= 0)) and (flag == 0):
                await message.channel.send("Please enter row and column within range")
            elif (player_list[current_player][3][column][row]== 1) and flag == 0:
                await message.channel.send("Please enter a box you haven't already guessed")
            else:
                player_list[current_player][3][column][row] = 1
                if player_list[current_player][2][column][row] == 1:
                    player_list[current_player][1] -= 1
                    await message.channel.send("BOOM, YOU SELECTED A BOMB TILE")
                    await message.channel.send(
                        str("YOU HAVE " + str(player_list[current_player][1]) +" LIVES LEFT"))
                else:
                    player_list[current_player][4] -= 1
                    await message.channel.send("PHEW, YOU SELECTED A SAFE TILE")
                    await message.channel.send(str("YOU HAVE " + str(player_list[current_player][1]) +" LIVES LEFT"))

            if player_list[current_player][1] == 0:
                await message.channel.send("You have exhausted all your lifes and the game is over")
                player_list.pop(current_player)

            if player_list[current_player][4] == 0:
                await message.channel.send("You have won the game, congratulations")
                player_list.pop(current_player)
            await message.channel.send(print_grid(game_grid, guessed_grid, grid_size))

keep_alive()
client.run(my_secret)
