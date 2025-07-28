import tkinter as tk
from tkinter import ttk


from sudoku import Sudoku, Cell

nytOrange = "#f99c30"


class mainMenu():
    def __init__(self, master, puzzle):
        self.sudoku = BoxWidget(master, puzzle.getBoxes()[0])
        self.menu = ttk.Frame(master, width=700, height= 500, style='menuFrame.TFrame')
        self.master = master
        self.topBar = ttk.Frame(master, width = 800, height = 25, style='topBar.TFrame')
        self.topBar.pack_propagate(False)

        style = ttk.Style()
        style.configure('menuFrame.TFrame', background = nytOrange)
        style.configure('topBar.TFrame', background= "white")

        backButton = tk.Button(self.topBar, text="<-", width="10", bg="white", command =lambda : self.toMenu())
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
        for widget in self.topBar.winfo_children():
            widget.pack(side="left")

    def toMenu(self):
        self.sudoku.forget()
        self.menu.pack()
        for widget in self.topBar.winfo_children():
            widget.forget()

class sudokuDisplay(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        #label = tk.Label(self, text="Tada!")
        #label.pack()
        b = BoxWidget(parent, [1,2,3,4,5,6,7,8,9])
        #b.pack()

class BoxWidget(tk.Frame):
    def __init__(self, parent, box):
        super().__init__(parent)
        #grid = tk.Frame(self, width = 81, height = 81, borderwidth=1, relief="solid")
        self.config(width=243, height=243)
        self.pack_propagate(False)
        for i, row in enumerate(box):
            for j, cell in enumerate(row):
                if cell.solution != 0:
                    tk.Label(self, text=cell.solution,  font=(
                        'Times New Roman', 21), wraplength=27, relief="solid", borderwidth= 1).grid(
                        row=i, column=j, sticky="nsew")
                else:
                    candidateStr = ""
                    for possibleCandidate in range(1,10):
                        if possibleCandidate in cell.candidates:
                            candidateStr = candidateStr + str(possibleCandidate) + " "
                        else:
                            candidateStr = candidateStr + "  "
                    tk.Label(self, text=candidateStr,  font=(
                        'Times New Roman', 8), wraplength=27, relief="solid", borderwidth= 1,height=3, width=6).grid(
                        row=i, column=j,sticky="nsew")






