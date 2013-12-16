WORLD = [  # False = dead cell, True = live cell
    [False, False, False, False, False],
    [False, True, False, True, False],
    [False, True, True, False, False],
    [False, False, True, True, False],
    [False, False, False, False, False],
]


class Cell:

    def __init__(self, alive=False):
        self.neighbours = []
        self.alive = alive

    def add_neighbour(self, cell):
        self.neighbours.append(cell)

    def get_num_live_neighbours(self):
        return len([cell for cell in self.neighbours if cell.alive])

    def mutate(self):
        live_neighbours = self.get_num_live_neighbours()
        survives = self.alive and live_neighbours in [2, 3]
        born = not self.alive and live_neighbours == 3
        self.next_state = born or survives
        return self.next_state

    def step(self):
        self.alive = self.next_state

    def __str__(self):
        return 'O' if self.alive else ' '


class World:

    neighbours_rel_pos = [  # relative position of all possible neighbours
        (-1, -1), (-1, 0), (-1, 1),  # upper row
        (0, -1), (0, 1),  # same row
        (1, -1), (1, 0), (1, 1)]  # lower row

    def __init__(self, board):
        self.board = [[Cell(alive) for alive in line]
                      for line in board]

        # initialize neighbours for all cells
        for x, line in enumerate(self.board):
            for y, cell in enumerate(line):
                for neigh_pos_x, neigh_pos_y in self.neighbours_rel_pos:
                    pos_x = x + neigh_pos_x
                    pos_y = y + neigh_pos_y
                    if (pos_x >= 0 and pos_x < len(self.board) and
                            pos_y >= 0 and pos_y < len(self.board[0])):
                        cell.add_neighbour(self.board[pos_x][pos_y])

    def step(self):
        for line in self.board:  # compute next state
            for cell in line:
                cell.mutate()
        for line in self.board:  # apply
            for cell in line:
                cell.step()

    def __str__(self):
        return "\n".join("".join(str(cell) for cell in line)
                         for line in self.board)
