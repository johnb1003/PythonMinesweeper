import random
from models import MineCell, NumberCell, CellType, InputType

class Minesweeper:
    
    def __init__(self, dimensions=10, num_mines=10) -> None:
        self.dimensions = dimensions
        self.num_mines = num_mines
        self.mines = self.init_mines(dimensions, num_mines)
        self.board = self.init_board(dimensions, self.mines)
        self.game_active = False
        self.num_flagged = 0
        self.num_cleared_squares = 0


    def start(self):
        self.game_active = True

        while(self.game_active):
            self.print_board()
            input_string = input("Enter a turn as follows: [c for click or f for flag] [row number] [column number]:\n")
            inputs = self.validate_input(input_string)

            if inputs is None:
                continue

            input_type = inputs[0]
            row = inputs[1]
            col = inputs[2]

            cell = self.board[row][col]

            if input_type == InputType.FLAG:

                if cell.visible:
                    print("Can't flag a cell that is already visible.")
                    continue

                if cell.flagged:
                    cell.flagged = False
                    self.num_flagged -= 1
                else:
                    cell.flagged = True
                    self.num_flagged += 1

                if self.num_flagged == self.num_mines:
                    victory = True
                    for mine in self.mines:
                        if self.board[mine.x][mine.y].flagged == False:
                            victory = False
                            break

            elif input_type == InputType.CLICK:

                if cell.visible:
                    print("Can't click a cell that is already visible.")
                    continue
                elif cell.flagged:
                    print("Can't click a cell that is currently flagged. Unflag the cell then try again.")
                    continue

                if cell.type == CellType.MINE:
                    self.print_board(True)
                    print("\n\n********************\nRIP! You hit a mine!\n********************\n")
                    self.game_active = False
                    break

                elif cell.type == CellType.NUMBER:
                    cell.visible = True
                    self.num_cleared_squares += 1
                    if cell.number == 0:
                        self.expand_on_zero_click(cell)

            if self.num_flagged == self.num_mines:
                victory = True
                for mine in self.mines:
                    if self.board[mine.x][mine.y].flagged == False:
                        victory = False
                        break

                if victory and (self.num_cleared_squares == (self.dimensions ** 2) - self.num_flagged):
                    self.game_active = False
                    self.print_board(True)
                    print("\nVictory! You cleared all safe squares and flagged all of the mines.")
                    break


    def validate_input(self, input_string):
        inputs = input_string.split(" ")

        if len(inputs) != 3:
            print("Invalid input- must be 3 strings separated by a single space. Please try again.\n")
            return None

        input_type = inputs[0]
        row = inputs[1]
        col = inputs[2]

        if (input_type != "c") and (input_type != "f"):
            print("Invalid input type- must be either 'c' or 'f'. Please try again.\n")
            return None
        elif not (row.isdigit() and self.is_valid_index(int(row))):
            print("Invalid row- must be an integer within the dimesnions of the gameboard. Please try again.\n")
            return None
        elif not (col.isdigit() and self.is_valid_index(int(col))):
            print("Invalid col- must be an integer within the dimesnions of the gameboard. Please try again.\n")
            return None


        return (InputType.CLICK if input_type == "c" else InputType.FLAG, int(row), int(col))


    def expand_on_zero_click(self, cell):
        queue = []
        visited = set()

        queue.insert(0, cell)

        while len(queue) > 0:
            cell = queue.pop()
            visited.add((cell.x, cell.y))
            if cell.number == 0:
                # Explore neighbors
                for i in range(-1, 2):
                    row = cell.x + i
                    if(self.is_valid_index(row)):
                        for j in range(-1, 2):
                            col = cell.y + j
                            if row == cell.x and col == cell.y: continue
                            if(self.is_valid_index(col)):
                                neighbor = self.board[row][col]
                                neighbor_tuple = (neighbor.x, neighbor.y)
                                if(neighbor.visible == False and neighbor_tuple not in visited):
                                    visited.add(neighbor_tuple)
                                    neighbor.visible = True
                                    self.num_cleared_squares += 1
                                    if neighbor.number == 0:
                                        queue.insert(0, neighbor)
        
    
    def init_mines(self, dimensions: int, num_mines: int) -> list:
        mines = []
        while(len(mines) < num_mines):
            row = random.randrange(0, dimensions)
            col = random.randrange(0, dimensions)
            mine = MineCell(row, col)
            if(mine in mines):
                continue
            mines.append(mine)

        return mines


    def init_board(self, dimensions, mines) -> list:
        board = []

        # Init cells
        for i in range(0, dimensions):
            row = []
            for j in range(0, dimensions):
                row.append(NumberCell(i, j, 0))
            board.append(row)

        # Add mines to board and increment adjacent numbers
        for mine in mines:
            board[mine.x][mine.y] = mine
            board = self.increment_adjacent_nums(board, mine)

        return board


    def increment_adjacent_nums(self, board: list, mine: MineCell) -> list:
        for i in range(-1, 2):
            row = mine.x + i
            if(self.is_valid_index(row)):
                for j in range(-1, 2):
                    col = mine.y + j
                    if row == mine.x and col == mine.y: continue
                    if(self.is_valid_index(col)):
                        cell = board[row][col]
                        if(cell.type == CellType.NUMBER):
                            cell.number += 1
        
        return board


    def is_valid_index(self, index) -> bool:
        return index >= 0 and index < self.dimensions

    
    def print_board(self, print_all=False):
        board_string = "\n\n\t|\t"

        for i in range(0, self.dimensions):
            board_string += str(i) + "\t"

        board_string += "\n"

        for i in range(0, self.dimensions+2):
            board_string += "__\t"

        board_string += "\n\n"

        for i in range(0, self.dimensions):
            board_string += str(i) + "\t|\t"
            for j in range(0, self.dimensions):
                cell = self.board[i][j]
                if (not print_all) and (not cell.visible):
                    board_string += "F\t" if cell.flagged else "-\t"
                else:
                    board_string += str(cell.number) + "\t" if cell.type == CellType.NUMBER else "X\t"
            board_string += "\n\n"
        
        print(board_string)


game = Minesweeper(10, 10)
game.start()
