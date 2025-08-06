import numpy
import numpy as np
import bs4
import requests
import tkinter as tk
from tkinter import ttk
#from cell import Cell

from sudoku_model import Sudoku, Cell
from GUI import mainMenu, BoxWidget
from explainer import UnitType, EliminationStep


def main():

    stepPuzzles = getPuzzles()
    GUIPuzzles = getPuzzles()

    for step, gui in zip(stepPuzzles, GUIPuzzles):
        step.solve()
        gui.linkedList = step.linkedList
        node = gui.linkedList.head
        while(node != None):
            if isinstance(node.data, EliminationStep):
                for i, cell in enumerate(node.data.cells):
                    node.data.cells[i] = gui.grid[cell.x][cell.y]
            else:
                node.data.cell = gui.grid[node.data.cell.x][node.data.cell.y]
            node = node.next


    print(stepPuzzles[0])
    while (GUIPuzzles[0].linkedList.current != GUIPuzzles[0].linkedList.tail):
        print(GUIPuzzles[0].linkedList.current.data)
        GUIPuzzles[0].linkedList.current = GUIPuzzles[0].linkedList.current.next
    GUIPuzzles[0].linkedList.current = GUIPuzzles[0].linkedList.head

    nytOrange = "#f99c30"
    window = tk.Tk()

    window.geometry("850x600")
    window.title("Sudoku Solver")
    window.configure(bg=nytOrange)

    menu = mainMenu(window, GUIPuzzles)

    window.mainloop()

def getPuzzles():
    puzzleList = getGameData()

    temp = puzzleList[1]
    puzzleList[1] = puzzleList[2]
    puzzleList[2] = temp

    for i, puzzle in enumerate(puzzleList):
        puzzleList[i] = listToPuzzle(puzzle)
        puzzleList[i].difficulty = i
    return puzzleList

def getGameData():
    nytURL = "https://www.nytimes.com/puzzles/sudoku/easy"
    nytHTML = requests.get(nytURL)
    soup = bs4.BeautifulSoup(nytHTML.text, 'html.parser')
    lines = str(soup.prettify()).splitlines()

    gameData = ""
    for line in lines:
        if "gameData" in line:
            gameData = line
            break
    puzzles = gameData.split('"puzzle":[')
    puzzles.pop(0)
    for i in range(len(puzzles)): #scrub string
        scrubbedPuzzle = puzzles[i].split("]")
        puzzles[i] = scrubbedPuzzle[0]

    for i in range(len(puzzles)): #string to int
        puzzles[i] = puzzles[i].split(",")
        for j in range(len(puzzles[i])):
            puzzles[i][j] = int(puzzles[i][j])

    return puzzles # | 0: easy | 1: hard | 2: medium |

def listToPuzzle(puzzleList):
    COLS = 9
    ROWS = 9
    puzzle = Sudoku(np.empty((9,9), dtype= object))
    for i in range(ROWS):
        for j in range(COLS):

            if puzzleList[i*COLS + j] != 0:
                puzzle.grid[i][j] = Cell(i, j, puzzleList[i*COLS + j], [], puzzle, True)

            else:
                puzzle.grid[i][j] = Cell(i, j, 0, [1,2,3,4,5,6,7,8,9], puzzle)

    return puzzle

main()
