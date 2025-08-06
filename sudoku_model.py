from symtable import Class
import numpy as np
from enum import Enum
from double_linked_list import Node, DoubleLinkedList
from explainer import Step, Method, UnitType, EliminationStep


class Sudoku:
    DIMENSIONS = 9
    difficulties = ["easy", "medium", "hard"]
    def __init__(self, grid, difficulty= None):
        self.grid = grid
        self.difficulty = difficulty
        self.linkedList = DoubleLinkedList()

#self, x,y, solution = 0, candidates= None, sudoku= None, isGiven= False, widget= None):
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

    def isSolved(self):
        solved = True
        for row in self.grid:
            for cell in row:
                if cell.solution == 0:
                    solved = False
                    break
            if solved is False:
                break
        return solved


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
        whoops = 0
        while(self.isSolved() is False and whoops < 10):
            wasUsed = False
            while(True):
                wasUsed = self.forcedDigit()
                if wasUsed:
                    break
                wasUsed = self.hiddenSingle()
                if wasUsed:
                    break
                wasUsed = self.nakedPair()
                if wasUsed:
                    break

                wasUsed = self.lineBoxReduction()
                if wasUsed:
                    break
                wasUsed = self.boxLineReduction()
                if wasUsed:
                    whoops += 1
                    print(whoops)
                    break

        return self.linkedList

    def forcedDigit(self):
        puzzleFin = False
        cellSolved = False
        while(puzzleFin is False):
            puzzleFin = True
            for row in self.grid:
                for cell in row:
                    if len(cell.candidates) == 1:
                        cellSolved = True
                        puzzleFin = False
                        solution = cell.candidates[0]
                        cell.solution = solution
                        cell.updatePeers(solution)
                        self.linkedList.addTail(Node(Step(self.grid[cell.x][cell.y], cell.solution, Method.FORCED_DIGIT, UnitType.CELL)))
        return cellSolved

    def boxLineReduction(self):
        wasUsed = False
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
                    for candidate in eliminatedCandidates:
                        Unit(eliminatedCells).update(candidate)
                    wasUsed = True
                    Step(eliminatedCells, eliminatedCandidates, Method.BOX_LINE_REDUCTION, UnitType.ROW)
            if wasUsed:
                break
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
                    for candidate in eliminatedCandidates:
                        Unit(eliminatedCells).update(candidate)
                    wasUsed = True
                    self.linkedList.addTail(Node(EliminationStep(eliminatedCells, eliminatedCandidates, Method.BOX_LINE_REDUCTION, UnitType.COL)))
            if wasUsed:
                break
        return wasUsed

    def lineBoxReduction(self):
        wasUsed = False
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
                            if cell not in band and candidate in cell.candidates:
                                eliminatedCells.append(cell)
                if len(eliminatedCells) !=0:
                    for candidate in eliminatedCandidates:
                        Unit(eliminatedCells).update(candidate)
                    wasUsed = True
                    self.linkedList.addTail(Node(EliminationStep(band.tolist(), eliminatedCandidates, Method.LINE_BOX_REDUCTION, UnitType.ROW)))
            if wasUsed:
                break
        return wasUsed

    def hiddenSingle(self):
        wasUsed = False
        for box in self.getBoxes():
            wasUsed = box.hiddenSingleHelper(UnitType.BOX)
            if wasUsed:
                break

        if wasUsed is False:
            for row in self.getRows():
                wasUsed= row.hiddenSingleHelper(UnitType.ROW)
                if wasUsed:
                    break

        if wasUsed is False:
            for col in self.getCols():
                wasUsed= col.hiddenSingleHelper(UnitType.COL)
                if wasUsed:
                    break

        return wasUsed

    def nakedPair(self):
        wasUsed = False
        for box in self.getBoxes():
            wasUsed = box.nakedPairHelper(UnitType.BOX)
            if wasUsed:
                break

        if wasUsed is False:
            for row in self.getRows():
                wasUsed = row.nakedPairHelper(UnitType.ROW)
                if wasUsed:
                    break

        if wasUsed is False:
            for col in self.getCols():
                wasUsed = col.nakedPairHelper(UnitType.COL)
                if wasUsed:
                    break
        return wasUsed

class Unit:
    def __init__(self, cells = None, ):
        if isinstance(cells, list):
            cells = np.array(cells)
        self.cells = cells
        self.sudoku = self.cells[0].sudoku

        candidates = []
        for cell in self.cells:
            for candidate in cell.candidates:
                if candidate not in candidates:
                    candidates.append(candidate)
        self.candidates = candidates

        unsolvedCells = []
        for cell in self.cells:
            if cell.solution == 0:
                unsolvedCells.append(cell)
        self.unsolvedCells = unsolvedCells


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

    def update(self, solution):
        updatedCells = []
        for cell in self.cells:
            if solution in cell.candidates:
                updatedCells.append(cell)
                cell.candidates.remove(solution)
        return updatedCells

    def unupdate(self, solution):
        for cell in self.cells:
            cell.candidates.append(solution)

    def hiddenSingleHelper(self, unitT):
        wasUsed = False
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
                wasUsed = True
                onlyCell.solution = candidate
                onlyCell.candidates = []
                onlyCell.updatePeers(candidate)
                self.sudoku.linkedList.addTail(Node(Step(onlyCell, onlyCell.solution, Method.HIDDEN_SINGLE, unitT)))
            if wasUsed:
                break
        return wasUsed

    def nakedPairHelper(self, unitT):
        wasUsed = False
        firstCell = None
        possibleCells = []
        for cell in self.cells:
            if len(cell.candidates) == 2:
                possibleCells.append(cell)

        for i, cell in enumerate(possibleCells):
            firstCell = possibleCells[i]
            for j in range(i+1, len(possibleCells)):
                if firstCell.candidates == possibleCells[j].candidates:
                    secondCell = possibleCells[j]

                    updatedCells = set()
                    cellsToUpdate = []
                    for cell in self.cells:
                        if cell != firstCell and cell != secondCell:
                            cellsToUpdate.append(cell)
                    cellsToUpdateUnit = Unit(cellsToUpdate)
                    for candidate in firstCell.candidates:
                        updatedCells.update(cellsToUpdateUnit.update(candidate))
                    if len(updatedCells) != 0:
                        wasUsed = True
                        nakedPairCandidates = []
                        for candidate in firstCell.candidates:
                            nakedPairCandidates.append(candidate)
                        self.sudoku.linkedList.addTail(Node(EliminationStep([firstCell, secondCell], nakedPairCandidates, Method.NAKED_PAIR, unitT)))
                    break
            if wasUsed:
                break
        return wasUsed


class Cell:
    def __init__(self, x,y, solution = 0, candidates= None, sudoku= None, isGiven= False, widget= None):
        self.x = x
        self.y = y
        self.solution = solution
        self.candidates = candidates
        self.sudoku = sudoku
        self.isGiven = isGiven
        self.widget = widget

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
    def updatePeers(self, solution):
        rows = self.getRow().update(solution)
        cols = self.getCol().update(solution)
        box = self.getBox().update(solution)
        peers = set()
        peers.update(rows)
        peers.update(cols)
        peers.update(box)
        return list(peers)





