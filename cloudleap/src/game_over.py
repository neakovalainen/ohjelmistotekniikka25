import pygame

class GameOver():
    def __init__(self, screen):
        self.screen = screen
        self.rect = pygame.Rect(320, 180, 640, 360)
        self.red = (86, 3, 25)
        self.big = pygame.font.Font("src/assets/unifont-16.0.02.otf", 50)
        self.small = pygame.font.Font("src/assets/unifont-16.0.02.otf", 30)
        self.big_text = self.big.render("GAME OVER ( •̀ᴗ•́ )و ̑̑", True, self.red)
        self.small_text = self.small.render("open new game to try again~", True, self.red)
        self.window = self.small.render("wait, window will close automatically", True, self.red)

    def game_over_display(self, time_shown):
        self.screen.fill("white")
        pygame.draw.rect(self.screen, (139, 0, 0), self.rect, border_radius=5)
        self.screen.blit(self.big_text, (400, 300))
        self.screen.blit(self.small_text, (440, 370))
        self.screen.blit(self.window, (370, 400))
        pygame.display.flip()
        pygame.time.delay(time_shown)
