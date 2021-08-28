import pygame
from random import randint

class Tile:
    def __init__(self, bomb, x, y, offset_x, offset_y, graphics_list):

        self.screen_width = pygame.display.get_surface().get_size()[0]
        self.screen_height = pygame.display.get_surface().get_size()[1]
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.state = 'unpressed'
        self.bomb = False
        self.image = graphics_list[0]
        self.rect = self.image.get_rect(topleft = (x + offset_x, y + offset_y))
        self.bomb = bomb
        self.screen = pygame.display.get_surface()

        # grahics import
        self.tile_unpressed = graphics_list[0]
        self.tile_pressed = graphics_list[1]
        self.bomb_tile = graphics_list[2]
        self.bomb_clicked = graphics_list[3]
        self.flag_tile = graphics_list[4]
        self.fake_flag_tile = graphics_list[5]


    def draw_tile(self):
        self.screen.blit(self.image, self.rect)
        if self.state == 'pressed' and not self.bomb:
            if not self.surround_bombs == 0:
                self.screen.blit(self.text_surf, self.text_rect)

    def reveal(self):
        self.state = 'pressed'
        self.image = self.tile_pressed
        if self.bomb:
            self.image = self.bomb_clicked
            return 'BOOM'
        else:
            self.image = self.tile_pressed
            return ':)'

    def place_flag(self):
        if self.state == 'unpressed':
            self.image = self.flag_tile
            self.state = 'flagged'
            return 1
        elif self.state == 'flagged':
            self.image = self.tile_unpressed
            self.state = 'unpressed'
            return -1

    def add_fake_flag(self):
        self.image = self.fake_flag_tile

    def add_bomb_image(self):
        self.image = self.bomb_tile
