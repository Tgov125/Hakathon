#Note for myself: Run the
# "pyinstaller --onefile --noconsole --icon="assets\Icon.ico" --add-data "assets\Icon.png;assets" --add-data "assets\The_map.png;assets" --add-data "assets\Lore_page.png;assets" --add-data "assets\Victory_screen.png;assets" Crazy_Blob.py"
#command after changes.

#Pygame importation/initiation
import pygame
init = pygame.init()
import time
import os
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


#Adding an icon to the window
pygame.display.set_icon(pygame.image.load(resource_path('assets/Icon.png')))



#Window creating
win_height = 600
win_width = 800
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Crazy Blob")


try:
    background_img = pygame.image.load(resource_path(os.path.join("assets", "The_map.png")))
    background_img = pygame.transform.scale(background_img, (win_width, win_height))
    lore_img = pygame.image.load(resource_path(os.path.join("assets", "Lore_page.png")))
    lore_img = pygame.transform.scale(lore_img, (win_width, win_height))
    victory_img = pygame.image.load(resource_path(os.path.join("assets", "Victory_screen.png")))
    victory_img = pygame.transform.scale(victory_img, (win_width, win_height))
except pygame.error as e:
    print(f"Error loading background image: {e}")
    background_img = pygame.Surface((win_width, win_height))
    background_img.fill((255, 255, 255))


#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
TITLE_COLOR = (50, 50, 150) #Dark blue
SLIME_COLOR = (255, 255, 0) #Dark green
LORE_TEXT_COLOR = (255, 255, 0) #Yellow
VICTORY_TEXT_COLOR = (0, 150, 200)  #Blue



#Buttom dimensions
button_width = 200
button_height = 50
button_spacing = 20



#Creating fonts
pygame.font.init()
font = pygame.font.SysFont('Arial', 32)
title_font = pygame.font.SysFont('Arial', 64, bold=True)
description_font = pygame.font.SysFont('Arial', 24)



#Creating classes:

#Button's class
class Button:
    def __init__(self, x_button, y_button, width, height, text_button):
        self.rect = pygame.Rect(x_button, y_button, width, height)
        self.text = text_button
        self.is_hovered = False


    def draw(self, surface):
        color = GRAY if self.is_hovered else BLACK
        pygame.draw.rect(surface, color, self.rect)
        text_surface = font.render(self.text, True, WHITE)
        text_rect1 = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect1)


    def handle_event(self, event_button):
        if event_button.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event_button.pos)
        elif event_button.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False



#Player's class
class Player:
    def __init__(self):
        self.x = win_width // 2
        self.y = win_height // 2
        self.speed = 5
        self.passive_direction = "right"
        self.passive_speed = 2
        self.radius = 20
        self.speed_increase_rate = 0.01


    def check_border_collision(self):
        if (self.x - self.radius <= 0 or
                self.x + self.radius >= win_width or
                self.y - self.radius <= 0 or
                self.y + self.radius >= win_height):
            return True
        return False


    def update(self):
        self.passive_speed += self.speed_increase_rate

        if self.passive_direction == "left":
            self.x -= self.passive_speed
        elif self.passive_direction == "right":
            self.x += self.passive_speed
        elif self.passive_direction == "up":
            self.y -= self.passive_speed
        elif self.passive_direction == "down":
            self.y += self.passive_speed


    def change_direction(self, direction):
        self.passive_direction = direction


    def draw(self, surface):
        pygame.draw.circle(surface, SLIME_COLOR, (self.x, self.y), self.radius)






#Creating title
title_text = "Crazy Blob"
title_surface = title_font.render(title_text, True, TITLE_COLOR)
title_rect = title_surface.get_rect()
title_rect.centerx = win_width // 2
title_rect.top = 50




#Creating buttons a player can interact with
buttons = []
button_texts = ["Start", "Guide", "-Lore-", "Quit"]
total_height = len(button_texts) * button_height + (len(button_texts) - 1) * button_spacing
start_y = (win_height - total_height) // 2

for i, text in enumerate(button_texts):
    x = (win_width - button_width) // 2
    y = start_y + i * (button_height + button_spacing)
    buttons.append(Button(x, y, button_width, button_height, text))



#States of the game | Timer states
MENU = "menu"
GAME = "game"
GAME_OVER = "game over"
GUIDE = "guide"
LORE = "lore"
VICTORY = "victory"
current_state = MENU

game_start_time = None
survival_time = 0



#Initiating the player
player = Player()



#Creating a clock along with FPS
clock = pygame.time.Clock()
FPS = 60


#The menu
running = True
while running:

    #Launch the clock for FPS
    clock.tick(FPS)



    #Event fetching
    for event in pygame.event.get():

        #Allow the player to quit the game by pressing X
        if event.type == pygame.QUIT:
            running = False

        if current_state == MENU:
            for button in buttons:
                if button.handle_event(event):
                    if button.text == "Start":
                        current_state = GAME
                        game_start_time = time.time()
                        player = Player()
                    if button.text == "Guide":
                        current_state = GUIDE
                    if button.text == "Quit":
                        running = False
                    if button.text == "-Lore-":
                        current_state = "lore"



    #Clear the screen
    win.fill(WHITE)



    #Drawing content based on game state
    if current_state == MENU:

        # Remove duplicate button handling code here since it's already done in event handling

        #Drawing the title of the game
        win.blit(title_surface, title_rect)
        pygame.draw.line(win, TITLE_COLOR,
                         (title_rect.left, title_rect.bottom + 10),
                         (title_rect.right, title_rect.bottom + 10), 3)


        for button in buttons:
            button.draw(win)


    elif current_state == GAME:
        win.blit(background_img, (0, 0))

        #Set the start time when entering game-state if it hasn't been set
        if game_start_time is None:
            game_start_time = time.time()

        #Drawing the player
        player.draw(win)


        #Checking for border collision
        if player.check_border_collision():
            current_state = GAME_OVER
            survival_time = round(time.time() - game_start_time, 1)
            game_start_time = None



        #Displaying current time while playing
        if game_start_time is not None:  # Add this check
            current_time = round(time.time() - game_start_time, 1)
            time_text = font.render(f"Time: {current_time} seconds", True, BLACK)
            time_rect = time_text.get_rect(topleft=(10, 10))
            win.blit(time_text, time_rect)

        if current_time == 40:
            current_state = VICTORY
            survival_time = round(time.time() - game_start_time, 1)
            game_start_time = None



        #Updating player's direction
        player.update()



        #Making the player move
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.change_direction("left")
        elif keys[pygame.K_d]:
            player.change_direction("right")
        elif keys[pygame.K_w]:
            player.change_direction("up")
        elif keys[pygame.K_s]:
            player.change_direction("down")



    elif current_state == GAME_OVER:
        game_over_text = title_font.render("Game Over!", True, TITLE_COLOR)
        game_over_rect = game_over_text.get_rect(center=(win_width // 2, win_height // 2 - 50))
        win.blit(game_over_text, game_over_rect)

        result_text = description_font.render(f"You survived for {survival_time} seconds!", True, BLACK)
        result_rect = result_text.get_rect(center=(win_width // 2, win_height // 2 + 50))
        win.blit(result_text, result_rect)

        restart_text = font.render("Press SPACE to return to the menu", True, BLACK)
        restart_rect = restart_text.get_rect(center=(win_width // 2, win_height // 2 + 150))
        win.blit(restart_text, restart_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            current_state = MENU
            game_start_time = None  # Reset the time when returning to the menu
            survival_time = 0
            player = Player()



    elif current_state == GUIDE:
        # Title
        guide_title = title_font.render("How to Play", True, TITLE_COLOR)
        guide_title_rect = guide_title.get_rect(center=(win_width // 2, 100))
        win.blit(guide_title, guide_title_rect)

        # Game instructions
        instructions = [
            "Control your blob using WASD keys:",
            "W - Move Up",
            "A - Move Left",
            "S - Move Down",
            "D - Move Right",
            "",
            "Avoid touching the walls!",
            "Try to survive as long as possible.",
            "",
            "Press SPACE to return to menu"
        ]

        for i, line in enumerate(instructions):
            text = description_font.render(line, True, BLACK)
            text_rect = text.get_rect(center=(win_width // 2, 200 + i * 40))
            win.blit(text, text_rect)

        # Handle a SPACE key to return to the menu
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            current_state = MENU


    elif current_state == LORE:
        win.blit(lore_img, (0, 0))

        #Title
        lore_title = title_font.render("Story of a blob", True, LORE_TEXT_COLOR)
        lore_title_rect = lore_title.get_rect(center=(win_width // 2, 100))
        win.blit(lore_title, lore_title_rect)

        #The story
        story = [
            "You are a blob that has been poisoned in the forest.",
            "The poison makes you dizzy",
            "Sending you into a frantic, uncontrollable state.",
            "Your speed increases drastically, making movement more dangerous.",
            "Because of your extreme speed, crashing into trees will be fatal.",
            "You must endure for over 40 seconds until the poison wears off.",
            "Only then can you return home and finally get some rest.",
            "-Press SPACE to return to the menu-"
        ]

        for i, line in enumerate(story):
            text = description_font.render(line, True, LORE_TEXT_COLOR)
            text_rect = text.get_rect(center=(win_width // 2, 200 + i * 40))
            win.blit(text, text_rect)

        # Handle a SPACE key to return to the menu
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            current_state = MENU

    elif current_state == VICTORY:
        win.blit(victory_img, (0, 0))

        #Title
        victory_title = title_font.render("You saved blob!", True, VICTORY_TEXT_COLOR)
        victory_title_rect = victory_title.get_rect(center=(win_width // 2, 100))
        win.blit(victory_title, victory_title_rect)

        #Description
        Congratulation = [
            "You survived for",
            f"{survival_time} seconds",
            "and saved the blob!",
            "Job well done!",
            "-Press SPACE to return to the menu-"
        ]

        for i, line in enumerate(Congratulation):
            text = description_font.render(line, True, VICTORY_TEXT_COLOR)
            text_rect = text.get_rect(center=(win_width // 2, 200 + i * 40))
            win.blit(text, text_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            current_state = MENU

    #Display update
    pygame.display.update()