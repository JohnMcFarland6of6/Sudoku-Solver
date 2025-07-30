#save meta data, to .json, function registry
from enum import Enum

class SolutionStep():
    def __init__(self, cell= None, solution= None, explanation= None):
        self.cell = cell
        self.solution = solution
        self.explanation = explanation

    def __str__(self):
        return f"Cell at ({self.cell.x},{self.cell.y}) is {self.solution} because of {self.explanation}"

class CandidatesStep():
    def __init__(self, cells= None, solutions= None, explanation= None):
        self.cells = cells
        self.solutions = solutions
        self.explanation = explanation

    def __str__(self):
        toStr = "Cells at"
        for cell in self.cells:
            toStr += f" ({cell.x},{cell.y}),"
        toStr += f"cannot be "
        for solution in self.solutions:
            toStr += f"{solution}, "
        toStr += f"because of {self.explanation}"
        return toStr


class method(Enum):
    FORCED_DIGIT = 1
    HIDDEN_SINGLE = 2
    LINE_BOX_REDUCTION = 3
    BOX_LINE_REDUCTION = 4


'''
1) add variable so we know if its row/col/box for reduction 
1) put steps in GUI
2) make steps readable, don't include greyed boxes in reduction, etc 
2) reorganize logic so it does easier steps first
3) program back button 
4) program naked pair or hidden subsets or both 



'''