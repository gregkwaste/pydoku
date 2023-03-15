from itertools import combinations
puzzle = []
possible_vals = []


# Soduku Classes
class cell:
    def __init__(self):
        self.solved = False
        self.possible_vals = set(range(1, 9 + 1))
        self.value = 0
        self.x = None
        self.y = None
        self.updated = False
        self.box = None
        self.row = None
        self.column = None
    
    def report(self):
        if not self.solved:
            print("Cell ", self.x, self.y, "Possible Values:", self.possible_vals)
        else:
            print("Cell ", self.x, self.y, "Val:", self.value)


class sdk_element:
    def __init__(self):
        self.remaining_values = set(range(1, 9 + 1))
        self.cells = []
        self.name = ""
    
    def filter(self, c):
        if (c not in self.cells):
            print("Warning trying to filter based on a not owned cell")
            return
        
        if (not c.solved):
            print("Warning cell not yet solved")
            return

        for nc in self.cells:
            nc.possible_vals.discard(c.value)

    def findCellsWithPossibleVal(self, v):
        l = set()
        for c in self.cells:
            if c.solved:
                continue
            
            if v in c.possible_vals:
                l.add(c)
        
        return l

class Box(sdk_element):
    def __init__(self):
        pass


class puzzle:

    def __init__(self, size):
        self.matrix = [[0 for i in range(9)] for j in range(9)]
        self.boxes = []
        self.columns = []
        self.rows = []
        # Parameters
        self.size = None
        self.val_table = None
        self.state = []
        self.initStructures(size)

    def initStructures(self, size):
        #Populate Matrix
        for i in range(9):
            for j in range(9):
                c = cell()
                c.x = i
                c.y = j
                self.matrix[c.x][c.y] = c

        # Populate Rows
        for i in range(9):
            l = sdk_element()
            l.name = "Row " + str(i)
            for j in range(9):
                l.cells.append(self.matrix[i][j])
                self.matrix[i][j].row = l
            self.rows.append(l)

        # Populate Columns
        for i in range(9):
            l = sdk_element()
            l.name = "Column " + str(i)
            for j in range(9):
                l.cells.append(self.matrix[j][i])
                self.matrix[j][i].column = l
            self.columns.append(l)

        # Populate Boxes
        for box_i in range(3):
            for box_j in range(3):
                # Fetch cells
                l = sdk_element()
                l.name = "Box " + str(box_i) + " " + str(box_j)
                for i in range(3):
                    for j in range(3):
                        l.cells.append(self.matrix[box_i * 3 + i][box_j * 3 + j])
                        self.matrix[box_i * 3 + i][box_j * 3 + j].box = l
                self.boxes.append(l)

    def setupPuzzle(self, path):
        self.size = 9
        # GetData
        f = open(path)
        lines = f.readlines()
        for line_id in range(len(lines)):
            line = lines[line_id]
            values = list(map(int, line.rstrip('\n').split(',')))
            for i in range(len(values)):
                value = int(values[i])
                if (value):
                    c = self.matrix[line_id][i]
                    c.possible_vals = {value}
                    self.solve_cell(c)
        f.close()

    def resetCellStatus(self):
        for i in range(self.size):
            for j in range(self.size):
                self.matrix[i][j].updated = False

    def calcProgress(self):
        prog = 0
        for i in range(9):
            for j in range(9):
                if self.matrix[i][j].solved:
                    prog += 1
        return 9 ** 2 - prog

    def filter_solved(self, c):
        c.box.filter(c)
        c.row.filter(c)
        c.column.filter(c)
    
    def reportPossibleValues(self):
        print("-------------------")
        for r in self.rows:
            for c in r.cells:
                c.report()
        print("-------------------")

    def reportRemainingValues(self):
        for r_id in range(self.size):
            print("Row", r_id, self.rows[r_id].remaining_values)

        for c_id in range(self.size):
            print("Col", c_id, self.columns[c_id].remaining_values)

        for b_id in range(self.size):
            print("Box", b_id, self.boxes[b_id].remaining_values)


    def rowColumnPointingPairs(self):
        for struct in [self.rows, self.columns]:
            for b in struct:
                for val in b.remaining_values:
                    l = list(b.findCellsWithPossibleVal(val))
                    
                    #Check if found cells belong to the same box
                    boxDominance = True
                    box = l[0].box
                    for i in range(1, len(l)):
                        c = l[i]
                        if (c.box != box):
                            boxDominance = False
                    
                    if (boxDominance):
                        for c in box.cells:
                            if c not in l:
                                c.possible_vals.discard(val)

    def boxPointingPairs(self):
        for s in self.boxes:
            for val in s.remaining_values:
                l = list(s.findCellsWithPossibleVal(val))
                
                #Check if found cells belong to the same row
                rowDominance = True
                row = l[0].row
                for i in range(1, len(l)):
                    c = l[i]
                    if (c.row != row):
                        rowDominance = False
                
                if (rowDominance):
                    for c in row.cells:
                        if c not in l:
                            c.possible_vals.discard(val)

                
                #Check if found cells belong to the same column
                colDominance = True
                col = l[0].column
                for i in range(1, len(l)):
                    c = l[i]
                    if (c.column != col):
                        colDominance = False
                
            
                if (colDominance):
                    for c in col.cells:
                        if c not in l:
                            c.possible_vals.discard(val)
                


    def hiddenX(self, x):
        structs = [self.rows, self.columns, self.boxes]
        # Apply on Every struct iteratively
        for s in structs:
            for b in s:
                if len(b.remaining_values) < x:
                    continue
                for comb in combinations(b.remaining_values, x):
                    
                    l = []
                    for v in comb:
                        l.append(b.findCellsWithPossibleVal(v))
                    
                    hidden_found = True
                    for i in range(1, len(l)):
                        if (l[i] != l[0]):
                            hidden_found = False
                            break
                    
                    if (len(l[0]) != x):
                        hidden_found = False

                    if not hidden_found:
                        continue
                    

                    #At this point we have located a hidden pair/single/triple
                    
                    #Step A: force possible value sets to the identified cells
                    for c in l[0]:
                        c.possible_vals = set(comb)
                    
                    #Step B: remove comb values from the rest cells of the struct
                    for c in b.cells:
                        if c not in l[0]:
                            for val in comb:
                                c.possible_vals.discard(val)


    def solve_cell(self, c):
        c.value = c.possible_vals.pop()
        c.solved = True
        print("Solved Cell", c.x, c.y, ':', c.value)
        
        # Fix remaining values for row, box, column
        self.rows[c.x].remaining_values.discard(c.value)
        self.columns[c.y].remaining_values.discard(c.value)
        self.boxes[(c.x // 3) * 3 + c.y // 3].remaining_values.discard(c.value)
        
        # Filter After solved
        self.filter_solved(c)
    
    def solve_algo(self):
        if not self.nakedSingle():
            self._print()
            self.hiddenX(3)
            self.hiddenX(2)
            self.hiddenX(1)
            self.boxPointingPairs()
            self.rowColumnPointingPairs()
            
    def nakedSingle(self):
        status = False
        for i in range(self.size):
            for j in range(self.size):
                c = self.matrix[i][j]
                if len(c.possible_vals) == 1:
                    #print("Found Naked Single!")
                    self.solve_cell(c)
                    status = True
        return status

    def _print(self):
        for i in range(self.size):
            print([c.value for c in self.rows[i].cells])


def main():
    sdk = puzzle(9)
    sdk.setupPuzzle("web_sudoku_evil_1.sdk")
    stepCounter = 0
    while(sdk.calcProgress() > 0):
        print("Step", stepCounter)
        sdk.solve_algo()
        #sdk.reportPossibleValues()
        # sdk.reportRemainingValues()
        #sdk._print()
        stepCounter += 1
        if (stepCounter > 400):
            break

    print("Final Solution. Steps: ", stepCounter)
    sdk._print()


if __name__ == "__main__":
    main()
