import pygame.font
import game_functions


class Button:

    def __init__(self, settings, screen, button_id, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.button_id = button_id
        self.msg = msg

        self.width, self.height = 200, 60
        self.button_color = (100, 50, 50)
        self.text_color = (200, 200, 200)
        self.font = pygame.font.SysFont(None, 40)

        self.rect = pygame.Rect(0, 0, self.width, self.height)

    def prep_msg(self):
        self.msg_image = self.font.render(self.msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center


    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)