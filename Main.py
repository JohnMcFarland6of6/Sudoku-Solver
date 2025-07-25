import numpy
import numpy as np
import bs4
import requests
#from cell import Cell
from sudoku import Sudoku, Cell



def main():
    puzzles = getPuzzles()
    print(puzzles[1])


    getCandidates(puzzles[1])
    solve(puzzles[1])
    print(puzzles[1])

def getPuzzles():
    puzzleList = getGameData()

    temp = puzzleList[1]
    puzzleList[1] = puzzleList[2]
    puzzleList[2] = temp

    for i, puzzle in enumerate(puzzleList):
        puzzleList[i] = Sudoku(listToPuzzle(puzzle), i)
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
    puzzle = np.empty((9,9), dtype= object)
    for i in range(ROWS):
        for j in range(COLS):

            if puzzleList[i*COLS + j] != 0:
                puzzle[i][j] = Cell(i, j, puzzleList[i*COLS + j], [], puzzle)
            else:
                puzzle[i][j] = Cell(i, j, 0, [1,2,3,4,5,6,7,8,9], puzzle)

    return puzzle

def eliminateCandidates(unit):
    COLS = 9
    ROWS = 9
    solutions = []
    for cell in unit:
        solutions.append(cell.solution)
    for i in range(ROWS):
        for sol in solutions:
            if sol in unit[i].candidates:
                unit[i].candidates.remove(sol)

def getCandidates(puzzle):
    ROWS = 9
    COLS = 9
    for row in puzzle.getRows():
        eliminateCandidates(row)
    for col in puzzle.getCols():
        eliminateCandidates(col)
    for box in puzzle.getBoxes():
        eliminateCandidates(box.flatten())

def solve(puzzle):
    getCandidates(puzzle)
    for x in range(3):
        pointingPair(puzzle)
        for i in range(10):
            forcedDigit(puzzle)
            for unit in puzzle.getRows():
                hiddenSingle(unit)
            for unit in puzzle.getCols():
                hiddenSingle(unit)
            for unit in puzzle.getBoxes():
                hiddenSingle(unit.flatten())
    print(puzzle)


def forcedDigit(puzzle):
    ROWS = 9
    COLS = 9
    puzzleFin = False

    while(puzzleFin is False):
        puzzleFin = True
        for row in puzzle.grid:
            for cell in row:
                if len(cell.candidates) == 1:
                    puzzleFin = False
                    solution = cell.candidates[0]
                    cell.solution = solution
                    update(cell.getRow(), [solution]) #updates row
                    update(cell.getCol(), [solution]) #updates col
                    update(cell.getBox(), [solution]) #updates 3x3 box
        #print(puzzle)

def update(unit, solutions):
    for cell in unit:
        for sol in solutions:
            if sol in cell.candidates:
                cell.candidates.remove(sol)

def hiddenSingle(unit):
    for candidate in range(1,10):
        onlyCell = None
        onlyCellFlag = True
        flag = False
        for cell in unit:
            if candidate in cell.candidates:
                if onlyCellFlag:
                    onlyCellFlag = False
                    flag = True
                    onlyCell = cell
                else:
                    flag = False
                    onlyCell = None
                    break
        if flag:
            onlyCell.solution = candidate
            onlyCell.candidates = []
            update(onlyCell.getRow(), [candidate]) #updates row
            update(onlyCell.getCol(), [candidate]) #updates col
            update(onlyCell.getBox(), [candidate]) #updates 3x3 box

def pointingPair(puzzle):
    boxes = puzzle.getBoxes()
    for box in boxes:
        box = box.reshape(3,3)
        for i, row in enumerate(box):
            otherRows = numpy.delete(box, i, 0)
            for candidate in getUnitCandidates(row):
                if candidate not in getUnitCandidates(otherRows.flatten()):
                    for cell in row[0].getRow():
                        if cell not in row:
                            update([cell], [candidate])


def getUnitCandidates(unit):
    candidates = []
    for cell in unit:
        for candidate in cell.candidates:
            if candidate not in candidates:
                candidates.append(candidate)
    print(candidates)
    return candidates



main()
