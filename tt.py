import tkinter as tk
from tkinter import ttk


root = tk.Tk()

# window title
root.title("Athan")

# window size
root.geometry('600x400')

# place a label on the root window
#message = tk.Label(root, text="Hello, World!")
#message.pack()

# label with a specific font
label = ttk.Label(
    root,
    text='Fajer',
    font=("Helvetica", 80))

label.pack(ipadx=10, ipady=10)

# label with a specific font
label2 = ttk.Label(
    root,
    text='05.25 am',
    font=("Helvetica", 80))

label2.pack(ipadx=10, ipady=10)

# keep the window displaying
root.mainloop()