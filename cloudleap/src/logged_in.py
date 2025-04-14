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


status = LogInManager()