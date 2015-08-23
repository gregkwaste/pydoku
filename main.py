
puzzle = []
possible_vals = []

# Soduku Class


class puzzle:

    def __init__(self):
        self.data = []
        self.size = None
        self.val_table = None
        self.state = []

    def setupPuzzle(self, path):
        # GetData
        f = open(path)
        for line in f.readlines():
            entry = [int(i) for i in line.rstrip('\n').split(',')]
            self.data.append(entry)
        f.close()

        self.size = len(self.data)
        self.val_table = set(range(self.size + 1))
        self.val_table.discard(0)

    def calcProgress(self):
        prog = 0
        for line in self.data:
            for val in line:
                if val:
                    prog += 1
        return self.size ** 2 - prog

    def readPuzzle(self):
        self.boxes = []
        self.lines = []
        self.columns = []
        self.possible_vals = []

        # Getting Data

        # Get Boxes
        for i in range(self.size // 3):
            line = []
            for j in range(self.size // 3):
                box = set()
                box_x = 3 * i
                box_y = 3 * j
                for k in range(3):
                    for l in range(3):
                        box.add(self.data[box_x + k][box_y + l])
                box.discard(0)
                line.append(box)
            self.boxes.append(line)

        # Get Lines
        for i in range(self.size):
            line = set(self.data[i])
            line.discard(0)
            self.lines.append(line)

        # Get Columns
        # Also init the possible vals
        for i in range(self.size):
            column = set()
            emptyset = []
            for j in range(self.size):
                column.add(self.data[j][i])
                emptyset.append(set())
            column.discard(0)
            self.columns.append(column)
            self.possible_vals.append(emptyset)

        for i in range(self.size):  # line index
            for j in range(self.size):  # column index
                val = self.data[i][j]
                if not val:
                    box_x = (i // 3)
                    box_y = (j // 3)
                    box = self.boxes[box_x][box_y]
                    line = self.lines[i]
                    col = self.columns[j]
                    step0 = line.union(col).union(box)
                    self.possible_vals[i][j] = self.val_table.difference(step0)
                    # step0 = step0.difference(self.val_table)
                    # print i, j, self.val_table.difference(step0)

    def hiddenSingle(self):
        tempstate = []
        # Iterate in the boxes
        for i in range(self.size // 3):
            for j in range(self.size // 3):
                # Check for uniqueness in the box
                ids = [(), (), (), (), (), (), (), (), ()]
                for k in range(9):
                    state = 0
                    foundIdx = None
                    for m in range(self.size // 3):
                        for n in range(self.size // 3):
                            candidateIdx = 3 * i + m
                            candidateIdy = 3 * j + n
                            candidateVal = self.data[candidateIdx][candidateIdy]
                            candidate = self.possible_vals[candidateIdx][candidateIdy]
                            # print candidate
                            if (not candidateVal):
                                if ((k + 1) in candidate) and state == 0:
                                    foundIdx = (candidateIdx, candidateIdy)
                                    state = 1
                                elif ((k + 1) in candidate) and state == 1:
                                    state = 2
                            if (state == 2):
                                break
                        if (state == 2):
                            break
                    if state == 1:
                        ids[k] = foundIdx

                tempstate.append(ids)

        # Update Data
        for box in tempstate:
            for j in range(len(box)):
                if box[j]:
                    # Commit Data
                    self.data[box[j][0]][box[j][1]] = j + 1

        self.state = tempstate

    def nakedSingle(self):
        for i in range(self.size):
            for j in range(self.size):
                if (not self.data[i][j] and len(self.possible_vals[i][j]) == 1):
                    # Update the Data
                    self.data[i][j] = self.possible_vals[i][j].pop()
                    # Sudoku Functions


sdk = puzzle()
sdk.setupPuzzle("easy0.sdk")

print sdk.size
progress = sdk.calcProgress()
step = 0
while progress:
    sdk.readPuzzle()
    sdk.nakedSingle()
    sdk.readPuzzle()
    sdk.hiddenSingle()
    # sdk.readPuzzle()
    # print('State ' + str(step))
    # for i in sdk.state:
    #    print i
    print('Stage' + str(step))
    for i in sdk.data:
        print i
    progress = sdk.calcProgress()
    step += 1
    print 'Progress: ', sdk.calcProgress()
