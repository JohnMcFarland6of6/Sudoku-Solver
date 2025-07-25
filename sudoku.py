from symtable import Class
#rom cell import Cell

class Sudoku:
    DIMENSIONS = 9
    difficulties = ["easy", "medium", "hard"]
    def __init__(self, grid, difficulty):
        self.grid = grid
        self.difficulty = difficulty

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
        return self.grid[:]
    def getCols(self):
        return self.grid.T[:]
    def getBoxes(self):
        boxList = []
        for i in range(3):
            for j in range(3):
                boxList.append(self.grid
                               [i*3:i*3+3,j*3:j*3+3] #.flatten()
                               )
        return boxList
    def getDifficulty(self):
        return self.difficulties[self.difficulty]

class Unit:
    def __init__(self, cells = None, ):
        self.cells = cells


    def getCandidates(self):
        candidates = []
        for cell in self.cells:
            for candidate in cell.candidates:
                if candidate not in candidates:
                    candidates.append(candidate)
        return candidates

class Cell:
    #solution = 0
    #candidates = []
    def __init__(self, x,y, solution = 0, candidates = None, sudoku = None):
        self.x = x
        self.y = y
        self.solution = solution
        self.candidates = candidates
        self.sudoku = sudoku


    def __str__(self):
        return f"Solution: {self.solution}, candidates: {self.candidates} at {self.x},{self.y}"

    def __repr__(self):
        return f"Solution: {self.solution}, candidates: {self.candidates}"

    def getRow(self):
        return self.sudoku[self.x]

    def getCol(self):
        return self.sudoku[:,self.y]

    def getBox(self):
        box = self.sudoku[
              (self.x//3)*3:(self.x//3)*3+3,
              (self.y//3)*3:(self.y//3)*3+3
              ]
        return box.flatten()