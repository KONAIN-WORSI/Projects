import curses
from curses import wrapper
import datetime
import json
import os

def screen_set_up(stdscr):
    stdscr.clear()
    stdscr.addstr(0 , 0, 'Welcome to the TO-DO List app.')
    stdscr.addstr(1 , 0, 'Press any key to start the application...')
    stdscr.refresh()
    stdscr.getkey()


def load_screen(stdscr):
    stdscr.clear()
    stdscr.addstr(0 , 0, 'TO-DO LIST APP')
    stdscr.addstr(1 , 0, 'Enter the to-do list items (press Enter on a blank line to finish):')
    stdscr.refresh()
    curses.echo()
    row = 3
    items = []
    while True:
        stdscr.move(row, 4)
        stdscr.clrtoeol()
        item_to_do = stdscr.getstr(row, 4, 100)
        item = item_to_do.decode('utf-8').strip()
        if item == "":
            break
        items.append(item)
        row += 1
    curses.noecho()
    try:
        with open('to_do_list.txt', 'a') as f:
            for item in items:
                f.write(item + '\n')
    except Exception:
        print("Something went wrong!")

def save_file(stdcsr):
    # Ensure the JSON file is saved in the real OS filesystem
   current_dir = os.path.dirname(os.path.abspath(__file__))
   txt_path = os.path.join(current_dir, 'to_do_list.txt')
   json_path = os.path.join(current_dir, 'to_do_list.json')

   try:
       with open('to_do_list.txt', 'r') as f:
           j = f.readlines()
           # Convert each line to a dictionary with a timestamp
           todo_items = []
           for line in j:
               item = line.strip()
               if item:
                   todo_items.append({
                       "item": item,
                       "timestamp": datetime.datetime.now().isoformat()
                   })
           # Save to JSON file
           with open(json_path, 'w') as jf:
               json.dump(todo_items, jf, indent=4)
   except Exception as e:
       stdcsr.addstr(5 , 0, f'Error in saving json: {e}')
   


def main(stdscr):
    screen_set_up(stdscr)
    load_screen(stdscr)
    save_file(stdscr)

wrapper(main)
