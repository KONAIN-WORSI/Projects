import tkinter as tk
from tkinter import messagebox, simpledialog

# creating the main window
root = tk.Tk()
root.title('To Do List')
root.geometry('600x600')
root.config(bg='#9b9987')

tasks = []

def add_task():
    task = task_entry.get()
    if task.strip() == '':
        messagebox.showerror('Input error','Please enter a task')
        return
    task_listbox.insert(tk.END, task)
    tasks.append(task)
    task_entry.delete(0, tk.END)


def remove_task():
    selected = task_listbox.curselection()
    if not selected:
        messagebox.showerror('Select task','Please select task to delete')

    for i in reversed(selected):
        task_listbox.delete(i)
        del tasks[i]

def mark_done():
    selected = task_listbox.curselection()

    if not selected:
        messagebox.showerror('Select task', 'Please select task to mark as done')

    for i in selected:
        task = task_listbox.get(i)
        if not task.startswith('✔️ '):
            task_listbox.delete(i)
            task_listbox.insert(i, '✔️' + task)
            task_listbox.itemconfig(i, fg='gray')
        

def remove_mark_done():
    selected = task_listbox.curselection()

    if not selected:
        messagebox.showerror('Select task', 'Please select task to undo mark as done')


    for i in selected:
        task = task_listbox.get(i)

        if task.startswith('✔️'):
            # Remove the checkmark and restore normal color
            new_task = task.lstrip('✔️')
            task_listbox.delete(i)
            task_listbox.insert(i, new_task)
            task_listbox.itemconfig(i, fg='black')


def update_tasks():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        task_listbox.insert(tk.END, task)


# UI elements
title_label = tk.Label(root, text = 'To Do List', font = ('Helvetica',18,'bold'), bg = 'White smoke')
title_label.pack(pady = 10)

task_entry = tk.Entry(root, font= ('Helvetica', 14))
task_entry.pack(padx = 20, pady = 10, fill = tk.X)

task_listbox = tk.Listbox(root, width=60, height=20)
task_listbox.pack(padx = 20, pady = 10, fill = tk.BOTH, expand = True)

add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.pack(side=tk.LEFT, padx=10)

remove_button = tk.Button(root, text="Remove Task", command=remove_task)
remove_button.pack(side=tk.LEFT, padx=10)

mark_as_done = tk.Button(root, text = 'Mark as Done', command = mark_done)
mark_as_done.pack(side = tk.RIGHT, pady = 5, padx = 5)

remove_mark_done_btn = tk.Button(root, text = 'Remove Mark Done', command = remove_mark_done)
remove_mark_done_btn.pack(side = tk.RIGHT, pady = 5, padx = 5)


update_tasks()
root.mainloop()