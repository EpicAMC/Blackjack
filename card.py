from pygame.sprite import Sprite
import pygame
import assets


class Cards(Sprite):
    def __init__(self, settings, screen, card_id):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.card_id = card_id

        self.image = pygame.image.load(assets.card_sprites[self.card_id])
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.y = 50
        self.rect.x = 50

    def blitme(self):
        self.screen.blit(self.image, self.rect)