class LogInManager():
    """
        Sisäänkirjautumista seuraava luokka, erillisenä,
        jotta voidaan välttyä circular importilta
    """
    def __init__(self):
        self.logged_in = False
        self.username = ""
        self.display_error = False

    def login(self):
        self.logged_in = True

    def logout(self):
        self.logged_in = False

    def current_user(self, username):
        self.username = username

class GameStatus():
    """
        Luokka, joka seuraa pelin sen hetkistä statusta
    """
    def __init__(self):
        """
            Konstruktori, joka luodaan aina uuden pelin alkaessa

            Args:
            self.game_over: onko peli hävitty
            self.game_started: onko peli aloitettu (alkaa vasta kun kirjauduttu sisään)
            self.energy_level: määräytyy kerättyjen energiajuomien perusteella,
            (määrää pelin nopeuden)
        """
        self.game_over = False
        self.game_started = False
        self.energy_level = 4

    def game_lost(self):
        self.game_over = True

    def change_game_status(self):
        """
            pelistatuksen muuttaminen, esimerkiksi uloskirjautumisen ja käyttäjän 
            poistamisen yhteydessä
        """
        if self.game_started:
            self.game_started = False
        else:
            self.game_started = True

status = LogInManager()
game_status = GameStatus()
