import numpy as np
import bs4
import requests
from cell import Cell

def main():
    puzzleLists = getGameData()
    easyPuzzle = listToPuzzle(puzzleLists[0])
    printPuzzle(easyPuzzle)

    solve(easyPuzzle)
    printCandidates(easyPuzzle)


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
                puzzle[i][j] = Cell(puzzleList[i*COLS + j], [])
            else:
                puzzle[i][j] = Cell(0, [1,2,3,4,5,6,7,8,9])

    return puzzle

def removeCandidates(puzzleRow):
    COLS = 9
    ROWS = 9
    solutionsInRow = []
    for cell in puzzleRow:
        solutionsInRow.append(cell.solution)
    for i in range(ROWS):
        for solution in solutionsInRow:
            if solution in puzzleRow[i].candidates:
                puzzleRow[i].candidates.remove(solution)

def printPuzzle(puzzle):
    for i in range(len(puzzle)):
        print("")
        for j in range(len(puzzle[0])):
            print(puzzle[i][j].solution, " ", end='')
    print("")

def printCandidates(puzzle):
    for i in range(len(puzzle)):
        print("")
        for j in range(len(puzzle[0])):
            print(puzzle[i][j].candidates)
    print("")

def getEasyCandidates(puzzle):
    ROWS = 9
    COLS = 9
    for i in range(ROWS):
        removeCandidates(puzzle[i])
    for i in range(COLS):
        removeCandidates(puzzle[:,i])
    for i in range(3):
        for j in range(3):
            box = puzzle[i*3:i*3+3,j*3:j*3+3]
            removeCandidates(box.flatten())

def solve(puzzle):
    ROWS = 9
    COLS = 9
    puzzleFin = False
    getEasyCandidates(puzzle)
    while(puzzleFin is False):
        puzzleFin = True
        for i in range(ROWS):
            for j in range(COLS):
                #print(puzzle[i][j].candidates) #TEMP###############
                if len(puzzle[i][j].candidates) == 1:
                    solution = puzzle[i][j].candidates[0]
                    puzzle[i][j].solution = solution
                    update(puzzle[i], [solution]) #updates row
                    update(puzzle[:,j], [solution]) #updates col
                    what = (i%3)*3
                    theheck = (j%3)*3
                    box = puzzle[((i)//3)*3:(i//3)*3+3,(j//3)*3:(j//3)*3+3].flatten()
                    update(box, [solution]) #updates 3x3 box

                    #printCandidates(puzzle) #TEMP###############
                else:
                    puzzleFin = False
        printPuzzle(puzzle)


def update(list, solutionsInRow):
    ROWS = 9
    for i in range(ROWS):
        for solution in solutionsInRow:
            if solution in list[i].candidates:
                list[i].candidates.remove(solution)

main()
#box = easyPuzzle[0:3,0:3]