import pygame

class Button:
    def __init__(self, y, w, h, text, lw = 4):
        self.screen = pygame.display.get_surface()
        self.x = int(self.screen.get_width() / 2)
        self.y = y
        self.width = w
        self.height = h
        self.lw = lw
        self.surf = pygame.Surface((w,h))
        self.rect = self.surf.get_rect(midtop = (self.x,self.y))
        self.pressed = False
        self.text = text
        self.button_font = pygame.font.Font(None, 32)
        self.text_surf = self.button_font.render(text, True, (255,255,255))
        self.text_rect = self.text_surf.get_rect(center = self.rect.center)
        self.color = (100,100,100)
        self.click_sound = pygame.mixer.Sound('./assets/button_click.wav')


    def update(self):
        if self.detect_mouse_click():
            clicked = True
        else:
            clicked = False
        self.draw()
        return clicked

    def detect_mouse_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.color = (50,50,50)
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    self.pressed = False
                    self.click_sound.play()
                    return True
        else:
            self.pressed = False
            self.color = (100,100,100)
        return False

    def draw(self):
        self.surf.fill(self.color)
        self.screen.blit(self.surf, self.rect)
        pygame.draw.rect(self.screen, (0,0,0), self.rect, self.lw)
        self.screen.blit(self.text_surf, self.text_rect)
