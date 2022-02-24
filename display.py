def updateDisplay(PTime, Index):
    # Figuring out the next salah time
    if Index == 0:
        Salah = "Fajer"
    elif Index == 1:
        Salah = "Doher"
    elif Index == 2:
        Salah = "Aser"
    elif Index == 3:
        Salah = "Magreb"
    else:
        Salah = "Isha"
    
    # label with a specific font
    label = ttk.Label(
        root,
        text=Salah,
        font=("Helvetica", 80),
        background="black", foreground="white")

    label.pack(ipadx=10, ipady=10)


    # label with a specific font
    label2 = ttk.Label(
        root,
        text=str(PTime),
        font=("Helvetica", 80),
        background="black", foreground="white")

    label2.pack(ipadx=10, ipady=10)

    # keep the window displaying
    root.mainloop()
