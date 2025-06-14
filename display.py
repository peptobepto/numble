import pygame
import sys
import random
import os

from logic import NumbleGame 

pygame.init()
pygame.mixer.init()
info = pygame.display.Info()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Load icon from assets folder for both window and taskbar
icon_path = resource_path("assets/hot.ico")
icon_surface = pygame.image.load(icon_path)
pygame.display.set_icon(icon_surface)

# Window setup
W, H = info.current_w, info.current_h
screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
pygame.display.set_caption("NUMBLE BAYBEE!!!!")

# Sounds
key_sound = pygame.mixer.Sound(resource_path("assets/explosion.wav"))
buzzer_sound = pygame.mixer.Sound(resource_path("assets/wrong.wav"))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Load images
logo = pygame.image.load(resource_path("assets/logo.png"))
logo = pygame.transform.scale(logo, (W // 6, H // 6))
logo_rect = logo.get_rect()
logo_rect.midtop = (W // 2, 30)

background = pygame.image.load(resource_path("assets/background.png"))
menu_background = pygame.transform.scale(background, (W, H))

# Tile and UI settings
TILE_SIZE = 60
TILE_GAP = 10
NUM_TILES = 5
start_x = (W - ((TILE_SIZE + TILE_GAP) * NUM_TILES - TILE_GAP)) // 2
start_y = H // 2 - TILE_SIZE // 2

font = pygame.font.SysFont(None, 48)
msg_font = pygame.font.SysFont(None, 36)
button_font = pygame.font.SysFont(None, 50)

clock = pygame.time.Clock()

start_button_rect = pygame.Rect(W//2 - 100, H//2 - 90, 200, 60)
howto_button_rect = pygame.Rect(W//2 - 100, H//2 - 10, 200, 60)
quit_button_rect = pygame.Rect(W//2 - 100, H//2 + 70, 200, 60)
quit_after_game_rect = pygame.Rect(W//2 - 100, start_y + TILE_SIZE + 80, 200, 60)

start_button_color = BLUE
howto_button_color = BLUE
quit_button_color = BLUE

in_menu = True
in_how_to_play = False
game_started = False
guess_submitted = False
buzzer_active = False
show_message = True
last_flash_time = 0
last_buzz_time = 0
flash_interval = 300
buzz_interval = random.uniform(0, 1000)

current_guess = ""
feedback = []
solution = ""
game = None

def draw_button(rect, text, color_bg, color_text):
    pygame.draw.rect(screen, color_bg, rect)
    text_surf = button_font.render(text, True, color_text)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def teleport_button(button_rect):
    new_x = random.randint(0, W - button_rect.width)
    new_y = random.randint(0, H - button_rect.height)
    button_rect.topleft = (new_x, new_y)

def draw_how_to_play():
    instructions = [
        "HOW TO PLAY NUMBLE BAYBEE!!!",
        "",
        "- uhh ouh um wait how guys howo do you play numble",
        "- type in YOUR numble. NOT MY NUMBLE!!! YOU HAVE TO MAKE YOUR OWN NUMBLE!!!",
        "- you get ONE NUMBLE GUESS!!!!!!!!",
        "- green tile mean that single numblet is perfect",
        "- yeller tile mean that single numblet is in big numble, but NOT that SPOT!!!",
        "- grey numble..... ooohh boy ouh boy YOU STUUPID!!! NUMBLET NOT!!! IN BIG NUMBLE!!!!",
        "",
        "Press 'Quit Back to Menu' to return."
    ]
    padding = 20
    box_width = W - 100
    box_height = len(instructions) * 40 + padding * 2
    box_rect = pygame.Rect(50, 80, box_width, box_height)
    pygame.draw.rect(screen, BLACK, box_rect)

    y_offset = 100 + padding
    for line in instructions:
        text_surface = msg_font.render(line, True, ORANGE)
        text_rect = text_surface.get_rect(center=(W // 2, y_offset))
        screen.blit(text_surface, text_rect)
        y_offset += 40

running = True
while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if in_menu:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    start_button_color = GREEN
                    solution = f"{random.randint(0, 99999):05}"
                    game = NumbleGame(solution)
                    current_guess = ""
                    feedback = []
                    guess_submitted = False
                    buzzer_active = False
                    in_menu = False
                    game_started = True
                elif howto_button_rect.collidepoint(event.pos):
                    howto_button_color = GREEN
                    in_how_to_play = True
                    in_menu = False
                elif quit_button_rect.collidepoint(event.pos):
                    quit_button_color = RED
                    teleport_button(quit_button_rect)

        elif in_how_to_play:
            if event.type == pygame.MOUSEBUTTONDOWN:
                quit_back_rect = pygame.Rect(W//2 - 150, H - 100, 300, 60)
                if quit_back_rect.collidepoint(event.pos):
                    start_button_color = BLUE
                    howto_button_color = BLUE
                    quit_button_color = BLUE
                    in_how_to_play = False
                    in_menu = True

        elif game_started and not guess_submitted:
            if event.type == pygame.KEYDOWN:
                key_sound.play()
                if event.key == pygame.K_BACKSPACE:
                    current_guess = current_guess[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(current_guess) == 5:
                        try:
                            feedback = game.submit_guess(current_guess)
                            guess_submitted = True
                            if current_guess != solution:
                                buzzer_active = True
                                last_flash_time = current_time
                                last_buzz_time = current_time
                                buzz_interval = random.uniform(0, 1000)
                        except Exception as e:
                            print(e)
                else:
                    if event.unicode.isdigit() and len(current_guess) < 5:
                        current_guess += event.unicode

        elif guess_submitted:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_after_game_rect.collidepoint(event.pos):
                    buzzer_active = False
                    buzzer_sound.stop()
                    running = False

    if buzzer_active and current_time - last_flash_time > flash_interval:
        show_message = not show_message
        last_flash_time = current_time

    if buzzer_active and current_time - last_buzz_time > buzz_interval:
        buzzer_sound.play()
        last_buzz_time = current_time
        buzz_interval = random.uniform(0, 1000)

    screen.blit(menu_background, (0, 0))
    screen.blit(logo, logo_rect)

    if in_menu:
        draw_button(start_button_rect, "START", start_button_color, WHITE)
        draw_button(howto_button_rect, "HOW PLAY", howto_button_color, WHITE)
        draw_button(quit_button_rect, "QUIT", quit_button_color, WHITE)

    elif in_how_to_play:
        draw_how_to_play()
        quit_back_rect = pygame.Rect(W//2 - 150, H - 100, 300, 60)
        draw_button(quit_back_rect, "QUIT BACK TO MENU", RED, WHITE)

    else:
        for i in range(NUM_TILES):
            x = start_x + i * (TILE_SIZE + TILE_GAP)
            if guess_submitted and feedback:
                if feedback[i] == "correct":
                    color = GREEN
                elif feedback[i] == "misplaced":
                    color = YELLOW
                else:
                    color = GRAY
                pygame.draw.rect(screen, color, (x, start_y, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(screen, BLACK, (x, start_y, TILE_SIZE, TILE_SIZE), 2)
            else:
                pygame.draw.rect(screen, WHITE, (x, start_y, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(screen, BLACK, (x, start_y, TILE_SIZE, TILE_SIZE), 2)

            if i < len(current_guess):
                text_surface = font.render(current_guess[i], True, BLACK)
                text_rect = text_surface.get_rect(center=(x + TILE_SIZE // 2, start_y + TILE_SIZE // 2))
                screen.blit(text_surface, text_rect)

        if guess_submitted:
            if current_guess == solution:
                msg = "yeah ok fuck you buddy I know you cheated somehow."
                msg_color = GREEN
            else:
                msg = "WRONG WRONG WRONG WRONG!!! BUZZER INCORRECT!!!"
                msg_color = RED if show_message else BLACK
            msg_surface = msg_font.render(msg, True, msg_color)
            msg_rect = msg_surface.get_rect(center=(W // 2, start_y + TILE_SIZE + 50))
            screen.blit(msg_surface, msg_rect)

            pygame.draw.rect(screen, RED, quit_after_game_rect)
            quit_text = button_font.render("QUIT", True, WHITE)
            quit_text_rect = quit_text.get_rect(center=quit_after_game_rect.center)
            screen.blit(quit_text, quit_text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
