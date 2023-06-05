# ==============================================Importing Libraries===================================================
import pygame
import random
from math import sqrt
from pygame import mixer

# =============================================Initializing pygame====================================================
pygame.init()
CLOCK = pygame.time.Clock()  # Creating an instance of Clock to control fps later in code

# ===========================================Creating the GAME screen=================================================
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# ===============================================Setting GAME Icon====================================================
ICON = pygame.image.load("icon.png").convert_alpha(SCREEN)
pygame.display.set_icon(ICON)

# ================================================Setting GAME Title==================================================
pygame.display.set_caption("Pygame Space Invaders")

# =========================================Loading and playing Background Music=======================================
mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)

# ================================Loading Assets and converting pixels values Accordingly=============================
BACKGROUND_IMG = pygame.image.load("background.png").convert(SCREEN)
PLAYER_IMG = pygame.image.load("space-invaders.png").convert_alpha(SCREEN)
BULLET_IMG = pygame.image.load("bullet.png").convert_alpha(SCREEN)
EXPLOSION_IMG = pygame.image.load("explosion.png").convert_alpha(SCREEN)
ENEMY_1 = pygame.image.load("enemy1.png").convert_alpha(SCREEN)
ENEMY_2 = pygame.image.load("enemy2.png").convert_alpha(SCREEN)
ENEMY_3 = pygame.image.load("enemy3.png").convert_alpha(SCREEN)
DESTRUCTION_SOUND = mixer.Sound("destruction_sound.wav")
FONT = pygame.font.Font("RAVIE.ttf", 32)

# ========================================Setting Initial coordinates and variables===================================
# ===============================================Player Initial Coordinates===========================================
player_x, player_y = 370, 480
bullet_x, bullet_y = 0, 0
player_x_change, player_y_change = 0, 0

# =================Making a list of enemies images and Empty lists for the initial coordinates========================
enemy_images = (ENEMY_1, ENEMY_2, ENEMY_3, ENEMY_1, ENEMY_2, ENEMY_3, ENEMY_1, ENEMY_2, ENEMY_3, ENEMY_1)
enemy_x = list()
enemy_y = list()
enemy_x_change = list()
enemy_y_change = list()
no_of_enemies = 10

# =================Filling up the initial Coordinate in respective lists for all the number of enemies================
for i in range(no_of_enemies):
    enemy_x.append(random.randint(0, 376))
    enemy_y.append(random.randint(0, 200))
    enemy_x_change.append(5)
    enemy_y_change.append(20)

# ===============================================Defining remaining Variables=========================================
bullet_fired = False
collision = False
running = True
score = 0
health = 3
level = 1
WHITE_COLOR = (255, 255, 255)
GAME_OVER_TEXT = FONT.render('GAME OVER', True, WHITE_COLOR)

# ===================================================MAIN GAME LOOP==================================================
while running:

    # ========================================Showing Background Image on screen=====================================
    SCREEN.blit(BACKGROUND_IMG, (0, 0))

    # ==========================Checking the health and if it is zero then Displaying GAME OVER======================
    if health <= 0:
        if enemy_y[0] < 1000:
            for i in range(10):
                enemy_y[i] = 2000
                SCREEN.blit(EXPLOSION_IMG, (player_x, player_y))
                DESTRUCTION_SOUND.play()
                pygame.time.delay(100)
        SCREEN.blit(GAME_OVER_TEXT, (280, 280))

    # ==============================increasing the difficulty level as the score increases===========================
    if score == 500:
        level = 2
    if score == 1500:
        level = 3

    # ====Checking for Events and In_game Key_presses to control the player movements or quit the game Accordingly====
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                player_x_change = -7
            if event.key == pygame.K_RIGHT:
                player_x_change = 7
            if event.key == pygame.K_DOWN:
                player_y_change = 7
            if event.key == pygame.K_UP:
                player_y_change = -7

            if event.key == pygame.K_SPACE:
                bullet_fired = True
                bullet_x = player_x
                bullet_y = player_y

        if event.type == pygame.KEYUP:
            player_x_change = 0
            player_y_change = 0

    # =================================Changing player Coordinates according to user input============================
    player_x += player_x_change
    player_y += player_y_change

    # ==========================Restricting the player to stay inside the screen limit================================
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736
    if player_y <= 0:
        player_y = 0
    elif player_y >= 500:
        player_y = 500

    # ===============Nested LOOP to check and control all the enemies at every iteration of Main While loop===========
    for i in range(no_of_enemies):

        # ======Restricting the enemy to stay on screen and changing its direction if it touches the boundary=========
        # ==========================Also changing the speed according to the difficulty level=========================
        if enemy_x[i] <= 0:
            if level == 1:
                enemy_x_change[i] = 7
            elif level == 2:
                enemy_x_change[i] = 10
            elif level == 3:
                enemy_x_change[i] = 15
            enemy_y[i] += 20
        elif enemy_x[i] >= 736:
            if level == 1:
                enemy_x_change[i] = -7
            elif level == 2:
                enemy_x_change[i] = -10
            elif level == 3:
                enemy_x_change[i] = -15
            enemy_y[i] += 20
        if enemy_y[i] > 480:  # Respawns the enemy if it goes too down on the screen and decreases health
            if health > 0:
                enemy_x[i] = random.randint(0, 376)
                enemy_y[i] = random.randint(0, 200)
                health -= 1

        # ========Changing Actual coordinates of the enemies and spawning them on screen if health is not zero========
        enemy_x[i] += enemy_x_change[i]
        if health > 0:
            SCREEN.blit(enemy_images[i], (enemy_x[i], enemy_y[i]))

        # ==========================Checking if bullet is in fire state and then firing the bullet====================
        if bullet_fired:
            bullet_y += -15
            SCREEN.blit(BULLET_IMG, (bullet_x, bullet_y))
            if bullet_y == 0:
                bullet_fired = False
            # =====================Checking if bullet hit the enemy using distance formula============================
            bullet_enemy_distance = sqrt(((bullet_x - enemy_x[i]) ** 2) + ((bullet_y - enemy_y[i]) ** 2))
            if bullet_enemy_distance < 70:
                SCREEN.blit(EXPLOSION_IMG, (enemy_x[i], enemy_y[i]))
                DESTRUCTION_SOUND.play()
                pygame.time.delay(20)
                enemy_x[i] = random.randint(0, 376)
                enemy_y[i] = random.randint(0, 200)
                bullet_fired = False
                score += 10

        # =======================Checking if Player collides with the Enemy using distance formula====================
        player_enemy_distance = sqrt(((player_x - enemy_x[i]) ** 2) + ((player_y - enemy_y[i]) ** 2))
        if player_enemy_distance < 55:
            DESTRUCTION_SOUND.play()
            health -= 1
            SCREEN.blit(EXPLOSION_IMG, (player_x, player_y))
            pygame.time.delay(60)
            if health > 0:
                player_x, player_y = 370, 480

    # ======================================Showing player, score and health on screen=================================
    if health > 0:
        SCREEN.blit(PLAYER_IMG, (player_x, player_y))
    score_text = FONT.render('Score: ' + str(score), True, WHITE_COLOR)
    SCREEN.blit(score_text, (0, 0))
    health_text = FONT.render('Health: ' + str(health), True, WHITE_COLOR)
    SCREEN.blit(health_text, (600, 0))
    level_text = FONT.render('LEVEL: ' + str(level), True, WHITE_COLOR)
    SCREEN.blit(level_text, (300, 0))

    # =============================updates the Display screen on every iteration of while loop========================
    pygame.display.update()
    CLOCK.tick(60)  # Fixing the FPS to 60 Frames per Second
