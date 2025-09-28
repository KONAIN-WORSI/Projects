import random

computer_choice = random.randint(1,100)
count = 1

while True:
    user_choice = int(input('Guess the number from 1 to 100: '))


    if user_choice > computer_choice:
        print('Enter lower number and try again!')
        count += 1
    elif user_choice < computer_choice:
        print('Enter greater number and try again!')
        count += 1
    else:
        print(f'Congratulations! You guess the correct number {computer_choice} in {count} times!')
        break

