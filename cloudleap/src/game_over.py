import pygame

class GameOver():
    def __init__(self, screen, points):
        self.screen = screen
        self.points = points
        self.rect = pygame.Rect(320, 180, 640, 360)
        self.red = (86, 3, 25)
        self.big = pygame.font.Font("src/assets/unifont-16.0.02.otf", 50)
        self.small = pygame.font.Font("src/assets/unifont-16.0.02.otf", 30)


    def texts(self):
        big_text = self.big.render("GAME OVER ( •̀ᴗ•́ )و ̑̑", True, self.red)
        points = self.big.render("energy at the end: " + str(self.points), True, self.red)
        small_text = self.small.render("open new game to try again~", True, self.red)
        window = self.small.render("wait, window will close automatically", True, self.red)
        return big_text, points, small_text, window

    def game_over_display(self, time_shown):
        big_text, points, small_text, window = self.texts()
        self.screen.fill("white")
        pygame.draw.rect(self.screen, (139, 0, 0), self.rect, border_radius=5)
        self.screen.blit(big_text, (415, 300))
        self.screen.blit(points, (390, 370))
        self.screen.blit(small_text, (440, 440))
        self.screen.blit(window, (370, 470))
        pygame.display.flip()
        pygame.time.delay(time_shown)
