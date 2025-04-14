class LogInManager():
    def __init__(self):
        self.logging_in = True
        self.username = ""

    def login(self):
        self.logging_in = False

    def logout(self):
        self.logging_in = True

    def current_user(self, username):
        self.username = username


status = LogInManager()