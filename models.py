from enum import Enum

class InputType(Enum):
    CLICK = 1
    FLAG = 2

class CellType(Enum):
    MINE = 1
    NUMBER = 2

class Cell:

    def __init__(self, x, y, type) -> None:
        self.x = x
        self.y = y
        self.type = type
        self.flagged = False
        self.visible = False


    def __eq__(self, other: object) -> bool:
        if isinstance(other, Cell):
            return self.x == other.x and self.y == other.y
        return False

    def __repr__(self) -> str:
        return repr((self.x, self.y, self.type))


class MineCell(Cell):

    def __init__(self, x, y) -> None:
        super().__init__(x, y, CellType.MINE)


class NumberCell(Cell):

    def __init__(self, x, y, number) -> None:
        super().__init__(x, y, CellType.NUMBER)
        self.number = number