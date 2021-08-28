import pygame, sys
from random import randint
from board import Board
from tile import Tile
from button import Button

class Main_game:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.screen_width = self.screen.get_size()[0]
        self.screen_height = self.screen.get_size()[1]
        self.game_state = 'intro'
        self.button1 = Button(250, 300, 75, "Easy")
        self.button2 = Button(350, 300, 75, "Medium")
        self.button3 = Button(450, 300, 75, "Hard")
        self.logo_surf = pygame.image.load('./assets/logo.png').convert_alpha()
        self.logo_rect = self.logo_surf.get_rect(center = (self.screen.get_size()[0] / 2 - 50, 125))
        self.title_font = pygame.font.Font(None, 65)
        self.title_text_surf1 = self.title_font.render('MINE', True, (0,0,0))
        self.title_text_surf2 = self.title_font.render('SWEEPER', True, (0,0,0))
        self.title_text_rect1 = self.title_text_surf1.get_rect(center = (130, 125))
        self.title_text_rect2 = self.title_text_surf2.get_rect(center = (420, 125))
        self.background_music = pygame.mixer.Sound('./assets/background.mp3')
        self.background_music.set_volume(0.3)
        self.background_music.play(loops = -1)
        self.win_font = pygame.font.Font(None, 45)

        self.win_background = pygame.Surface((250,200))
        self.win_background.fill((200,200,200))
        self.win_background_rect = self.win_background.get_rect(center = (self.screen_width / 2, self.screen_height / 2))

    def update(self):
        if self.game_state == 'active':
            self.board.draw_board()
            self.game_state = self.board.update()
        elif self.game_state == 'won':
            self.board.draw_board()
            self.game_state = self.board.update()
            self.display_win_screen()
        elif self.game_state == 'game_over':
            self.board.draw_board()
            self.game_state = self.board.update()
        elif self.game_state == 'intro':
            self.display_intro_screen()

    def start_game(self, rows, cols, bombs, block_size):
        self.board = Board(rows,cols, bombs, block_size)
        self.game_state = 'active'


    def display_intro_screen(self):
        self.screen.blit(self.logo_surf, self.logo_rect)
        self.screen.blit(self.title_text_surf1, self.title_text_rect1)
        self.screen.blit(self.title_text_surf2, self.title_text_rect2)
        self.button1.draw()
        if self.button1.update():
            self.difficulty = 'easy'
            self.start_game(rows = 9, cols = 9, bombs = 1, block_size = 32)
        self.button2.draw()
        if self.button2.update():
            self.difficulty = 'medium'
            self.start_game(rows = 16, cols = 16, bombs = 40, block_size = 32)
        self.button3.draw()
        if self.button3.update():
            self.difficulty = 'hard'
            self.start_game(rows = 15, cols = 30, bombs = 99, block_size = 16)

    def display_win_screen(self):
        self.screen.blit(self.win_background, self.win_background_rect)
        pygame.draw.rect(self.screen, (0,0,0), self.win_background_rect, 2)

        self.win_surf = self.win_font.render("You win!", True, (0,0,0))
        self.win_rect = self.win_surf.get_rect(center = (self.screen_width / 2, self.win_background_rect.top + 30))
        self.screen.blit(self.win_surf, self.win_rect)

        score = self.board.get_final_score()
        self.score_surf = self.win_font.render(f"Time: {score}s", True, (0,0,0))
        self.score_rect = self.score_surf.get_rect(center = (self.screen_width / 2, self.win_background_rect.top + 80))
        self.screen.blit(self.score_surf, self.score_rect)




if __name__ == "__main__":
    screen_width, screen_height = 600,600
    pygame.init()
    screen = pygame.display.set_mode((screen_width,screen_height))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Mine Sweeper')

    main_game = Main_game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((220,220,220))
        main_game.update()
        #print(pygame.mouse.get_pos())
        pygame.display.update()
        clock.tick(60)
