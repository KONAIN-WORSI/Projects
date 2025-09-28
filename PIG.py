import random

def roll_dice():
    min_value = 1
    max_value = 6
    return random.randint(min_value , max_value)



while True:
    players = int(input("Enter the number of players:"))
    if 2 <= players <= 4:
        break
    else:
        print('Please! enter a number between 2 and 4 ')

max_score = 30
player_score = [0 for _ in range(players)]

while max(player_score) < max_score:
    
    for player_idx in range(players):
        if max(player_score) >= max_score:
            break  # Breaks out of the for loop if any player has reached the max score
        print(f"\n player {player_idx + 1} turn has started!")
        print(f"player {player_idx +1} total score is {player_score[player_idx]}")
        current_score = 0

        while True:
            should_roll = input(f"\nplayer {player_idx +1} do you want to roll the dice?  (y/n):").lower()
            if should_roll == 'y':
                value = roll_dice()
                print(f"player {player_idx + 1} rolled {value}")
                if value == 1:
                    print(f"player {player_idx + 1} turn is over, no points added")
                    current_score = 0
                    break
                else:
                    current_score += value
                    player_score[player_idx ] += current_score
                print(f"\nplayer {player_idx +1} total score is {player_score[player_idx]}\n")
                if player_score[player_idx] >= max_score:
                    break  # End the current player's turn if they reach the max score
            else:
                print("PLease enter y or n")
                
print(f"\nplayer {player_score.index(max(player_score)) + 1} wins with a score of {max(player_score)}!")