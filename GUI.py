import tkinter as tk
from tkinter import ttk
import numpy as np

from double_linked_list import Node
from explainer import UnitType, Method, Step, EliminationStep
from sudoku_model import Sudoku, Unit, Cell
from enum import Enum
#from sudoku import Sudoku, Cell

nytOrange = "#f99c30"


ORANGE= "#f99c30"
BORDER_GRAY= "#979797"
GIVEN_GRAY= "#dfdfdf"
UNIT_YELLOW= "#FFF59D"

class mainMenu():
    def __init__(self, master, puzzles):
        self.puzzles = puzzles
        self.sudoku = None #sudokuWidget(master, puzzle)
        self.info = None #infoWidget(master)
        self.menu = ttk.Frame(master, width=500, height= 500, style='menuFrame.TFrame')
        self.master = master
        self.topBar = ttk.Frame(master, width = 850, height = 25, style='topBar.TFrame')
        self.topBar.pack_propagate(False)

        style = ttk.Style()
        style.configure('menuFrame.TFrame', background = ORANGE)
        style.configure('topBar.TFrame', background= "white")


        backButton = tk.Button(self.topBar, text="<-", width="10", bg="white", command =lambda : self.toMenu())
        self.topBar.pack()

        self.menu.pack()

        label = tk.Label(self.menu, text="Which Sudoku do you want solved?", font=('Times New Roman', 16))
        label.configure(bg= ORANGE)
        label.pack(pady = 30)

        easyButton = tk.Button(self.menu, text="Easy", width = "15", bg="black", fg="white", command = lambda: self.changeWindow(0))
        easyButton.pack(pady = 10)
        mediumButton = tk.Button(self.menu, text="Medium", width = "15", bg="black", fg="white", command =lambda: self.changeWindow(1))
        mediumButton.pack(pady = 10)
        hardButton = tk.Button(self.menu, text="Hard", width = "15", bg="black", fg="white", command =lambda: self.changeWindow(2))
        hardButton.pack(pady = 10)

    def changeWindow(self, difficulty):
        self.menu.forget()
        self.info = infoWidget(self.master, self.puzzles[difficulty])
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
        self.puzzle = puzzle
        for i in range(3):
            self.rowconfigure(i, weight = 1, uniform="grid")
            self.columnconfigure(i, weight = 1, uniform="grid")

        for i, box in enumerate(puzzle.getBoxes()):
            BoxWidget(self, box).grid(row=i//3, column=i%3, sticky="nsew")

        self.configure(highlightbackground="black", highlightthickness=3, relief="solid")

    def resetSudoku(self):
        #self.puzzle.grid = self.puzzle.originalGrid
        for row in self.puzzle.grid:
            for cell in row:
                cell.widget.getLabel()

class BoxWidget(tk.Frame):
    def __init__(self, parent, box):
        super().__init__(parent)
        self.pack_propagate(False)
        for i in range(3):
            self.rowconfigure(i, weight = 1, uniform="grid")
            self.columnconfigure(i, weight = 1, uniform="grid")
        for i, row in enumerate(box.cells.reshape(3,3)):
            for j, cell in enumerate(row):
                widget = CellWidget(self, cell)
                widget.grid(row=i, column=j, sticky="nsew")
                cell.widget = widget
        self.configure(highlightbackground=BORDER_GRAY, highlightthickness=1, relief="solid")

class CellWidget(tk.Frame):
    def __init__(self, parent, cell):
        super().__init__(parent)
        self.cell = cell
        self.label= None
        self.configure(width= 50, height=50)
        self.grid_propagate(False)
        self.getInitialLabel()

        self.label.grid(sticky="nsew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def __str__(self):
        return self.cell.__str__() + "I exist!"

    def getInitialLabel(self):
        if self.cell.solution != 0:
            self.label = tk.Label(self, text=str(self.cell.solution),  font=(
                'Franklin Gothic', 21, "bold"), highlightbackground=BORDER_GRAY, highlightthickness=1, relief="flat", anchor="center", background=GIVEN_GRAY)
        else:
            candidateStr = ""
            for possibleCandidate in range(1,10):
                if possibleCandidate in self.cell.candidates:
                    candidateStr += str(possibleCandidate)
                else:
                    candidateStr += " "
                if possibleCandidate == 3: #==0 and possibleCandidate != 9:
                    candidateStr += "\n"
                elif possibleCandidate == 6:
                    candidateStr += "\n "
                else:
                    candidateStr += " "
            self.label = tk.Label(self, text=candidateStr,  font=(
                'Courier', 9), highlightbackground=BORDER_GRAY, highlightthickness=1, relief="flat", anchor="center")

    def getNewLabel(self):
        if self.cell.solution != 0:
            self.label.config(text=str(self.cell.solution),  font=(
                'Franklin Gothic', 21, "bold"))
        else:
            candidateStr = ""
            for possibleCandidate in range(1,10):
                if possibleCandidate in self.cell.candidates:
                    candidateStr += str(possibleCandidate)
                else:
                    candidateStr += " "
                if possibleCandidate == 3: #==0 and possibleCandidate != 9:
                    candidateStr += "\n"
                elif possibleCandidate == 6:
                    candidateStr += "\n "
                else:
                    candidateStr += " "
            self.label.config(text=candidateStr, font=('Courier', 9))

    def highlightCell(self, color):
        self.label.config(bg=color)
        
    def unhighlightCell(self):
        self.label.config(bg="white")


    def getNextNode(self):
        return self.cell.sudoku.linkedList.current.next
    def getPrevNode(self):
        return self.cell.sudoku.linkedList.current.prev

class infoWidget(tk.Frame):
    def __init__(self, parent, puzzle):
        super().__init__(parent)
        self.puzzle = puzzle
        self.steps = puzzle.linkedList

        backButton = tk.Button(self, text="<-", width = "15", bg=GIVEN_GRAY, command =lambda: self.back())
        backButton.grid(row= 0, column= 0)

        nextButton = tk.Button(self, text="->", width = "15", bg=GIVEN_GRAY, command =lambda: self.next())
        nextButton.grid(row= 0, column= 1)

        self.label = tk.Label(
            self, text= 'Press "->" for first step.', bg=GIVEN_GRAY, highlightbackground=BORDER_GRAY, highlightthickness=1, relief="flat", width=36, anchor="nw", wraplength=250, justify=tk.LEFT)
        self.label.grid(row= 1, column=0, columnspan=2, pady=0, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        self.configure(bg=ORANGE)


    def back(self):
        #self.puzzle.linkedList.current = self.puzzle.linkedList.current.prev
        step = self.puzzle.linkedList.current.prev.data
        prevStep = None
        if self.puzzle.linkedList.current.prev.prev != None:
            prevStep = self.puzzle.linkedList.current.prev.prev.data

        if isinstance(step, Step):
            step.cell.widget.highlightCell("white")
            match step.unit:
                case UnitType.ROW:
                    for cell in step.cell.getRow().cells:
                        cell.widget.highlightCell("white")
                case UnitType.COL:
                    for cell in step.cell.getCol().cells:
                        cell.widget.highlightCell("white")
                case UnitType.BOX:
                    for cell in step.cell.getBox().cells:
                        cell.widget.highlightCell("white")

            self.label.config(text=prevStep.__str__())
            step.cell.candidates.append(step.solution)
            step.cell.solution = 0
            step.cell.widget.getNewLabel()
        else:
            self.label.config(text=prevStep.__str__())

            if step.explanation == Method.LINE_BOX_REDUCTION:
                for cell in step.cells[0].getBox().unsolvedCells:
                    cell.widget.highlightCell("white")
            else:
                match step.unit:
                    case UnitType.ROW:
                        for cell in step.cells[0].getRow().unsolvedCells:
                            cell.widget.highlightCell("white")
                    case UnitType.COL:
                        for cell in step.cells[0].getCol().unsolvedCells:
                            cell.widget.highlightCell("white")
                    case UnitType.BOX:
                        for cell in step.cells[0].getBox().unsolvedCells:
                            cell.widget.highlightCell("white")





        if isinstance(prevStep, Step):
            match prevStep.unit:
                case UnitType.ROW:
                    for cell in prevStep.cell.getRow().unsolvedCells:
                        cell.widget.highlightCell(UNIT_YELLOW)
                case UnitType.COL:
                    for cell in prevStep.cell.getCol().unsolvedCells:
                        cell.widget.highlightCell(UNIT_YELLOW)
                case UnitType.BOX:
                    for cell in prevStep.cell.getBox().unsolvedCells:
                        cell.widget.highlightCell(UNIT_YELLOW)
            prevStep.cell.widget.highlightCell(ORANGE)

            prevStep.cell.candidates = prevStep.finalCandidates
            prevStep.cell.solution = 0
            prevStep.cell.widget.getNewLabel()
            if prevStep.peers != []:
                Unit(prevStep.peers).unupdate(prevStep.solution)

            for cell in prevStep.peers:
                cell.widget.getNewLabel()
        else:

            if prevStep.unit == UnitType.ROW:
                for cell in prevStep.cells[0].getRow().unsolvedCells:
                    #if cell not in step.cells:
                    cell.widget.highlightCell(UNIT_YELLOW)
            elif prevStep.unit == UnitType.COL:
                for cell in prevStep.cells[0].getCol().unsolvedCells:
                    cell.widget.highlightCell(UNIT_YELLOW)
            else:
                for cell in prevStep.cells[0].getBox().unsolvedCells:
                    cell.widget.highlightCell(UNIT_YELLOW)

            for cell in prevStep.cells:
                cell.widget.highlightCell(ORANGE)

            for candidate in prevStep.eliminations.keys():
                Unit(prevStep.eliminations[candidate]).unupdate(candidate)
                for cell in prevStep.eliminations[candidate]:
                    cell.widget.getNewLabel()


        self.puzzle.linkedList.current = self.puzzle.linkedList.current.prev

    def next(self):
        step = None
        prevStep = None

        if self.puzzle.linkedList.current != None:
            step = self.puzzle.linkedList.current.data

            if self.puzzle.linkedList.current.prev != None:
                prevStep = self.puzzle.linkedList.current.prev.data
            self.label.config(text=step.__str__())
        else:
            step = self.puzzle.linkedList.tail.data
            step.cell.widget.highlightCell("white")
            step.cell.solution = step.solution
            step.cell.widget.getNewLabel()
            self.label.config(text="...And the sudoku is solved!")

        if prevStep != None:
            if isinstance(prevStep, Step):
                prevStep.cell.widget.highlightCell("white")
                match prevStep.unit:
                    case UnitType.ROW:
                        for cell in prevStep.cell.getRow().unsolvedCells:
                            cell.widget.highlightCell("white")
                    case UnitType.COL:
                        for cell in prevStep.cell.getCol().unsolvedCells:
                            cell.widget.highlightCell("white")
                    case UnitType.BOX:
                        for cell in prevStep.cell.getBox().unsolvedCells:
                            cell.widget.highlightCell("white")

                prevStep.cell.solution = prevStep.solution
                prevStep.finalCandidates = prevStep.cell.candidates
                prevStep.cell.candidates = []
                prevStep.cell.widget.getNewLabel()
                prevStep.peers= prevStep.cell.updatePeers(prevStep.solution)
                for cell in prevStep.peers:
                    cell.widget.getNewLabel()
            else:
                cellsToUpdate = None

                if prevStep.explanation == Method.LINE_BOX_REDUCTION:
                    cellsToUpdate = prevStep.cells[0].getBox()
                    if prevStep.unit == UnitType.ROW:
                        cellsToUnhighlight = prevStep.cells[0].getRow()
                    else:
                        cellsToUnhighlight = prevStep.cells[0].getRow()
                    for cell in cellsToUnhighlight.cells:
                        cell.widget.highlightCell("white")
                else:
                    match prevStep.unit:
                        case UnitType.ROW:
                            cellsToUpdate = prevStep.cells[0].getRow()
                        case UnitType.COL:
                            cellsToUpdate = prevStep.cells[0].getCol()
                        case UnitType.BOX:
                            cellsToUpdate = prevStep.cells[0].getBox()

                temp = cellsToUpdate.cells.tolist()
                for cell in prevStep.cells:
                    temp.remove(cell)
                cellsToUpdate.cells = np.array(temp)
                for solution in prevStep.solutions:
                    eliminations = cellsToUpdate.update(solution)
                    if len(eliminations) != 0:
                        prevStep.eliminations[solution] = eliminations
                for cell in cellsToUpdate.cells:
                    cell.widget.highlightCell("white")
                    cell.widget.getNewLabel()
                for cell in prevStep.cells:
                    cell.widget.highlightCell("white")


        if step != None:
            if isinstance(step, Step):
                match step.unit:
                    case UnitType.ROW:
                        for cell in step.cell.getRow().unsolvedCells:
                            cell.widget.highlightCell(UNIT_YELLOW)
                    case UnitType.COL:
                        for cell in step.cell.getCol().unsolvedCells:
                            cell.widget.highlightCell(UNIT_YELLOW)
                    case UnitType.BOX:
                        for cell in step.cell.getBox().unsolvedCells:
                            cell.widget.highlightCell(UNIT_YELLOW)

                step.cell.widget.highlightCell(ORANGE)
            else:
                print(step)

                if step.unit == UnitType.ROW:
                    for cell in step.cells[0].getRow().unsolvedCells:
                        #if cell not in step.cells:
                        cell.widget.highlightCell(UNIT_YELLOW)
                elif step.unit == UnitType.COL:
                    for cell in step.cells[0].getCol().unsolvedCells:
                        cell.widget.highlightCell(UNIT_YELLOW)
                else:
                    for cell in step.cells[0].getBox().unsolvedCells:
                        cell.widget.highlightCell(UNIT_YELLOW)

                for cell in step.cells:
                    cell.widget.highlightCell(ORANGE)
        if self.puzzle.linkedList.current != None:
            self.puzzle.linkedList.current = self.puzzle.linkedList.current.next








