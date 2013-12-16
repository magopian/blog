WORLD = [  # False = dead cell, True = live cell
    [False, False, False, False, False],
    [False, True, False, True, False],
    [False, True, True, False, False],
    [False, False, True, True, False],
    [False, False, False, False, False],
]


def evolve_world(world):
    new_world = [line[:] for line in world]  # copy the current world
    for x, line in enumerate(new_world):
        for y, cell in enumerate(line):
            new_world[x][y] = evolve_cell(new_world[x][y],
                                          num_alive_neighbours(world, x, y))
    return new_world


def evolve_cell(cell_alive, num_neighbours):
    return ((cell_alive and num_neighbours in [2, 3]) or
            (not cell_alive and num_neighbours == 3))


def num_alive_neighbours(world, x, y):
    neighbours_rel_pos = [  # relative position of all possible neighbours
        (-1, -1), (-1, 0), (-1, 1),  # upper row
        (0, -1), (0, 1),  # same row
        (1, -1), (1, 0), (1, 1)]  # lower row

    count = 0
    for neigh_pos_x, neigh_pos_y in neighbours_rel_pos:
        pos_x = x + neigh_pos_x
        pos_y = y + neigh_pos_y
        if (pos_x >= 0 and pos_x < len(world) and
                pos_y >= 0 and pos_y < len(world[0]) and
                world[pos_x][pos_y]):
            count += 1
    return count


def world_tostring(world):
    return "\n".join("".join("O" if alive else " " for alive in line)
                     for line in world)
