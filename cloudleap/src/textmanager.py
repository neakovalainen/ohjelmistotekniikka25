import pygame_textinput
import pygame
import pygame_widgets
from pygame_widgets.button import Button
from shared_resources import status

FONT = "src/assets/unifont-16.0.02.otf"

class TextManager:
    def __init__(self, energy, screen, user_data):
        self.textmanager = pygame_textinput.TextInputManager()
        self.textinput = pygame_textinput.TextInputVisualizer(manager=self.textmanager)
        self.textinput.cursor_width = 1
        self.textinput.cursor_blink_interval = 500
        self.textinput.font_object = pygame.font.Font(FONT, 15)
        self.font = pygame.font.Font(FONT, 30)
        self.energy = energy
        #self.username = ""
        self.screen = screen
        self.user_data = user_data
        #self.logged_in = status.logged_in
        self.logout_button = Button(
            win=self.screen,
            x=1000,
            y=30,
            width=75,
            height=25,
            text='log out',
            fontSize=12,
            inactiveColour=(211, 211, 211),
            hoverColour=(200, 200, 200),
            radius=10,
            onClick=lambda: self.logout() # pylint: disable=unnecessary-lambda
        )
        self.delete_button = Button(
            win=self.screen,
            x=1080,
            y=30,
            width=75,
            height=25,
            text='delete user',
            fontSize=12,
            inactiveColour=(211, 211, 211),
            hoverColour=(200, 200, 200),
            radius=10,
            onClick=lambda: self.delete_user() # pylint: disable=unnecessary-lambda
        )

    def get_users(self):
        lil_font = pygame.font.Font(FONT, 15)
        y_coordinate = 75
        for _, score, user in self.user_data.get_all_scores():
            user_rendered = lil_font.render(str(user), True, ("Black"))
            score_rendered = lil_font.render(str(score), True, ("black"))
            self.screen.blit(user_rendered, (1000, y_coordinate))
            self.screen.blit(score_rendered,(1100, y_coordinate))
            y_coordinate += 15

    def text_objects(self):
        lil_font = pygame.font.Font(FONT, 15)
        text = self.font.render("current energy:" + str(self.energy.points), True, ("black"))
        start = self.font.render("start game by pressing space (づ ◕‿◕ )づ", True, ("black"))
        guide1 = lil_font.render("write username below and press enter", True, ("black"))
        guide2 = lil_font.render("if user doesn't exist,", True, ("black"))
        guide3 = lil_font.render("it will be created automatically:", True, ("black"))
        logged_in = lil_font.render("logged in as: " + status.username, True, ("black"))
        rules1 = lil_font.render("try to get as much energy as you can", True, ("black"))
        rules2 = lil_font.render("to catch up on that uni work!!", True, ("black"))
        rules3 = lil_font.render("if 3 schoolworks catch you, or your energy goes below 0", True, ("black")) # pylint: disable=line-too-long
        rules4 = lil_font.render("you missed your deadlines or fell asleep, so you lose", True, ("black")) # pylint: disable=line-too-long
        return text, start, guide1, guide2, guide3, logged_in, rules1, rules2, rules3, rules4

    def draw_texts(self):
        text, start, guide1, guide2, guide3, logged_in, rules1, rules2, rules3, rules4 = self.text_objects() # pylint: disable=line-too-long
        self.screen.blit(text, (20, 20))
        if not status.logged_in:
            self.screen.blit(guide1, (10, 100))
            self.screen.blit(guide2, (10, 120))
            self.screen.blit(guide3, (10, 140))
            self.screen.blit(rules1, (426, 180))
            self.screen.blit(rules2, (426, 200))
            self.screen.blit(rules3, (426, 220))
            self.screen.blit(rules4, (426, 240))
        if status.logged_in:
            self.screen.blit(start, (300, 20))
        self.screen.blit(logged_in, (1000, 10))
        self.get_users()

    def button_update(self, events):
        pygame_widgets.update(events)

    def logout(self):
        status.logout()
        status.current_user("")
        self.textinput.value = ""

    def delete_user(self):
        self.user_data.delete_user(status.username)
        self.user_data.delete_score(status.username)
        self.logout()
