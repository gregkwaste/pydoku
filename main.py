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

    def report(self):
        if not self.solved:
            print("Cell ", self.x, self.y, "Possible Values:", self.possible_vals)
        else:
            print("Cell ", self.x, self.y, "Val:", self.value)


class sdk_element:
    def __init__(self):
        self.remaining_values = set(range(1, 9 + 1))
        self.cells = []

    def filter(self):
        for c in self.cells:
            if c.solved:
                for nc in self.cells:
                    if nc != c:
                        nc.possible_vals.discard(c.value)


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
            for j in range(9):
                l.cells.append(self.matrix[i][j])
            self.rows.append(l)

        # Populate Columns
        for i in range(9):
            l = sdk_element()
            for j in range(9):
                l.cells.append(self.matrix[j][i])
            self.columns.append(l)

        # Populate Boxes
        for box_i in range(3):
            for box_j in range(3):
                # Fetch cells
                l = sdk_element()
                for i in range(3):
                    for j in range(3):
                        l.cells.append(self.matrix[box_i * 3 + i][box_j * 3 + j])
                self.boxes.append(l)

    def setupPuzzle(self, path):
        self.size = 9
        # GetData
        f = open(path)
        lines = f.readlines()
        for line_id in range(len(lines)):
            line = lines[line_id]
            values = map(int, line.rstrip('\n').split(','))
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

    def filter_solved(self):
        for b in self.boxes:
            b.filter()

        for r in self.rows:
            r.filter()

        for c in self.columns:
            c.filter()

    def reportPossibleValues(self):
        for r in self.rows:
            for c in r.cells:
                c.report()

    def reportRemainingValues(self):
        for r_id in range(self.size):
            print("Row", r_id, self.rows[r_id].remaining_values)

        for c_id in range(self.size):
            print("Col", c_id, self.columns[c_id].remaining_values)

        for b_id in range(self.size):
            print("Box", b_id, self.boxes[b_id].remaining_values)

    def hiddenX(self, x):
        structs = [self.rows, self.columns, self.boxes]
        # Apply on Every struct iteratively
        for s in structs:
            for b in s:
                if len(b.remaining_values) < x:
                    continue
                for comb in combinations(b.remaining_values, x):
                    l = []
                    for c in b.cells:
                        if c.solved:
                            continue
                        if (c.possible_vals == set(comb)) or (c.possible_vals < set(comb)):
                            l.append(c)

                    if (len(l) == x):
                        '''
                        print("found hidden ", x, comb)
                        for j in l:
                            print(j.x, j.y, j.possible_vals)
                        '''
                        # Remove vals from all other cells
                        for c in b.cells:
                            if c not in l:
                                for val in comb:
                                    c.possible_vals.discard(val)

                        # Set only one val for the found cells
                        for j in l:
                            j.possible_vals = j.possible_vals & set(comb)

    def solve_cell(self, c):
        c.value = c.possible_vals.pop()
        c.solved = True

        # Fix remaining values for row, box, column
        self.rows[c.x].remaining_values.discard(c.value)
        self.columns[c.y].remaining_values.discard(c.value)
        self.boxes[(c.x // 3) * 3 + c.y // 3].remaining_values.discard(c.value)
        # Filter After solved
        self.filter_solved()

    def solve_algo(self):
        '''
        for i in range(3, 0, -1):
            # Rest Cell Status
            print "HIDDEN" + str(i)
            self.hiddenX(i)
        '''
        self.hiddenX(3)
        self.hiddenX(2)
        self.hiddenX(1)
        self.nakedSingle()

    def nakedSingle(self):
        for i in range(self.size):
            for j in range(self.size):
                c = self.matrix[i][j]
                if len(c.possible_vals) == 1:
                    print("Solving Cell", c.x, c.y)
                    self.solve_cell(c)

    def _print(self):
        for i in range(self.size):
            print([c.value for c in self.rows[i].cells])


def main():
    sdk = puzzle(9)
    sdk.setupPuzzle("cover.sdk")
    stepCounter = 0
    while(sdk.calcProgress() > 0):
        print("Step", stepCounter)
        sdk.solve_algo()
        # sdk.reportPossibleValues()
        # sdk.reportRemainingValues()
        # sdk._print()
        stepCounter += 1
        if (stepCounter > 50):
            break

    print("Final Solution. Steps: ", stepCounter)
    sdk._print()


if __name__ == "__main__":
    main()
