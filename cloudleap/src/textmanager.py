import pygame_textinput
import pygame
import pygame_widgets
from pygame_widgets.button import Button

class TextManager:
    def __init__(self, energy, screen, user_data, logging_in):
        self.textmanager = pygame_textinput.TextInputManager()
        self.textinput = pygame_textinput.TextInputVisualizer(manager=self.textmanager)
        self.textinput.cursor_width = 1
        self.textinput.cursor_blink_interval = 500
        self.textinput.font_object = pygame.font.Font("src/assets/unifont-16.0.02.otf", 15)
        self.font = pygame.font.Font("src/assets/unifont-16.0.02.otf", 30)
        self.energy = energy
        self.username = ""
        self.screen = screen
        self.user_data = user_data
        self.logging_in = logging_in
        self.button = Button(
            win=self.screen,
            x=1000, # x
            y=30, # y
            width=75, # width
            height=25, #height
            text='delete user',
            fontSize=12,
            inactiveColour=(211, 211, 211),
            hoverColour=(200, 200, 200),
            radius=10,
            onClick=lambda: self.user_data.delete_user(self.username)
        )

    def get_users(self):
        lil_font = pygame.font.Font("src/assets/unifont-16.0.02.otf", 15)
        y_coordinate = 75
        for _ , user in self.user_data.get_all_users():
            user_rendered = lil_font.render(user, True, ("Black"))
            self.screen.blit(user_rendered, (1000, y_coordinate))
            y_coordinate += 15

    def text_objects(self):
        lil_font = pygame.font.Font("src/assets/unifont-16.0.02.otf", 15)
        text = self.font.render("current energy:" + str(self.energy.points), True, ("black"))
        start = self.font.render("start game by pressing space (づ ◕‿◕ )づ", True, ("black"))
        guide1 = lil_font.render("write username below, if it doesn't exist,", True, ("black"))
        guide2 = lil_font.render("it will be created automatically:", True, ("black"))
        logged_in = lil_font.render("logged in as: " + self.username, True, ("black"))
        return text, start, guide1, guide2, logged_in

    def draw_texts(self):
        text, start, user_guide1, user_guide2, logged_in = self.text_objects()
        self.screen.blit(text, (20, 20))
        self.screen.blit(start, (300, 20))
        if self.logging_in:
            self.screen.blit(user_guide1, (10, 100))
            self.screen.blit(user_guide2, (10, 120))
        self.screen.blit(logged_in, (1000, 10))
        self.get_users()

    def button_update(self, events):
        pygame_widgets.update(events)

    def username_update(self, username):
        self.username = username

    def login(self):
        self.logging_in = False
