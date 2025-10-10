import tkinter as tk
import calendar
from datetime import date


def create_calendar(year, month, frame):
    cal = calendar.monthcalendar(year, month)

    for widget in frame.winfo_children():
        widget.destroy()

    tk.Label(
        frame,
        text=f"{calendar.month_name[month]} {year}",
        font=('Arial', 18, 'bold'),
        pady=10
    ).grid(row=0, column=0, columnspan=7, sticky='nsew')
    frame.grid_rowconfigure(0, weight=1)
    for col in range(7):
        frame.grid_columnconfigure(col, weight=1)

    for i, day in enumerate(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']):
        tk.Label(frame, text = day, width = 6, font = ('Arial', 16)).grid(row = 1, column = i)

    for i, week in enumerate(cal):
        for j, day in enumerate(week):
            if day == 0:
                tk.Label(frame, text = '', width = 6, font = ('Arial', 12)).grid(row = i + 2, column = j)
            else:
                tk.Label(frame, text = str(day), width = 6, font = ('Arial', 12)).grid(row = i + 2, column = j)

def next_month():
    global year, month
    
    if month ==  12:
        month = 1
        year += 1
    else:
        month += 1
        year = year

    create_calendar(year, month, frame)

def prev_month():
    global year, month

    if month == 1:
        month = 12
        year -= 1
    else:
        month -= 1
        year = year

    create_calendar(year, month, frame)
   

year = date.today().year
month = date.today().month

root = tk.Tk()
root.title("Calender")

frame = tk.Frame(root)
frame.pack()

create_calendar(year, month, frame)
prev_month_btn = tk.Button(root, text = "Previous Month", command = prev_month)
prev_month_btn.pack(side = tk.LEFT)

next_month_btn = tk.Button(root, text = "Next Month", command = next_month)
next_month_btn.pack(side = tk.RIGHT)

root.mainloop()
