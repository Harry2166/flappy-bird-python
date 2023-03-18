import pygame
import math
import random
from number_generator import pairs

WIDTH = 800
HEIGHT = 400

game_active = False

def distance(y1, y2):
    return math.sqrt((y1-y2)**2)

class Bird(pygame.sprite.Sprite):
    '''
    jump ✓
    gravity ✓
    coliisions
    die when you collide with ground (✓) or with the pipe (✓)
    keyboard inputs (space) ✓
    score ✓
    '''
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('flappy_bird/graphics/bird.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (52.5, 37.5))
        self.rect = self.image.get_rect(center = (100, HEIGHT/2))
        self.gravity = 0
        self.counter = 0

        self.jump_sound = pygame.mixer.Sound('flappy_bird/audio/jump.wav')
        self.jump_sound.set_volume(0.3)

    def keyboard_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.gravity = -10
            #self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1.5
        self.rect.y += self.gravity

    def update(self):
        self.keyboard_input()
        self.apply_gravity()

class Floor_Roof(pygame.sprite.Sprite):
    '''
    collision with the bird ✓
    '''
    def __init__(self, type,):
        super().__init__()
        self.type = type
        self.image = pygame.image.load('flappy_bird/graphics/barrier.png').convert_alpha()
        if self.type == 'roof':
            self.rect = self.image.get_rect(center = (0, HEIGHT-HEIGHT))
        else:
            self.rect = self.image.get_rect(center = (0, HEIGHT))

class Pipe(pygame.sprite.Sprite):
    '''
    random spawn ✓
    one for up ✓
    one for down ✓
    collision ✓
    move from left to right ✓
    have its own x and y coords to be put so that i wouldnt have much of a hard time ✓
    '''
    def __init__(self, type, y):
        super().__init__()
        self.type = type
        self.y = y
        self.image = pygame.image.load(r'C:\Users\Admin\Coding\flappy_bird\graphics\pipe.png').convert_alpha()
        if self.type == 'down':
            self.image = pygame.transform.scale(self.image, (100,200))
            self.rect = self.image.get_rect(center = (850, self.y)) # 3*HEIGHT/4 + 100 == 400
        else:
            self.image = pygame.transform.scale(self.image, (100,200))
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect = self.image.get_rect(center = (850, self.y))

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def score(self):
        if self.rect.right == larry.rect.centerx and self.type == 'down':
            larry.counter += 1
            ding_music = pygame.mixer.Sound('flappy_bird/audio/ding.wav')
            ding_music.set_volume(0.3)
            ding_music.play()

    def update(self):
        self.destroy()
        self.score()
        self.rect.x -= 6

def collision_pipe():
    if pygame.sprite.spritecollide(birdo.sprite, pipe_gang, False):# (sprite, group, bool)
        pipe_gang.empty()
        collision_music.play()
        return False
    else: return True

def collision_floor_roof():
    if pygame.sprite.spritecollide(birdo.sprite, floor_roof_gang, False):# (sprite, group, bool)
        pipe_gang.empty()
        collision_music.play()
        return False
    else: return True

def display_score():
    fonterino = pygame.font.Font('flappy_bird/font/Pixeltype.ttf', 50)
    counter = 0
    #counter += (larry.counter/2)
    score_surface = fonterino .render(f'Score: {larry.counter}', False, (255,255,255))
    score_rect = score_surface.get_rect(midtop = (400, 50))
    screen.blit(score_surface, score_rect)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")
clock = pygame.time.Clock()

bg_music = pygame.mixer.Sound('flappy_bird/audio/bg_song.mp3')
bg_music.set_volume(0.3)
bg_music.play(loops = -1)

collision_music = pygame.mixer.Sound('flappy_bird/audio/hitHurt.wav')
collision_music.set_volume(0.3)

larry = Bird()
birdo = pygame.sprite.GroupSingle()
birdo.add(larry)

pipe_gang = pygame.sprite.Group()
floor_roof_gang = pygame.sprite.Group()

background_image = pygame.image.load('flappy_bird/graphics/skyline.jpg').convert_alpha()

flappy_bird_font = pygame.font.Font('flappy_bird/font/FlappyBirdy.ttf', 110)
flappy_bird_title = flappy_bird_font.render("Flappy Bird", True, 'white')
flappy_bird_title_rect = flappy_bird_title.get_rect(center= (WIDTH/2, 75))
flappy_bird_instructions = flappy_bird_font.render("Press space to play", True, 'white')
flappy_bird_instructions_rect = flappy_bird_instructions.get_rect(center= (WIDTH/2, HEIGHT-41))

floor_roof_gang.add(Floor_Roof('roof'))
floor_roof_gang.add(Floor_Roof('floor'))

score = display_score()

pipe_update_timer = pygame.USEREVENT + 1
pygame.time.set_timer(pipe_update_timer, 1500)

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pipe_update_timer:
                y_pos = random.choice(pairs)
                pipe_gang.add(Pipe('up', y_pos[0]))
                pipe_gang.add(Pipe('down', y_pos[1]))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                select_music = pygame.mixer.Sound('flappy_bird/audio/blipSelect.wav')
                select_music.set_volume(0.3)
                select_music.play()
                game_active = True
                larry.rect.x, larry.rect.y = (100, HEIGHT/2)
                larry.counter = 0

    if game_active:
        screen.blit(background_image, (0,0))
        score = display_score()
        birdo.draw(screen)
        birdo.update()
        pipe_gang.draw(screen)
        pipe_gang.update()

        if not collision_pipe():
            game_active = False
        else:
            game_active = collision_floor_roof()
            
    else:
        screen.blit(background_image, (0,0))
        bird = pygame.image.load('flappy_bird/graphics/bird.png').convert_alpha()
        bird = pygame.transform.scale(bird, (217, 155))
        bird_rect = bird.get_rect(center = (WIDTH/2, HEIGHT/2 + 30))
        screen.blit(bird, bird_rect)
        screen.blit(flappy_bird_title, flappy_bird_title_rect)
        screen.blit(flappy_bird_instructions, flappy_bird_instructions_rect)

    pygame.display.update()
    clock.tick(60)