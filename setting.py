class Color:
    GREEN = '#00cc00'
    RED = '#F71313'
    YELLOW = '#FFFF00'
    BLUE = '#3575EC'
    DEFAULT = '#b5b5b5'
    WHITE = '#fff'


class Board:
    SQUARE_SIZE = 40
    BOARD_WIDTH = 640
    BOARD_HEIGHT = 620
    POINTS = [(0, 0), (0, 1), (1, 0), (1, 1)]
    POSITIVE_V = [(8, 1), (6, 13)]
    POSITIVE_H = [(1, 6), (13, 8)]


class Members:
    dic = dict()
    with open('members.txt') as f:
        for i in f.readlines():
            user, password = i.split()
            dic[str(user)] = str(password)


class Text:
    MADE_BY = 'Made by: Eshaq Farrokhi'
    HTP = 'Welcome to our Mensch(Ludo) game!\n' \
          'To start the game first, you should login by press "Add Player" button in menu > Game.' \
          'After adding at least 2 members; you can press "Start game" to start the game :)\n' \
          'In the left panel you can see the players ,turn and dice number. ' \
          'You can roll a dice in your turn and go on until treading all the home paths and jump into the maze;' \
          'in this way you should be careful! Because the other pieces can attack you.' \
          'Each player that has the most jumped piece will win, so move on.'


class Path:

    def __init__(self):

        self.green_path = []
        self.red_path = []
        self.blue_path = []
        self.yellow_path = []
        self.gx = None
        self.gy = None
        self.ry = None
        self.by = None
        self.count = None

    def update_coordinates(self, gx, gy, ry, by, count):

        self.gx = gx
        self.gy = gy
        self.ry = ry
        self.by = by
        self.count = count

    def start_populating(self):

        # 1
        self.update_coordinates(60, 260, 540, 340, 5)
        self.direct(pow_index=0, direction='right')
        # 2
        self.update_coordinates(260, 220, 340, 380, 5)
        self.direct(pow_index=3, direction='up')
        # 3
        self.update_coordinates(260, 20, 340, 580, 3)
        self.direct(direction='right')
        # 4
        self.update_coordinates(340, 60, 260, 540, 5)
        self.direct(pow_index=0, direction='down')
        # 5
        self.update_coordinates(380, 260, 220, 340, 5)
        self.direct(pow_index=3, direction='right')
        # 6
        self.update_coordinates(580, 260, 20, 340, 3)
        self.direct(direction='down')
        # 7
        self.update_coordinates(540, 340, 60, 260, 5)
        self.direct(pow_index=0, direction='left')
        # 8
        self.update_coordinates(340, 380, 260, 220, 5)
        self.direct(pow_index=3, direction='down')
        # 9
        self.update_coordinates(340, 580, 260, 20, 3)
        self.direct(direction='left')
        # 10
        self.update_coordinates(260, 540, 340, 60, 5)
        self.direct(pow_index=0, direction='up')
        # 11
        self.update_coordinates(220, 340, 380, 260, 6)
        self.direct(pow_index=3, direction='left')
        # 12
        self.update_coordinates(20, 300, 580, 300, 7)
        self.direct(direction='right')

    def direct_horizontal(self, k, pow_index=-1):

        for i in range(self.count):
            if i == pow_index:
                p = 1
            else:
                p = 0
            self.green_path.append((self.gx + k * i * Board.SQUARE_SIZE, self.gy, p))
            self.red_path.append((self.gy, self.ry - k * i * Board.SQUARE_SIZE, p))
            self.blue_path.append((self.ry - k * i * Board.SQUARE_SIZE, self.by, p))
            self.yellow_path.append((self.by, self.gx + k * i * Board.SQUARE_SIZE, p))

    def direct_vertical(self, k, pow_index=-1):

        for i in range(self.count):
            if i == pow_index:
                p = 1
            else:
                p = 0
            self.green_path.append((self.gx, self.gy - k * i * Board.SQUARE_SIZE, p))
            self.red_path.append((self.gy - k * i * Board.SQUARE_SIZE, self.ry, p))
            self.blue_path.append((self.ry, self.by + k * i * Board.SQUARE_SIZE, p))
            self.yellow_path.append((self.by + k * i * Board.SQUARE_SIZE, self.gx, p))

    def direct(self, direction, pow_index=-1):
        if direction == 'right':
            self.direct_horizontal(1, pow_index=pow_index)
        elif direction == 'left':
            self.direct_horizontal(-1, pow_index=pow_index)
        elif direction == 'down':
            self.direct_vertical(-1, pow_index=pow_index)
        else:
            self.direct_vertical(1, pow_index=pow_index)


path = Path()
path.start_populating()
