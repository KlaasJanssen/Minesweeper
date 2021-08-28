import pygame
from random import randint
from tile import Tile
from graphics_creation import import_images
from button import Button

class Board:
    def __init__(self, size_y, size_x, bombs, block_size):
        self.screen = pygame.display.get_surface()
        self.screen_width = self.screen.get_size()[0]
        self.screen_height = self.screen.get_size()[1]

        self.offset_x = (self.screen_width - size_x * block_size) / 2
        self.offset_y = (self.screen_height - size_y * block_size) / 2 + 30
        self.block_size = block_size
        self.game_state = 'active'
        self.tiles = []
        self.bomb_num = bombs
        self.size_x = size_x
        self.size_y = size_y
        self.bombs = self.place_bombs(self.bomb_num)
        self.flag_pressed = False
        self.flags_placed = 0
        self.tiles_pressed = 0

        self.game_font = pygame.font.Font(None, 20)
        #print(self.bombs)
        graphics_list, score_graphics = import_images()

        if not self.block_size == 32:
            for index, asset in enumerate(graphics_list):
                graphics_list[index] = pygame.transform.scale(asset, (self.block_size, self.block_size))

        self.scoreboard_left = score_graphics[0]
        self.scoreboard_left_rect = self.scoreboard_left.get_rect(bottomleft = (self.offset_x, self.offset_y))
        self.scoreboard_middle = pygame.transform.scale(score_graphics[1], (self.block_size * self.size_x - 40,60))
        self.scoreboard_middle_rect = self.scoreboard_middle.get_rect(bottomleft = (self.offset_x + 20, self.offset_y))
        self.scoreboard_right = score_graphics[2]
        self.scoreboard_right_rect = self.scoreboard_right.get_rect(bottomright = (self.screen.get_size()[0] - self.offset_x, self.offset_y))

        for i in range(size_y):
            temp = []
            for j in range(size_x):
                if (i, j) in self.bombs:
                    temp.append(Tile(True, j * self.block_size, i * block_size, self.offset_x, self.offset_y, graphics_list))
                else:
                    temp.append(Tile(False, j * self.block_size, i * self.block_size, self.offset_x, self.offset_y, graphics_list))
            self.tiles.append(temp)

        self.score_board_surf = pygame.Surface((self.block_size * self.size_x, 60))
        self.score_board_rect = self.score_board_surf.get_rect(bottomleft = (self.offset_x, self.offset_y))
        self.start_time = pygame.time.get_ticks()
        self.score_font = pygame.font.Font('./assets/Digital_Dismay.otf', 40)

        self.menu_button = Button(self.offset_y - 50, 80, 40, "Menu", 2)

        # Sound
        self.bomb_exposion = pygame.mixer.Sound('./assets/explosion.wav')
        self.safe_click = pygame.mixer.Sound('./assets/safe_click.wav')
        self.safe_click_play = True
        self.place_flag_sound = pygame.mixer.Sound('./assets/place_flag.wav')
        self.place_flag_sound.set_volume(0.3)
        self.remove_flag = pygame.mixer.Sound('./assets/remove_flag.wav')
        self.remove_flag.set_volume(0.3)


    def draw_board(self):
        self.screen.blit(self.scoreboard_left, self.scoreboard_left_rect)
        self.screen.blit(self.scoreboard_middle, self.scoreboard_middle_rect)
        self.screen.blit(self.scoreboard_right, self.scoreboard_right_rect)

        for row in self.tiles:
            for col in row:
                col.draw_tile()

        if self.game_state == 'game_over':
            self.reveal_all_bombs()




    def update(self):
        if self.game_state == 'active':
            self.click_tile()
        self.display_score()
        self.safe_click_play = True
        return self.game_state

    def click_tile(self):
        pos_x = pygame.mouse.get_pos()[0]
        grid_x = int((pos_x - self.offset_x) / self.block_size)
        pos_y = pygame.mouse.get_pos()[1]
        grid_y = int((pos_y - self.offset_y) / self.block_size)
        if pos_x - self.offset_x < 0 or pos_y - self.offset_y < 0:
            grid_x = - 1
        if pygame.mouse.get_pressed()[0]:
            if grid_x >= 0 and grid_x < self.size_x:
                if grid_y >= 0 and grid_y < self.size_y:
                    if self.tiles[grid_y][grid_x].state == 'unpressed':
                        self.handle_tile_click(grid_y, grid_x)

        elif pygame.mouse.get_pressed()[2]:
            if grid_x >= 0 and grid_x < self.size_x:
                if grid_y >= 0 and grid_y < self.size_y:
                    if self.tiles[grid_y][grid_x].state == 'unpressed' or self.tiles[grid_y][grid_x].state == 'flagged':
                        if self.flag_pressed == False:
                            if self.tiles[grid_y][grid_x].state == 'unpressed':
                                self.place_flag_sound.play()
                            else:
                                self.remove_flag.play()
                            self.flags_placed += self.tiles[grid_y][grid_x].place_flag()

                    self.flag_pressed = True
        else:
            self.flag_pressed = False


    def handle_tile_click(self, y, x):
        bombs = self.tiles[y][x].reveal()
        if bombs == "BOOM":
            self.game_state = 'game_over'
            self.bomb_exposion.play()
            self.reveal_all_bombs()
        else:
            if self.safe_click_play:
                self.safe_click.play()
                self.safe_click_play = False
            self.tiles_pressed += 1
            if self.tiles_pressed == self.size_x * self.size_y - self.bomb_num:
                self.game_state = 'won'
                self.end_time = pygame.time.get_ticks()
            surround_bombs = self.get_num_bombs(y, x)
            self.tiles[y][x].surround_bombs = surround_bombs
            if surround_bombs == 0: color = (0,0,0)
            elif surround_bombs == 1: color = (0,0,255)
            elif surround_bombs == 2: color = (0,200,0)
            elif surround_bombs == 3: color = (255,0,0)
            elif surround_bombs == 4: color = (128,0,128)
            elif surround_bombs == 5: color = (128,0,0)
            elif surround_bombs == 6: color = (64,224,208)
            elif surround_bombs == 7: color = (0,0,0)
            elif surround_bombs == 8: color = (128,128,128)
            self.tiles[y][x].text_surf = self.game_font.render(str(surround_bombs), True, color)
            self.tiles[y][x].text_rect = self.tiles[y][x].text_surf.get_rect(center = self.tiles[y][x].rect.center)
            if surround_bombs == 0:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if not (i == 0 and j == 0):
                            if y + i >= 0 and y + i < self.size_y and x + j >= 0 and x + j < self.size_x:
                                if self.tiles[y + i][x + j].state == 'unpressed':
                                    self.handle_tile_click(y + i, x + j)


    def place_bombs(self, bombs):
        bomb_list = []
        while len(bomb_list) < bombs:
            bomb_pos = (randint(0, self.size_y - 1), randint(0, self.size_x - 1))
            if not bomb_pos in bomb_list:
                bomb_list.append(bomb_pos)
        return bomb_list

    def reveal_all_bombs(self):
        for row in self.tiles:
            for col in row:
                if col.bomb == True and col.state == 'unpressed':
                    col.add_bomb_image()
                elif col.bomb == False and col.state == 'flagged':
                    col.add_fake_flag()

    def get_num_bombs(self, y, x):
        bombs = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0):
                    if y + i >= 0 and y + i < self.size_y and x + j >= 0 and x + j < self.size_x:
                        if self.tiles[y + i][x + j].bomb:
                            bombs += 1
        return bombs

    def display_score(self):
        # Time
        if self.game_state == 'active':
            self.current_time = pygame.time.get_ticks()
            self.time_taken = int((self.current_time - self.start_time) / 1000)
            if self.time_taken >= 999:
                self.time_taken = 999
        self.time_surf = self.score_font.render(f'{self.time_taken:03}', True, 'red')
        self.time_background = pygame.Surface((self.time_surf.get_size()[0] + 15,40))
        self.time_background.fill((50,50,50))
        self.time_background_rect = self.time_background.get_rect(bottomright = (self.scoreboard_right_rect.left, self.scoreboard_right_rect.bottom - 10))
        self.time_rect = self.time_surf.get_rect(center = self.time_background_rect.center - pygame.math.Vector2(-2,0))
        self.screen.blit(self.time_background, self.time_background_rect)
        pygame.draw.rect(self.screen, 'black', self.time_background_rect, 2)
        self.screen.blit(self.time_surf, self.time_rect)

        # Flags
        number_left = self.bomb_num - self.flags_placed
        self.flags_surf = self.score_font.render(f'{number_left:03}', True, 'red')
        self.flag_background_rect = self.time_background.get_rect(bottomleft = (self.scoreboard_left_rect.right, self.scoreboard_left_rect.bottom - 10))
        self.flags_rect = self.flags_surf.get_rect(center = self.flag_background_rect.center - pygame.math.Vector2(-2,0))
        self.screen.blit(self.time_background, self.flag_background_rect)
        pygame.draw.rect(self.screen, 'black', self.flag_background_rect, 2)
        self.screen.blit(self.flags_surf, self.flags_rect)

        if self.menu_button.update():
            self.game_state = 'intro'

    def get_final_score(self):
        return (self.end_time - self.start_time) / 1000
