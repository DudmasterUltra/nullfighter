import sys

#Check Python version
if (sys.version_info.major < 3):
    print("Python 3+ is required.")
    quit()

#Pygame install wizard, imports
try:
    import pygame
except ImportError:
    print("Pygame is required. Install? (y/n)")
    val = input()
    if (val == "y" or val == "Y"):
        import pip
        print("installing pygame...")
        pip.main(["install", "pygame"])
        import pygame
        print("Complete!")
    else:
        quit()

import random, math, nullfighter_sprites

#Initialize pygame and menu
pygame.init()
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
GAME_NAME = "nullfighter"
font_code = pygame.font.SysFont("monospace", 15)
font_name = pygame.font.Font("Paskowy.ttf", 100)
font_menu = pygame.font.Font("HackedCrt.ttf", 35)
pygame.display.set_caption(GAME_NAME)
pygame.display.set_icon(pygame.image.load("ship.png"))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.key.set_repeat(100, 100)
running = True
clock = pygame.time.Clock()
menuitem = 0
framecount = 0
menu_offset = 0

#Create menu surfaces
image_title = font_name.render(GAME_NAME, 0, (255, 255, 255))
image_play = font_menu.render("play", 0, (255, 255, 255))
image_exit = font_menu.render("exit", 0, (255, 255, 255))
image_arrow = font_menu.render(">     <", 0, (255, 255, 255))
alphaSurface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
alphaSurface.fill((0, 0, 0))
alphaSurface.set_alpha(0)

#Read code
words = [line.rstrip() for line in open(__file__)]

#Initialize code positions
codes = []
for i in range(10):
    codes.append((random.randint(-200, SCREEN_WIDTH), random.randint(-200, SCREEN_HEIGHT)))

#Render code at a position with color
def drawcode(x, y, col):
    y_off = 0
    for word in words:
        label = font_code.render(word, 0, col)
        screen.blit(label, (x, y + y_off))
        y_off += label.get_height()

#Calculate the color in a sine pattern
def calccolor(count, maximum):
    return int(math.sin(count / 10) * (maximum / 2 + 1) + (maximum / 2))

#Menu loop
while True:
    #Clear
    screen.fill((0, 0, 0))

    #Draw code
    for i in range(len(codes)):
        drawcode(codes[i][0], codes[i][1], (0, calccolor(framecount + (i * 30), 100), 0))

    #Draw menu
    menu_offset += ((menuitem * 60) - menu_offset) * 0.6
    screen.blit(image_title, image_title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100 - menu_offset)))
    image_play.set_alpha(255 - 0 if menuitem == 0 else 120)
    screen.blit(image_play, image_play.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - menu_offset)))
    image_exit.set_alpha(255 - 0 if menuitem == 1 else 120)
    screen.blit(image_exit, image_exit.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - menu_offset + 60)))
    screen.blit(image_arrow, image_arrow.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))

    #Fade if an option was selected
    if (running is False):
        alphaSurface.set_alpha(alphaSurface.get_alpha() + 7)
        screen.blit(alphaSurface, (0, 0))
        if (alphaSurface.get_alpha() > 253):
            break

    #Update screen
    pygame.display.update()

    #Scroll code
    if (random.randint(0, 2) == 0):
        words = words[1:] + words[:1]

    #Check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            running = False
            break
        if running is True and event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            menuitem = menuitem - 1
            if menuitem == -1:
                menuitem = 1
        if running is True and event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            menuitem = menuitem + 1
            if menuitem == 2:
                menuitem = 0
        if running is True and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            running = False

    #Tick
    framecount+= 1
    clock.tick_busy_loop(60)

#Initialize game
player = nullfighter_sprites.Ship(SCREEN_WIDTH / 2, SCREEN_HEIGHT)
player.move(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 200)
player_bullets = []
stars = []
particles = []
next_lightning = framecount + 210
lightning_opacity = 0
lightning_x = 0
lightning_y = 0
next_enemy = framecount + 200
enemies = []

#Create game surfaces
image_lightning_1 = pygame.transform.scale(pygame.image.load("lightning_1.png"), (512, 512)).convert()
surf_size = image_lightning_1.get_size()
scale_size = (int(surf_size[0] * .1), int(surf_size[1] * .1))
image_lightning_1_blur = pygame.transform.smoothscale(image_lightning_1, scale_size)
image_lightning_1_blur = pygame.transform.smoothscale(image_lightning_1_blur, surf_size)

if (menuitem == 1):
    pass
else:
    running = True
    #Game loop
    while running:
        #Clear
        screen.fill((0, 0, 0))

        #Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x-= 12
        if keys[pygame.K_RIGHT]:
            player.x+= 12
        if keys[pygame.K_UP]:
            player.y = SCREEN_HEIGHT - 300
        elif keys[pygame.K_DOWN]:
            player.y = SCREEN_HEIGHT - 100
        else:
            player.y = SCREEN_HEIGHT - 200

        #Game logic
        stars = [star for star in stars if star.check_bounds(screen) is False]
        player_bullets = [bullet for bullet in player_bullets if bullet.check_bounds(screen) is False]
        particles = [particle for particle in particles if particle.check_bounds(screen) is False]
        if framecount % 5 == 0:
            stars.append(nullfighter_sprites.Star(random.randint(0, SCREEN_WIDTH), random.randint(3, 15), random.randint(15, 40)))

        hit = None
        for enemy in enemies:
            for bullet in player_bullets:
                if enemy.hit(bullet):
                    hit = (bullet, enemy)
                    for i in range(random.randint(15, 30)):
                        particles.append(nullfighter_sprites.BasicParticle(enemy.rect.x + (enemy.rect.width / 2), enemy.rect.y + (enemy.rect.height / 2), random.randint(-5, 5), random.randint(-5, 5), random.randint(5, 15), (255, 0, 0)))
                    break
            if hit is not None:
                break
        if hit is not None:
            player_bullets.remove(hit[0])
            enemies.remove(hit[1])
            
        if framecount == next_lightning:
            lightning_x = random.randint(0, SCREEN_WIDTH - image_lightning_1.get_width())
            next_lightning+= random.randint(100, 200)
            lightning_y = random.randint(-200, 0)
            lightning_opacity = 255
            if (bool(random.getrandbits(1)) == True):
                image_lightning_1 = pygame.transform.flip(image_lightning_1, True, False)
                image_lightning_1_blur = pygame.transform.flip(image_lightning_1_blur, True, False)

        if framecount == next_enemy:
            enemy = nullfighter_sprites.Enemy(random.randint(0, SCREEN_WIDTH), -30, random.randint(1, 2))
            enemy.move(enemy.x + random.randint(-5, 5), random.randint(10, 300))
            enemies.append(enemy)
            next_enemy+= random.randint(50, 150)

        #Draw game
        image_lightning_1.set_alpha(lightning_opacity)
        image_lightning_1_blur.set_alpha(lightning_opacity)
        lightning_opacity-= 8
        screen.blit(image_lightning_1_blur, (lightning_x, lightning_y))
        screen.blit(image_lightning_1, (lightning_x, lightning_y))

        for x in range(int(player.rect.x - 5), int(player.rect.x + 5), 3): #Cool thruster effects lol
            pygame.draw.line(screen, (0, 255, 0), (x + (player.rect.width / 2), player.rect.y + 70), (x + (player.rect.width / 2), player.rect.y + 70 + random.randint(1, 15)), 3)

        for bullet in player_bullets:
            bullet.draw(screen)

        for star in stars:
            star.draw(screen)

        for shot in particles:
            shot.draw(screen)

        for enemy in enemies:
            enemy.draw(screen)
            
        player.draw(screen)
        
        #Update screen
        pygame.display.update()

        #Check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player_bullets.append(nullfighter_sprites.Bullet(player.rect.x, player.rect.y - 70))
                for i in range(random.randint(2, 5)):
                    particles.append(nullfighter_sprites.BasicParticle(player.rect.x + (player.rect.width / 2), player.rect.y, random.randint(-15, 15), random.uniform(-1.5, 0), random.randint(5, 15), (0, 255, 0)))

        #Tick
        framecount+= 1
        clock.tick_busy_loop(60)
    
pygame.quit()
