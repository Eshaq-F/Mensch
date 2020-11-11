from random import choice

colors = []


class Piece:

    def __init__(self, master, x, y, color, path_list, flag):
        self.canvas = master
        self.x = x
        self.y = y
        self.home_x = x
        self.home_y = y
        self.color = color
        self.disable = True
        self.path_list = path_list
        self.flag = flag
        self.win = 0

    def move(self):

        if self.disable:
            return None

        roll = Dice.roll
        if len(roll) == 0:
            return None

        if roll[-1] == 6:
            raise NotImplementedError

        if len(roll) != 0:
            n = len(self.path_list)
            max_moves = n - self.index - 1
            if max_moves < roll[0]:
                return

        check = (False, 0, 0)
        congrats = False
        if self.is_at_home():
            if 6 in roll:
                check = self.can_attack(0)
                self.x = self.path_list[0][0]
                self.y = self.path_list[0][1]
                self.index = 0
                Dice.remove(6)
        else:
            check = self.can_attack(self.index + roll[0])
            for i in range(roll[0] - 1):
                self.index += 1
                self.curr_x = self.path_list[self.index][0]
                self.curr_y = self.path_list[self.index][1]
                self.canvas.update()

            self.index += 1
            self.x = self.path_list[self.index][0]
            self.y = self.path_list[self.index][1]

        if self.is_player_won():
            Dice.roll = []

        if not check[0] and not congrats:
            pass

    def congratulations(self):
        Dice.update_state()
        ...

        return True

    def change_state(self, flag):
        if flag == self.flag:
            self.disable = False
        else:
            self.disable = True

    def is_at_home(self):
        return self.x == self.home_x and self.y == self.home_y

    def check_home(self):
        count = 0
        for mohre in colors[self.flag]:
            if mohre.is_at_home():
                count += 1

        return count

    def is_player_won(self):
        reached = 0

        return reached == 4

    def gameover(self):
        pass

    def can_attack(self, idx):
        pass

    def goto_home(self):
        self.canvas.coords(self.home_x, self.home_y)
        self.x = self.home_x
        self.y = self.home_y
        self.index = -1

    def playername(self, player):
        self.player = player


class Dice:
    chance = 0
    roll = []
    append_state = False

    @classmethod
    def rolling(cls):
        temp = choice(range(1, 9))
        if temp > 6:
            temp = 6

        if len(cls.roll) == 0 or cls.roll[-1] == 6 or cls.append_state:
            cls.roll.append(temp)
            cls.append_state = False

    @classmethod
    def start(cls):
        Dice.rolling()
        if cls.roll.count(6) >= 3:
            if [cls.roll[-1], cls.roll[-2], cls.roll[-3]] == [6, 6, 6]:
                for i in range(3):
                    Dice.remove(6)

    @classmethod
    def remove(cls, ex):
        del cls.roll[cls.roll.index(ex)]

    @classmethod
    def update_state(cls):
        cls.append_state = True

    @classmethod
    def check_move(cls):
        pass
