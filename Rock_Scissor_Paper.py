import random

choice = {1: 'Rock', 2: 'Scissor', 3: 'Paper'}


comp_score = 0
user_score = 0

while user_score < 3 and comp_score < 3:
    user_choice = input("Enter your choice between Rock, Scissor, Paper: ").lower()
    computer_choice = choice[random.randint(1, 3)].lower()

    print(f'Computer choice {computer_choice.capitalize()} and Your choice is {user_choice}')

    if user_choice == computer_choice:
        print('Its a Tie!')
    elif user_choice == 'rock' and computer_choice == 'scissor':
        user_score += 1
        print('You win!')
    elif user_choice == 'rock' and computer_choice == 'paper':
        comp_score += 1
        print('Computer wins!')
    elif user_choice == 'scissor' and computer_choice == 'paper':
        user_score += 1
        print('You win!')
    elif user_choice == 'scissor' and computer_choice == 'rock':
        comp_score += 1
        print('Computer wins!')
    elif user_choice == 'paper' and computer_choice == 'rock':
        user_score += 1
        print('You win!')
    elif user_choice == 'paper' and computer_choice == 'scissor':
        comp_score += 1
        print('Computer wins!')
    else:
        print('invalid input!')

    print(f'Computer score is {comp_score} and Your score is {user_score}')
    
print('Game Over!')

        