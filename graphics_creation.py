import pygame

def import_images():
    tile_unpressed = pygame.image.load('./assets/tile_not_revealed.png').convert_alpha()
    tile_pressed = pygame.image.load('./assets/tile_pressed.png').convert_alpha()

    bomb_image = pygame.image.load('./assets/bomb.png').convert_alpha()
    bomb_tile = tile_unpressed.copy()
    bomb_tile.blit(bomb_image, (3,3))
    bomb_clicked = pygame.image.load('./assets/tile_bomb.png').convert_alpha()
    bomb_clicked.blit(bomb_image, (3,3))

    flag_tile = tile_unpressed.copy()
    flag_image = pygame.image.load('./assets/flag.png').convert_alpha()
    flag_tile.blit(flag_image, (3,3))

    fake_flag_tile = flag_tile.copy()

    red_surf = pygame.Surface((32, 32))
    red_surf.fill((255,0,0))
    red_surf.set_alpha(35)
    fake_flag_tile.blit(red_surf, (0,0))
    tile_graphics_list = [tile_unpressed, tile_pressed, bomb_tile, bomb_clicked, flag_tile, fake_flag_tile]

    left_scoreboard = pygame.image.load('./assets/Scoreboard_left.png').convert_alpha()
    middle_scoreboard = pygame.image.load('./assets/Scoreboard_middle.png').convert_alpha()
    right_scoreboard = pygame.image.load('./assets/Scoreboard_right.png').convert_alpha()
    scoreboard_graphics_list = [left_scoreboard, middle_scoreboard, right_scoreboard]


    return tile_graphics_list, scoreboard_graphics_list
