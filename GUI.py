import tkinter as tk
from tkinter import ttk

from sudoku import Sudoku, Cell

nytOrange = "#f99c30"



class mainMenu():
    def __init__(self, master, puzzles):
        self.puzzles = puzzles
        self.sudoku = None #sudokuWidget(master, puzzle)
        self.info = infoWidget(master)
        self.menu = ttk.Frame(master, width=500, height= 500, style='menuFrame.TFrame')
        self.master = master
        self.topBar = ttk.Frame(master, width = 850, height = 25, style='topBar.TFrame')
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
        self.puzzles[difficulty].getCandidates()
        self.sudoku = sudokuWidget(self.master, self.puzzles[difficulty])
        self.sudoku.pack(side=tk.LEFT, padx=25)
        self.info.pack(side=tk.RIGHT, padx=25, pady=100, fill="y")
        for widget in self.topBar.winfo_children():
            widget.pack(side="left")

    def toMenu(self):
        self.sudoku.forget()
        self.info.forget()
        self.menu.pack()
        for widget in self.topBar.winfo_children():
            widget.forget()

class sudokuWidget(tk.Frame):
    def __init__(self, parent, puzzle):
        super().__init__(parent)
        for i in range(3):
            self.rowconfigure(i, weight = 1, uniform="grid")
            self.columnconfigure(i, weight = 1, uniform="grid")

        for i, box in enumerate(puzzle.getBoxes()):
            BoxWidget(self, box).grid(row=i//3, column=i%3, sticky="nsew")

        self.configure(highlightbackground="black", highlightthickness=3, relief="solid")

class BoxWidget(tk.Frame):
    def __init__(self, parent, box):
        super().__init__(parent)
        self.pack_propagate(False)
        for i in range(3):
            self.rowconfigure(i, weight = 1, uniform="grid")
            self.columnconfigure(i, weight = 1, uniform="grid")
        for i, row in enumerate(box.cells.reshape(3,3)):
            for j, cell in enumerate(row):
                CellWidget(self, cell).grid(row=i, column=j, sticky="nsew")
        self.configure(highlightbackground="#979797", highlightthickness=1, relief="solid")

class CellWidget(tk.Frame):
    def __init__(self, parent, cell):
        super().__init__(parent)

        self.configure(width= 50, height=50)
        self.grid_propagate(False)
        if cell.solution != 0:
            label = tk.Label(self, text=cell.solution,  font=(
                'Franklin Gothic', 21, "bold"), highlightbackground="#979797", highlightthickness=1, relief="flat", anchor="center", background="#dfdfdf")
        else:
            candidateStr = ""
            for possibleCandidate in range(1,10):
                if possibleCandidate in cell.candidates:
                    candidateStr += str(possibleCandidate)
                else:
                    candidateStr += " "
                if possibleCandidate == 3: #==0 and possibleCandidate != 9:
                    candidateStr += "\n"
                elif possibleCandidate == 6:
                    candidateStr += "\n "
                else:
                    candidateStr += " "
            label = tk.Label(self, text=candidateStr,  font=(
                'Courier', 9), highlightbackground="#979797", highlightthickness=1, relief="flat", anchor="center")

        label.grid(sticky="nsew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

class infoWidget(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        backButton = tk.Button(self, text="<-", width = "15", bg="#dfdfdf", command =lambda: self.back())
        backButton.grid(row= 0, column= 0)

        nextButton = tk.Button(self, text="->", width = "15", bg="#dfdfdf", command =lambda: self.next())
        nextButton.grid(row= 0, column= 1)

        explanationLabel = tk.Label(
            self, text= 'Press "->" for first step.', bg="#dfdfdf", highlightbackground="#979797", highlightthickness=1, relief="flat", width=36, anchor="nw")
        explanationLabel.grid(row= 1, column=0, columnspan=2, pady=0, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        self.configure(bg=nytOrange)



    def back(self):
        pass
    def next(self):
        pass






