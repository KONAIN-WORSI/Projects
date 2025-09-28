import turtle
import random
import time

WIDTH, HEIGHT = 800,700
COLORS = ['red', 'purple', 'green', 'blue', 'pink', 'black', 'violet', 'magenta', 'grey', 'lightgreen']

def get_number_of_racers():
    racers = 0
    while True:
        racers = input('Enter a number of racers between (2-10): ')

        if racers.isdigit():
            racers = int(racers)
            if 2 <= racers <= 10:
                return racers
            else:
                print('Invalid number of racers. Enter a number between (2-10)')
        else:
            print('Invalid syntax!, PLease enter a number for racres')


def race(colors):
    turtles = create_turtle(colors)

    while True:
        for racer in turtles:
            distance = random.randrange(1, 20)
            racer.forward(distance)

            x, y = racer.pos()
            if y >= HEIGHT // 2 - 10:
                return colors[turtles.index(racer)]


def create_turtle(colors):
    turtles = []
    spacingx = WIDTH // (len(colors) + 1)

    for i,colors in enumerate(colors):
        racer = turtle.Turtle()
        racer.color(colors)
        racer.shape('turtle')
        racer.forward(random.randrange(2,20))
        racer.left(90)
        racer.penup()
        racer.setpos(- WIDTH // 2 + (i + 1) * spacingx, - HEIGHT // 2 + 20)
        racer.pendown()
        turtles.append(racer)

    return turtles



def init_screen():
    screen = turtle.Screen()
    screen.setup(WIDTH, HEIGHT)
    screen.title('Turtle Racing Game 🐢')

racer = get_number_of_racers()
init_screen()

random.shuffle(COLORS)
colors = COLORS[:racer]

start_time = time.time()
winner = race(colors)
end_time = time.time()

finish_time = round(end_time - start_time)
print(f'The winner of the turtle racing is {winner} with the finish time of {finish_time} second!')

