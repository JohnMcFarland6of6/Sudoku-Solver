from symtable import Class

class Cell:
    #solution = 0
    #candidates = []
    def __init__(self, x,y, solution = 0, candidates = None):
        self.x = x
        self.y = y
        self.solution = solution  # Instance attribute
        self.candidates = candidates    # Instance attribute

    def __str__(self):
        return f"Solution: {self.solution}, candidates: {self.candidates} at {self.x},{self.y}"

    def __repr__(self):
        return f"Solution: {self.solution}, candidates: {self.candidates}"

    def getRow(self, puzzle):
        return puzzle[self.x]

    def getCol(self, puzzle):
        return puzzle[:,self.y]

    def getBox(self, puzzle):
        box = puzzle[
              (self.x//3)*3:(self.x//3)*3+3,
              (self.y//3)*3:(self.y//3)*3+3
              ]
        return box.flatten()

'''

bool true
    if candidate is in the row  
        if bool is true
            then set bool to false
        if bool is false
            break everything 








'''