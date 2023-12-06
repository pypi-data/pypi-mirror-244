class Tile:
    def __init__(self, position):
        self._status = None
        self.position = position

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if self._status is None:
            self._status = value

    def __repr__(self):
        return f"{self._status if self._status is not None else '-'}"


class Grid:
    def __init__(self):
        self.tiles = self._creator()
        self.choice = "O"
        self.winlose = WinLose()
        self.winner = str()
        self.draw = False
        self.x = 0
        self.o = 0
        self.d = 0

    def restart(self):
        if self.winner or self.draw:
            self.tiles = self._creator()
            if self.winner:
                self.choice = "X" if self.winner == "O" else "O"
            self.winner = ""
            self.draw = False
            
    @staticmethod
    def _creator():
        tiles = []
        for x in range(3):
            temp = []
            for y in range(3):
                temp.append(Tile((x, y)))
            tiles.append(temp)
        return tiles

    def insert(self, position):
        try:
            self.swap_choice(position)
            self.tiles[position[0]][position[1]].status = self.choice

            if self.winlose.check_result(self.tiles):
                self.winner = self.choice
                self.add_win()
            elif all([obj.status for tile in self.tiles for obj in tile]):
                self.add_draw()

        except IndexError:
            print("Position out of range! Please put a right Position!")

    def swap_choice(self, position):
        if self.tiles[position[0]][position[1]].status is None:
            self.choice = "X" if self.choice == "O" else "O"

    def add_win(self):
        if self.choice == "X":
            self.x += 1
        else:
            self.o += 1

    def add_draw(self):
        self.draw = True
        self.d += 1


class WinLose:
    @staticmethod
    def check_rows(tiles):
        for row in tiles:
            row_status = [obj.status for obj in row]
            if all(row_status) and len(set(row_status)) == 1:
                return True
        return False

    def check_columns(self, tiles):
        columns = list(zip(*tiles))
        return self.check_rows(columns)

    @staticmethod
    def check_diagonals(tiles):
        left_diagonal = set([tiles[i][i].status for i in range(len(tiles))])
        if all(left_diagonal) and len(left_diagonal) == 1:
            return True

        right_diagonal = set([tiles[i][len(tiles)-1-i].status for i in range(len(tiles))])
        if all(right_diagonal) and len(right_diagonal) == 1:
            return True
        return False

    def check_result(self, tiles):
        if self.check_rows(tiles) or self.check_columns(tiles) or self.check_diagonals(tiles):
            return True
        return False
