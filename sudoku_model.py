from symtable import Class
import numpy as np
#import GUI
from explainer import SolutionStep, CandidatesStep, method

class Sudoku:
    DIMENSIONS = 9
    difficulties = ["easy", "medium", "hard"]
    def __init__(self, grid, difficulty= None):
        self.grid = grid
        self.difficulty = difficulty
        self.stepQueue = []

    def __str__(self):
        sudok = self.difficulties[self.difficulty]
        for row in self.grid:
            sudok = sudok +"\n"
            for cell in row:
                sudok = sudok + str(cell.solution) + "  "
        return sudok
    def __repr__(self):
        sudok = self.difficulties[self.difficulty]
        for row in self.grid:
            sudok = sudok +"\n"
            for cell in row:
                sudok = sudok + str(cell.solution) + "  "
        return sudok

    def printCandidates(self):
        for row in self.grid:
            print("")
            for cell in row:
                print(cell.candidates)
        print("")

    def getRows(self):
        rows = []
        for row in self.grid[:]:
            rows.append(Unit(row))
        return rows
    def getCols(self):
        cols = []
        for col in self.grid.T[:]:
            cols.append(Unit(col))
        return cols
    def getBoxes(self):
        boxList = []
        for i in range(3):
            for j in range(3):
                boxList.append(Unit(self.grid
                               [i*3:i*3+3,j*3:j*3+3].flatten()
                               ))
        return boxList
    def getDifficulty(self):
        return self.difficulties[self.difficulty]

    def getCandidates(self):
        for row in self.getRows():
            row.eliminateCandidates()
        for col in self.getCols():
            col.eliminateCandidates()
        for box in self.getBoxes():
            box.eliminateCandidates() #have to flatten before

    def solve(self):
        self.getCandidates()
        for x in range(4):
            self.forcedDigit()
            self.hiddenSingle()
            self.lineBoxReduction()
            self.boxLineReduction()

    def forcedDigit(self):
        puzzleFin = False
        while(puzzleFin is False):
            puzzleFin = True
            for row in self.grid:
                for cell in row:
                    if len(cell.candidates) == 1:
                        puzzleFin = False
                        solution = cell.candidates[0]
                        cell.solution = solution
                        cell.getRow().update([solution])
                        cell.getCol().update([solution])
                        cell.getBox().update([solution])
                        self.stepQueue.append(SolutionStep(cell, cell.solution, method.FORCED_DIGIT))


    def boxLineReduction(self): #box-line reduction
        boxes = self.getBoxes()
        for box in boxes:
            box = box.cells.reshape(3,3)
            for i, row in enumerate(box):
                otherRows = Unit(np.delete(box, i, 0).flatten())
                eliminatedCandidates = []
                eliminatedCells = []
                for candidate in Unit(row).candidates:
                    if candidate not in otherRows.candidates:
                        eliminatedCandidates.append(candidate)
                        for cell in row[0].getRow().cells:
                            if cell not in row:
                                eliminatedCells.append(cell)
                if len(eliminatedCells) !=0:
                    Unit(eliminatedCells).update(eliminatedCandidates)
                    CandidatesStep(eliminatedCells, eliminatedCandidates, method.BOX_LINE_REDUCTION)

            for i, col in enumerate(box.T):
                otherCols = Unit(np.delete(box, i, 1).flatten())
                eliminatedCandidates = []
                eliminatedCells = []
                for candidate in Unit(col).candidates:
                    if candidate not in otherCols.candidates:
                        eliminatedCandidates.append(candidate)
                        for cell in col[0].getCol().cells:
                            if cell not in col:
                                eliminatedCells.append(cell)
                if len(eliminatedCells) !=0:
                    Unit(eliminatedCells).update(eliminatedCandidates)
                    self.stepQueue.append(CandidatesStep(eliminatedCells, eliminatedCandidates, method.BOX_LINE_REDUCTION))


    def lineBoxReduction(self):
        for row in self.getRows():
            rowBox = row.cells.reshape(3,3)
            for i, band  in enumerate(rowBox):
                otherBands = Unit(np.delete(rowBox,i,0).flatten())
                eliminatedCandidates = []
                eliminatedCells = []
                for candidate in Unit(band).candidates:
                    if candidate not in otherBands.candidates:
                        eliminatedCandidates.append(candidate)
                        for cell in band[0].getBox().cells:
                            if cell not in band:
                                eliminatedCells.append(cell)
                if len(eliminatedCells) !=0:
                    Unit(eliminatedCells).update(eliminatedCandidates)
                    self.stepQueue.append(CandidatesStep(eliminatedCells, eliminatedCandidates, method.LINE_BOX_REDUCTION))

    def hiddenSingle(self):
        for row in self.getRows():
            row.hiddenSingleHelper()
        for col in self.getCols():
            col.hiddenSingleHelper()
        for box in self.getBoxes():
            box.hiddenSingleHelper()

class Unit:
    def __init__(self, cells = None, ):
        self.cells = cells
        self.sudoku = self.cells[0].sudoku
        candidates = []
        for cell in self.cells:
            for candidate in cell.candidates:
                if candidate not in candidates:
                    candidates.append(candidate)
        self.candidates = candidates

    def eliminateCandidates(self):
        COLS = 9
        ROWS = 9
        solutions = []
        for cell in self.cells:
            solutions.append(cell.solution)
        for cell in self.cells:
            for sol in solutions:
                if sol in cell.candidates:
                    cell.candidates.remove(sol)

    def update(self, solutions):
        for cell in self.cells:
            for sol in solutions:
                if sol in cell.candidates:
                    cell.candidates.remove(sol)

    def hiddenSingleHelper(self):
        for candidate in range(1,10):
            onlyCell = None
            onlyCellFlag = True
            flag = False
            for cell in self.cells:
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
                onlyCell.getRow().update([candidate])
                onlyCell.getCol().update([candidate])
                onlyCell.getBox().update([candidate])
                self.sudoku.stepQueue.append(SolutionStep(onlyCell, onlyCell.solution, method.HIDDEN_SINGLE))


class Cell:
    def __init__(self, x,y, solution = 0, candidates= None, sudoku= None, isGiven= False, widget= None):
        self.x = x
        self.y = y
        self.solution = solution
        self.candidates = candidates
        self.sudoku = sudoku
        self.isGiven = isGiven
        self.widge = widget

    def __str__(self):
        return f"Solution: {self.solution}, candidates: {self.candidates} at {self.x},{self.y}"

    def __repr__(self):
        return f"Solution: {self.solution}, candidates: {self.candidates}"

    def getRow(self):
        return Unit(self.sudoku.grid[self.x])

    def getCol(self):
        return Unit(self.sudoku.grid[:,self.y])

    def getBox(self):
        box = Unit(self.sudoku.grid[
              (self.x//3)*3:(self.x//3)*3+3,
              (self.y//3)*3:(self.y//3)*3+3
              ].flatten())
        return box #.flatten()


