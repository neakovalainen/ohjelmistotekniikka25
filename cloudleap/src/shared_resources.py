class LogInManager():
    def __init__(self):
        self.logged_in = False
        self.username = ""

    def login(self):
        self.logged_in = True

    def logout(self):
        self.logged_in = False

    def current_user(self, username):
        self.username = username

class GameStatus():
    def __init__(self):
        self.game_over = False
        self.game_started = False
        self.energy_level = 4

    def game_lost(self):
        self.game_over = True

    def change_game_status(self):
        if self.game_started:
            self.game_started = False
        else:
            self.game_started = True

status = LogInManager()
game_status = GameStatus()

