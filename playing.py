import curses
import random
import time
from curses import wrapper

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the typing test!")
    stdscr.addstr(1, 0, "Press any key to continue...")
    stdscr.refresh()
    stdscr.getkey()

def load_text():
    with open("text1.txt", 'r') as f:
        lines = f.readlines()
        return random.choice(lines).strip()
    
def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"wpm: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)

        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)


def typing_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round(len(current_text) / (time_elapsed / 60) / 5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey() 
        except:
            continue


        if ord(key) == 27:
            break

        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)       
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)

    while True:
        typing_test(stdscr)

        stdscr.addstr(2, 0, "You have completed the text! Press any key to continue")
        stdscr.addstr(3, 0, "Press ESC to exit or any other key to continue...")

        key = stdscr.getkey()
        if ord(key) == 27:
            break
 

wrapper(main)