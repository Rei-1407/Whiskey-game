import pygame
import random

class AmmoBox:
    def __init__(self, game_panel):
        self.x = random.randint(0, game_panel.screen_width - game_panel.tile_size)
        self.y = random.randint(0, game_panel.screen_height - game_panel.tile_size)
        self.tile_size = game_panel.tile_size
        try:
            self.image = pygame.image.load("src\\entity\\Data\\ammoBox.png")
            self.image = pygame.transform.scale(self.image, (self.tile_size, self.tile_size))
        except:
            print("Error loading ammo box image")
            self.image = None

    def is_picked_up(self, player):
        # Kiểm tra khoảng cách giữa ammo box và player
        return (abs(self.x - player.x) < self.tile_size and 
                abs(self.y - player.y) < self.tile_size)

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.tile_size, self.tile_size))