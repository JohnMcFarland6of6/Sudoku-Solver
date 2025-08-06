#save meta data, to .json, function registry
from enum import Enum

class Step():
    def __init__(self, cell= None, solution= None, explanation= None, unit= None):
        self.cell = cell
        self.solution = solution
        self.explanation = explanation
        self.unit = unit
        self.peers = None
        self.finalCandidates = None
    def __str__(self):
        match self.explanation:
            case Method.FORCED_DIGIT:
                return f"Cell at ({self.cell.y+1},{self.cell.x+1}) is {self.solution} because this is the cell's only candidate."
            case Method.HIDDEN_SINGLE:
                return f"Cell at ({self.cell.y+1},{self.cell.x+1}) is {self.solution} because this is the only possible {self.solution} in the cell's {self.unit.__str__()}."

    def setPeers(self, peers):
        self.peers = peers

class EliminationStep():
    def __init__(self, cells= None, solutions= None, explanation= None, unit= None):
        self.cells = cells
        self.solutions = solutions
        self.explanation = explanation
        self.unit = unit
        self.peers = None
        self.eliminations = {}




    def __str__(self):
        match self.explanation:
            case Method.BOX_LINE_REDUCTION:
                return "poop"
            case Method.LINE_BOX_REDUCTION:
                toStr = f"Since the cells at "
                for cell in self.cells:
                    toStr += f"({cell.y+1},{cell.x+1}), "
                toStr += f"are the only cells in the {self.unit.__str__()} that can be a "
                for solution in self.solutions:
                    toStr += f"{solution}, "
                toStr += "no other cells in their box can have those candidates."
                return toStr

            case Method.NAKED_PAIR:
                toStr = f"Since the cells at "
                for cell in self.cells:
                    toStr += f"({cell.y+1},{cell.x+1}), "
                toStr += f"must be a {self.solutions[0]} or a {self.solutions[1]}, they are the only cell is their {self.unit.__str__()} that can have those candidates."
                return toStr






class Method(Enum):
    FORCED_DIGIT = 1
    HIDDEN_SINGLE = 2
    NAKED_PAIR = 3
    LINE_BOX_REDUCTION = 4
    BOX_LINE_REDUCTION = 5

class UnitType(Enum):
    CELL = 0
    ROW = 1
    COL = 2
    BOX = 3

    def __str__(self):
        match self:
            case UnitType.CELL:
                return "cell"
            case UnitType.ROW:
                return "row"
            case UnitType.COL:
                return "column"
            case UnitType.BOX:
                return "box"


'''
1) add variable so we know if its row/col/box for reduction x
1) put steps in GUI x
2) make steps readable, don't include greyed boxes in reduction, etc x
2) reorganize logic so it does easier steps first x
3) program back button x
4) program naked pair or hidden subsets or both 

    a) loop through grid[i][j].widget and reset values when you go to each puzzle x
    b) run update with data from stepQueue and cell.widget.label x
    c) do something with candidate vs cell 
    d) back button 
    
    a) each cell holds a cell.original and cell.final 
    b) write better print funct for GUI
    c) make linked list instead of queue x
    d) make steps readable 
    e) make back button x

        
'''