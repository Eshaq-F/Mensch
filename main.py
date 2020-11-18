import tkinter.messagebox
import logging
from tkinter import ttk
from time import sleep
from random import choice
from PIL import ImageTk, Image
from setting import *
from board import *


class Piece:

    def __init__(self, master, x, y, color, path_list, flag):
        self.canvas = master
        self.curr_x = x
        self.curr_y = y
        self.home_x = x
        self.home_y = y
        self.color = color
        self.curr_index = -1
        self.coin = ImageTk.PhotoImage(Image.open('Images/{}.png'.format(color)))
        self.img = self.canvas.create_image(x, y, anchor=tk.NW, image=self.coin)
        self.canvas.tag_bind(self.img, '<1>', self.move)
        self.disable = True
        self.path_list = path_list
        self.player = None
        self.flag = flag
        self.win = 0
        self.pad_x = 0

    def move(self, event):

        if self.disable:
            return

        roll = Dice.roll
        if len(roll) == 0:
            return

        if roll[-1] == 6:
            tkinter.messagebox.showerror('Error', 'You got 6, So please Roll Again.')
            return

        if len(roll) != 0:
            n = len(self.path_list)
            max_moves = n - self.curr_index - 1
            if max_moves < roll[0]:
                return

        check = (False, 0, 0)
        congrats = False
        if self.at_home():
            if 6 in roll:
                check = self.can_attack(0)
                self.canvas.coords(self.img, self.path_list[0][0] + 4 + self.pad_x, self.path_list[0][1] + 4)
                self.curr_x = self.path_list[0][0]
                self.curr_y = self.path_list[0][1]
                self.curr_index = 0
                Dice.remove_by_index(6)
        else:
            check = self.can_attack(self.curr_index + roll[0])
            for i in range(roll[0] - 1):
                self.curr_index += 1
                self.canvas.coords(self.img, self.path_list[self.curr_index][0] + 4,
                                   self.path_list[self.curr_index][1] + 4)
                self.curr_x = self.path_list[self.curr_index][0]
                self.curr_y = self.path_list[self.curr_index][1]
                self.canvas.update()
                sleep(0.05)

            self.curr_index += 1
            self.canvas.coords(self.img, self.path_list[self.curr_index][0] + 4 + self.pad_x,
                               self.path_list[self.curr_index][1] + 4)
            self.curr_x = self.path_list[self.curr_index][0]
            self.curr_y = self.path_list[self.curr_index][1]
            if check[0]:
                colors[check[1]][check[2]].go_home()

            self.canvas.update()
            sleep(0.05)
            Dice.remove()
            if self.curr_index == len(self.path_list) - 1:
                self.win = 1
                tkinter.messagebox.showinfo('INFO', '** Congratulations **\nPlease Roll Dice Again!')
                winners.append(self.player)
                congrats = self.congratulations()

            if check[0]:
                tkinter.messagebox.showinfo('INFO', 'You killed another coin! Now you get another chance.')
                congrats = self.congratulations()

        if self.player_win():
            tkinter.messagebox.showinfo('INFO', '{} Wins'.format(self.color.title()))
            position.append(self.player.title())
            Dice.roll = []
            Dice.set(self.flag)

        if self.game_over():
            root.quit()

        if not check[0] and not congrats:
            if len(Dice.roll):
                Dice.check_move_possibility()
            self.next_turn()

    def congratulations(self):
        Dice.update_state()
        Dice.set(self.flag - 1)

        return True

    def change_state(self, flag):
        if flag == self.flag:
            self.disable = False
        else:
            self.disable = True

    def at_home(self):
        return self.curr_x == self.home_x and self.curr_y == self.home_y

    def check_home(self):
        count = 0
        for piece in colors[self.flag]:
            if piece.at_home():
                count += 1

        return count

    def player_win(self):
        reached = 0
        for piece in colors[self.flag]:
            if piece.win:
                reached += 1

        return reached == 4

    def game_over(self):
        color_reached = 0

        for i in range(len(colors)):
            game = 0
            for color in colors[i]:
                if color.win:
                    game += 1
            if game == len(colors):
                color_reached += 1

        if color_reached == 3:
            tkinter.messagebox.showinfo('Game Over', '\n\n1. {}\n\n2. {}\n\n3. {}'.format(*position))
        else:
            return False
        return True

    def can_attack(self, idx):
        max_pad = 0
        count_a = 0
        x = self.path_list[idx][0]
        y = self.path_list[idx][1]
        for i in range(len(colors)):
            for j in range(4):
                if colors[i][j].curr_x == x and colors[i][j].curr_y == y:
                    if colors[i][j].pad_x > max_pad:
                        max_pad = colors[i][j].pad_x
                    count_a += 1

        if not self.path_list[idx][2]:
            for i in range(len(colors)):
                count = 0
                jdx = 0
                for j in range(4):
                    if (colors[i][j].curr_x == x and colors[i][j].curr_y == y
                            and colors[i][j].color != self.color):
                        count += 1
                        jdx = j

                if count != 0 and count != 2:
                    self.pad_x = max_pad + 4
                    return True, i, jdx

        if count_a != 0:
            self.pad_x = max_pad + 4
        else:
            self.pad_x = 0
        return False, 0, 0

    def go_home(self):
        self.canvas.coords(self.img, self.home_x, self.home_y)
        self.curr_x = self.home_x
        self.curr_y = self.home_y
        self.curr_index = -1

    def next_turn(self):
        if len(Dice.roll) == 0:
            Dice.set(self.flag)

    def set_player_name(self, player):
        self.player = player


class Dice:
    chance = 0
    roll = []
    append_state = False

    @classmethod
    def rolling(cls):
        result()
        num = choice(range(1, 9))
        if num > 6:
            num = 6

        if len(cls.roll) == 0 or cls.roll[-1] == 6 or cls.append_state:
            cls.roll.append(num)
            cls.append_state = False

        tk.Label(text='{}'.format(' + '.join([str(x) for x in cls.roll])), width=8, height=2,
                 font=("Helvetica", "32"), bg=Color.WHITE).place(x=20, y=435)

    @classmethod
    def start(cls):
        Dice.rolling()
        if cls.roll.count(6) >= 3:
            if [cls.roll[-1], cls.roll[-2], cls.roll[-3]] == [6, 6, 6]:
                for i in range(3):
                    Dice.remove_by_index(6)

            if not cls.roll:
                Dice.update_panel()
                return
        Dice.check_move_possibility()

    @classmethod
    def update_panel(cls):
        root.update()
        sleep(0.5)
        Dice.set(cls.chance)
        cls.roll = []

    @classmethod
    def set(cls, flag):
        flag += 1
        cls.chance = flag
        if flag == len(colors):
            cls.chance = flag = 0
        if colors[cls.chance][0].player_win():
            Dice.set(cls.chance)
        else:
            for i in range(len(colors)):
                for j in range(4):
                    colors[i][j].change_state(flag)

            tk.Label(text=f"{turn[flag]}\'s Turn", width=15, height=3, bg=Color.WHITE,
                     font=("Helvetica", 18, "bold")).place(x=0, y=285)

            tk.Label(text='ROLL PLEASE', width=15, height=3, bg=Color.WHITE,
                     font=("Helvetica", "17")).place(x=20, y=445)

    @classmethod
    def remove(cls):
        Dice.roll.pop(0)

    @classmethod
    def remove_by_index(cls, ex):
        del cls.roll[cls.roll.index(ex)]

    @classmethod
    def update_state(cls):
        cls.append_state = True

    @classmethod
    def check_move_possibility(cls):
        check_1 = 0
        check_2 = 0
        for piece in colors[cls.chance]:
            if piece.at_home():
                check_1 += 1
            else:
                max_moves = len(piece.path_list) - piece.curr_index - 1
                if max_moves < cls.roll[0]:
                    check_2 += 1

        if 6 not in cls.roll:
            if check_1 == 4 or check_1 + check_2 == 4:
                Dice.update_panel()
        else:
            if check_2 == 4:
                Dice.update_panel()


def armed(x, y, color, path_list, flag):
    container = []
    for i in range(2):
        test = Piece(mensch.get_canvas(), x, y + i * 2 * Size.PATH_SIZE, color=color, path_list=path_list, flag=flag)
        container.append(test)
    for i in range(2):
        test = Piece(mensch.get_canvas(), x + 2 * Size.PATH_SIZE, y + i * 2 * Size.PATH_SIZE, color=color,
                     path_list=path_list, flag=flag)
        container.append(test)

    return container


def starting_game():
    if len(players) >= 2:
        for i in range(len(players)):
            if players[i].user:
                turn.append(players[i].user)
        for i in range(len(turn)):
            for j in range(4):
                colors[i][j].set_player_name(turn[i])

        tk.Button(text='ROLL', bg='gray', command=Dice.start, width=18, height=2).place(x=55, y=570)

        tk.Label(mensch.get_frame(), text=f'Let\'s start with {turn[0]}', width=18, height=3,
                 bg=Color.WHITE, font=("Helvetica", 15, "bold")).place(x=0, y=285)

        for num in range(len(players)):
            tk.Label(text=f'{num + 1}.{players[num].user}', font=("Helvetica", 18, "bold"),
                     fg=players[num].color, bg=Color.WHITE).place(x=10, y=50 + num * 40)

        return True

    else:
        tk.messagebox.showerror("Error", ' Game will start with at least 2 players!!! ')
        return False


def close_root():
    if tkinter.messagebox.askokcancel("Quit", "Do you want to quit the game?"):
        root.destroy()


def main():
    global final_result
    global winners
    global players
    global turn
    global position
    global colors
    global color_list
    color_list = ['Green', 'Blue', 'Yellow', 'Red']
    final_result = list()
    winners = list()
    players = list()
    turn = list()
    position = list()
    colors = list()


def set_state():
    for i in range(len(players)):
        for j in range(4):
            colors[i][j].change_state(0)


def main_loop():
    root.protocol("WM_DELETE_WINDOW", close_root)
    root.configure(bg=Color.BG)
    MenuBar(root)
    root.mainloop()


class Player:
    def __init__(self, username, password, color):
        self.user = username
        self.pas = password
        self.color = color


def log_result():
    logging.basicConfig(filename='mensch_result.log', format='%(asctime)s %(message)s', level=logging.INFO)
    logging.info(" {}".format(' '.join(final_result)))


def result():
    for i in range(len(players)):
        x = 0
        for j in range(len(winners)):
            if players[i].user == winners[j]:
                x += 1
        if x == 4:
            final_result.append(players[i].user)

    if len(final_result) == len(players):
        if len(final_result) == 2:
            tk.messagebox.showinfo('Results', Text.FINAL_RESULT1.format(final_result[0], final_result[1]))
            log_result()
            root.quit()
        elif len(final_result) == 3:
            tk.messagebox.showinfo('Results',
                                   Text.FINAL_RESULT2.format(final_result[0], final_result[1], final_result[2]))
            log_result()
            root.quit()
        elif len(final_result) == 4:
            tk.messagebox.showinfo('Results',
                                   Text.FINAL_RESULT3.format(final_result[0], final_result[1], final_result[2],
                                                             final_result[3]))
            log_result()
            root.quit()


class MenuBar(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master

        self.init_window()

    def init_window(self):
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        game = tk.Menu(menu, tearoff=False)

        def start_game():
            if starting_game():
                game.entryconfig(0, state=tk.DISABLED)
                game.entryconfig(1, state=tk.DISABLED)

        def new_game():
            global root
            global mensch
            root.destroy()
            main()
            set_state()
            root = tk.Tk()
            root.geometry('1000x660')
            root.title('Mensch')
            root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='Images/icons/dice-none.png'))
            mensch = MenschBoard(root)
            mensch.create()
            MenuBar(root)
            main_loop()

        game.add_command(label='Add Player', command=self.login_page)
        game.add_command(label='Start game', command=start_game)
        game.add_command(label='New game', command=new_game)
        game.add_separator()
        game.add_command(label='Exit', command=self.master.quit)

        menu.add_cascade(label=" Game ", menu=game)

        helping = tk.Menu(menu, tearoff=False)
        helping.add_command(label='How to play ?!', command=self.how_to_play)
        menu.add_cascade(label=" Help", menu=helping)

    @staticmethod
    def login_page():
        login = tk.Tk()
        login.wm_title("Login Page")
        login.config(bg=Color.BG)
        login.geometry('350x300')
        tk.Label(login, text='Login', font=("Times", 23, "bold"), bg=Color.BG).place(x=140, y=5)
        tk.Label(login, text='Username :', bg=Color.BG, fg=Color.WHITE,
                 font=("Helvetica", 10, "bold")).place(x=40, y=80)
        tk.Label(login, text='Password :', bg=Color.BG, fg=Color.WHITE,
                 font=("Helvetica", 10, "bold")).place(x=40, y=120)
        tk.Label(login, text='Color :', bg=Color.BG, fg=Color.WHITE,
                 font=("Helvetica", 10, "bold")).place(x=40, y=160)
        user_text = tk.Entry(login, width=23)
        user_text.focus_set()
        user_text.place(x=120, y=80)
        pass_text = tk.Entry(login, width=23, show='*')
        pass_text.place(x=120, y=120)
        pass_text.focus_set()
        color_choose = ttk.Combobox(login, values=color_list)
        color_choose.place(x=120, y=160)
        color_choose.focus_set()

        def add_player():
            if user_text.get() in Members.dic.keys() and Members.dic[user_text.get()] == pass_text.get():
                for gamer in players:
                    if gamer.user == user_text.get():
                        tkinter.messagebox.showerror('Error', f'" {gamer.user} " was added before!')
                        login.destroy()
                if color_choose.get() == 'Green':
                    colors.append(armed(2.1 * Size.PATH_SIZE, 2.1 * Size.PATH_SIZE, color='green',
                                        path_list=path.green_path, flag=len(colors)))
                    color_list.remove('Green') and turn.append(color_choose.get())
                    players.append(Player(user_text.get(), pass_text.get(), color_choose.get()))
                    login.destroy()

                elif color_choose.get() == 'Red':
                    colors.append(armed(2.1 * Size.PATH_SIZE, 11.1 * Size.PATH_SIZE, color='red',
                                        path_list=path.red_path, flag=len(colors)))
                    color_list.remove('Red') and turn.append(color_choose.get())
                    players.append(Player(user_text.get(), pass_text.get(), color_choose.get()))
                    login.destroy()

                elif color_choose.get() == 'Blue':
                    colors.append(armed(11.1 * Size.PATH_SIZE, 11.1 * Size.PATH_SIZE, color='blue',
                                        path_list=path.blue_path, flag=len(colors)))
                    color_list.remove('Blue') and turn.append(color_choose.get())
                    players.append(Player(user_text.get(), pass_text.get(), color_choose.get()))
                    login.destroy()

                elif color_choose.get() == 'Yellow':
                    colors.append(armed(11.1 * Size.PATH_SIZE, 2.1 * Size.PATH_SIZE, color='yellow',
                                        path_list=path.yellow_path, flag=len(colors)))
                    color_list.remove('Yellow') and turn.append(color_choose.get())
                    players.append(Player(user_text.get(), pass_text.get(), color_choose.get()))
                    login.destroy()

            else:
                tkinter.messagebox.showerror('Error', 'Wrong username or password!')
                login.destroy()

        tk.Button(login, width=10, text='Login', bg='white', command=add_player).place(x=180, y=210)
        tk.Button(login, width=10, text='Cancel', bg='white', command=login.destroy).place(x=180, y=240)

    @staticmethod
    def how_to_play():
        tk.messagebox.showinfo('How to play?!', Text.HTP)


if __name__ == '__main__':
    main()
    root = tk.Tk()
    root.geometry('1000x660')
    root.title('Mensch')
    root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='Images/icons/dice-none.png'))
    mensch = MenschBoard(root)
    mensch.create()
    main_loop()
