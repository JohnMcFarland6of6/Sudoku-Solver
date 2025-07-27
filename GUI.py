import tkinter as tk
from tkinter import ttk

nytOrange = "#f99c30"

window = tk.Tk()

window.geometry("800x600")
window.title("Sudoku Solver")
window.configure(bg=nytOrange)


class mainMenu():
    def __init__(self, master):
        self.sudoku = sudokuDisplay(master)
        self.menu = ttk.Frame(master, width=700, height= 500, style='menuFrame.TFrame')
        self.master = master
        self.topBar = ttk.Frame(master, width = 800, height = 25, style='topBar.TFrame')
        self.topBar.pack_propagate(False)

        style = ttk.Style()
        style.configure('menuFrame.TFrame', background = nytOrange)
        style.configure('topBar.TFrame', background= "white")

        #topBar = ttk.Frame(master, width = 800, height = 25, style='topBar.TFrame')
        self.topBar.pack()

        self.menu.pack()

        label = tk.Label(self.menu, text="Which Sudoku do you want solved?", font=('Times New Roman', 16))
        label.configure(bg=nytOrange)
        label.pack(pady = 30)

        easyButton = tk.Button(self.menu, text="Easy", width = "15", bg="black", fg="white", command = lambda: self.changeWindow(0))
        easyButton.pack(pady = 10)
        mediumButton = tk.Button(self.menu, text="Medium", width = "15", bg="black", fg="white", command =lambda: self.changeWindow(1))
        mediumButton.pack(pady = 10)
        hardButton = tk.Button(self.menu, text="Hard", width = "15", bg="black", fg="white", command =lambda: self.changeWindow(2))
        hardButton.pack(pady = 10)

    def changeWindow(self, difficulty):
        self.menu.forget()
        self.sudoku.pack()
        print(difficulty)

        #menuFra

    def toMenu(self):
        self.sudoku.forget()
        self.menu.tkraise()
        self.menu.pack()



class sudokuDisplay(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)



        label = tk.Label(self, text="Tada!")
        label.pack()


menu = mainMenu(window)

window.mainloop()
