from random import randint



# Functions (Setup)

def ask_coordinates():
    """Ask and return the coordinates of the mine the user wants to reveal"""
    print()
    x = int(input(f"Row number: \t"))
    y = int(input(f"Column number: \t"))
    print()
    return [x, y]

def create_grid(size):
    """Create and return a list of lists filled with zeros"""
    grid = []
    for row in range(size):
        grid.append([])
        for column in range(size):
            grid[row].append(0)
    return grid

def did_lose(grid, x, y):
    """Check the mine's at given location and return a bool indicating if the user did lose"""
    element = grid[x][y]
    if element == -1:
        print("GAME OVER!\n")
        return True
    return False

def did_win(grid, bombs, revealed_coordinates):
    """Check if all non-bomb mines have been revealed and return a bool indicating if the user did win"""
    if len(revealed_coordinates) == len(grid)**2 - bombs:
        print("SUCCESS!")
        print()
        return True
    return False

def fill_grid(grid, bombs):
    """Modify the grid by setting bombs at random locations and setting the mine's number"""
    bombs_coordinates = set()
    grid_filled = grid

    while len(bombs_coordinates) < bombs:
        x = randint(0, len(grid) - 1)
        y = randint(0, len(grid) - 1)
        bombs_coordinates.add((x, y))

    for row in range(len(grid)):
        for column in range(len(grid)):
            surrounding_bombs = 0
            surrounding_coordinates = [
                (row - 1, column - 1), (row - 1, column + 0), (row - 1, column + 1),
                (row + 0, column - 1), (row + 0, column + 1),
                (row + 1, column - 1), (row + 1, column + 0), (row + 1, column + 1)
            ]
            if (row, column) in bombs_coordinates:
                surrounding_bombs = -1
            else:
                for neighbor in surrounding_coordinates:
                    if neighbor in bombs_coordinates:
                        surrounding_bombs += 1
            grid_filled[row][column] = surrounding_bombs

    return grid_filled

def show_grid(grid, revealed_coordinates):
    """Present the grid to the user"""
    size = len(grid)
    style_bold = "\033[1m"
    style_end = "\033[0m"

    print("\n\t", end = "")
    for column in range(size):
        print(f"{style_bold}{column}{style_end}", end = "\t")
    print("\n\n")

    for row in range(size):
        print(f"{style_bold}{row}{style_end}", end = "\t")
        for column in range(size):
            if (row, column) in revealed_coordinates:
                element = grid[row][column]
                if element == -1:
                    print(f"\033[91m*\033[0m", end = "\t")
                elif element == 0:
                    print(f"\033[96m{element}\033[0m", end = "\t")
                else:
                    print(f"\033[93m{element}\033[0m", end = "\t")
            else:
                print("-", end = "\t")
        print("\n")
    print()

def reveal_neighbors(grid, x, y, revealed_coordinates):
    """Return the coordinate of mine neighbors to reveal based on its number of surrounding bombs"""
    revealed_coordinates = revealed_coordinates
    surrounding_coordinates = []

    revealed_coordinates.add((x, y))

    if 0 <= x < len(grid) and 0 <= y < len(grid) and grid[x][y] == 0:

        for row in range(x - 1, x + 2):
            if 0 <= row < len(grid):
                for column in range(y - 1, y + 2):
                    if 0 <= column < len(grid) and (row, column) not in revealed_coordinates:
                        surrounding_coordinates.append([row, column])

        for coordinates in surrounding_coordinates:
            revealed_coordinates = reveal_neighbors(grid, coordinates[0], coordinates[1], revealed_coordinates)

    return revealed_coordinates



# Functions (Execution)

def execute():
    restart = True
    while restart:
        start()
        restart = str(input(f"Do you want to restart? (Y/N)\t")) == "Y"

def start():
    lost = False
    won = False

    size = 20
    bombs = size * 2

    coordinates = []
    revealed_coordinates = set()

    print("=================================")
    print("\033[92m M     N     S     E     P     R \033[0m")
    print("\033[92m    I     E     W     E     E    \033[0m")
    print("=================================")

    grid = create_grid(size)
    fill_grid(grid, bombs)
    show_grid(grid, revealed_coordinates)

    while not lost and not won:
        coordinates = ask_coordinates()

        reveal_neighbors(grid, coordinates[0], coordinates[1], revealed_coordinates)
        show_grid(grid, revealed_coordinates)

        lost = did_lose(grid, coordinates[0], coordinates[1])
        won = did_win(grid, bombs, revealed_coordinates)



# Execution

execute()