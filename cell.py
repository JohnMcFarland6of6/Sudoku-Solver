from symtable import Class

class Cell:
    #solution = 0
    #candidates = []
    def __init__(self, solution = 0, candidates = None):
        self.solution = solution  # Instance attribute
        self.candidates = candidates    # Instance attribute

    def __str__(self):
        return f"Solution: {self.solution}, candidates: {self.candidates}"

    def __repr__(self):
        return f"Solution: {self.solution}, candidates: {self.candidates}"
