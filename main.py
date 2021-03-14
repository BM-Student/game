import pygame, sys, random, os

black = (34, 40, 49)
blue = (48, 71, 94)
orange = (242, 163, 101)
white = (236, 236, 236)
light_blue = (112, 159, 176)
yellow = (251, 238, 172)
red = (140, 43, 29)
dark_purple = (130, 38, 89)
light_purple = (227, 107, 174)

# highscore file
HScore_file = 'highscore.txt'
if os.path.exists(HScore_file) == False:
    f = open(HScore_file, 'w')
    f.write('highscore: 0')
    f.close()

pygame.init()

music = pygame.mixer.music.load('Kubbi - Digestive biscuit.mp3')
pygame.mixer.music.set_volume(0.03)
pygame.mixer.music.play(-1)

dash_sound = pygame.mixer.Sound('Dash_shootingGame.wav')
dash_sound.set_volume(0.04)

death_sound = pygame.mixer.Sound('Death.wav')
death_sound.set_volume(0.04)

hitenemy_sound = pygame.mixer.Sound('Hit_enemy.wav')
hitenemy_sound.set_volume(0.3)

shoot_sound = pygame.mixer.Sound('Shoot.wav')
shoot_sound.set_volume(0.3)

pygame.font.init()
font_small = pygame.font.SysFont('arialblack', 20)
font_large = pygame.font.SysFont('arialblack', 60)
font_tiny = pygame.font.SysFont('arialblack', 15)

x_width = 1066
y_width = 800
win = pygame.display.set_mode((x_width, y_width))

pygame.mouse.set_visible(False)
pygame.mouse.set_pos(400, 400)

enemy_spawn_list = [((1/2) * x_width, 0), ((1/2) * x_width, y_width), (0, (1/2)*y_width), (x_width,(1/2)*y_width)]
projectiles = []
particles = []
enemies = []
explosion_particles = []

def enemy_spawn(lst, n):
    if len(enemies) < n:
        random_spot = random.choice(lst)
        Enemy(random_spot[0], random_spot[1], 5)

def color_switch(start, end, n):
    color_list = [start]
    direction_vector = [start[0] - end[0], start[1] - end[1], start[2] - end[2]]
    step_vector = [direction_vector[0]*(1/n), direction_vector[1]*(1/n), direction_vector[2]*(1/n)]
    for step in range(1, n):
        step_forward = (int(start[0] - (step_vector[0] * step)), int(start[1] - (step_vector[1] * step)),
                        int(start[2] - (step_vector[2] * step)))
        color_list.append(step_forward)
    color_list.append(end)

    return color_list


class Wall:
    def __init__(self, x, y, depth, width, color):
        self.x = x
        self.y = y
        self.width = width
        self.depth = depth
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.depth, self.width)

    def display(self):
        pygame.draw.rect(win, self.color, self.rect)

class pBullet:
    def __init__(self, x, y, vel, color, damage):
        self.x = x
        self.y = y
        self.vel = vel
        self.color = color
        self.damage = damage
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        projectiles.append(self)

    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, 10, 10)

        self.x += self.vel[0]
        self.y += self.vel[1]
        pygame.draw.rect(win, self.color, self.rect)

        x_adjust = 10
        y_adjust = 10

        Particle(random.randint(int(self.x - x_adjust), int(self.x + x_adjust)),
                 random.randint(int(self.y - y_adjust), int(self.y + y_adjust)), 5, self.color, 0.1)

        if len(projectiles) > 20:
            projectiles.pop(0)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.alive = True
        self.health = 3

        self.score = 0

    def shoot(self):
        speed = 10
        direction = [mouse_x - self.x, mouse_y - self.y]
        length = (direction[0]**2 + direction[1]**2) ** 0.5
        velocity = [direction[0] * (speed / length), direction[1] * (speed / length)]
        pBullet(self.x, self.y, (velocity[0], velocity[1]), orange, 10)

    def display(self):
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        pygame.draw.rect(win, orange, self.rect)

class Particle:
    def __init__(self, x, y, size, color, rate_of_decay = 1, decay_color = white):
        self.x = x
        self.y = y
        self.color = color
        self.colors =color_switch(color, decay_color, int((size / rate_of_decay - 1)/2))
        self.rate_of_decay = rate_of_decay
        self.vel = [0,0]
        self.size = size

        self.color_tick = 0
        particles.append(self)

    def display(self):
        self.x += int(self.vel[0])
        self.y += int(self.vel[1])

        self.size -= self.rate_of_decay

        if self.size <= 0:
            particles.remove(self)
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        try:
            pygame.draw.rect(win, self.colors[self.color_tick], rect)
        except IndexError:
            pygame.draw.rect(win, self.colors[-1], rect)
        self.color_tick += 1

class Enemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

        self.rect = pygame.Rect(self.x, self.y, 10, 10)

        enemies.append(self)

    def display(self, target):
        direction_vect = ((target.x + 10 - self.x), (target.y + 10 - self.y))
        length = ((direction_vect[0] ** 2) + (direction_vect[1] ** 2)) ** (0.5)
        try:
            unit_vect = (direction_vect[0] / length, direction_vect[1] / length)
        except ZeroDivisionError:
            unit_vect = (direction_vect[0] / (length + 0.1), direction_vect[1] / (length + 0.1))
        approach_vect = (unit_vect[0] * self.speed, unit_vect[1] * self.speed)

        self.x += approach_vect[0]
        self.y += approach_vect[1]

        self.rect = pygame.Rect(self.x, self.y, 18, 18)
        pygame.draw.rect(win, white, self.rect)

        for i in projectiles:
            if self.rect.colliderect(i.rect):
                hitenemy_sound.play()
                target.score += 1
                try:
                    enemies.remove(self)
                except ValueError:
                    print('error')
                    pass

playr = Player(x_width/2, y_width/2)

count = 0
shoot_cooldown = 0
dash_cooldown = 0
wave = 1

player_has_died = False

clock = pygame.time.Clock()
running = True

# Game Border
x_wall1 = Wall(0, 0, 25, y_width, light_blue)
x_wall2 = Wall(x_width - 25, 0, 25, y_width, light_blue)
y_wall1 = Wall(0, 0, x_width, 25, light_blue)
y_wall2 = Wall(0, y_width - 25, x_width, 25, light_blue)
wall_list = [x_wall1, x_wall2, y_wall1, y_wall2]

while running:
    count += 1
    for i in range(1, 9):
        if count > i*500 and wave == i:
            wave += 1
    enemy_spawn(enemy_spawn_list, wave)

    if shoot_cooldown > 0:
        shoot_cooldown += 1

    if shoot_cooldown >= 20:
        shoot_cooldown = 0

    clock.tick(50)
    for event in pygame.event.get():
         if event.type == pygame.QUIT:
            running = False
            sys.exit()

    win.fill(blue)

    target_pos = pygame.mouse.get_pos()
    mouse_x = int(target_pos[0])
    mouse_y = int(target_pos[1])

    pygame.draw.circle(win, orange, target_pos, 5, 0)
    if pygame.mouse.get_pressed(num_buttons=3)[0] and shoot_cooldown == 0 and playr.alive:
        shoot_cooldown += 1
        shoot_sound.play()
        playr.shoot()

    playr.display()

    keys = pygame.key.get_pressed()
    if playr.alive:
        if dash_cooldown == 0 and keys[pygame.K_SPACE]:
            dash_sound.play()
            dash_cooldown += 1

        if dash_cooldown > 0:
            dash_cooldown += 1
            if dash_cooldown > 50:
                dash_cooldown = 0

        if dash_cooldown > 0 and dash_cooldown < 15:
            if keys[pygame.K_a]:
                playr.x += -20
                for i in range(2):
                    Particle(playr.x + 10, random.randint(playr.y, playr.y + 20), 5, orange, 0.1)
            elif keys[pygame.K_d]:
                playr.x += 20
                for i in range(2):
                    Particle(playr.x + 10, random.randint(playr.y, playr.y + 20), 5, orange, 0.1)

            if keys[pygame.K_w]:
                playr.y += -20
            elif keys[pygame.K_s]:
                playr.y += 20

            # Just for particles
            if keys[pygame.K_w] and not keys[pygame.K_a] and not keys[pygame.K_d]:
                for i in range(2):
                    Particle(random.randint(playr.x, playr.x + 20), playr.y + 10, 5, orange, 0.1)
            elif keys[pygame.K_s] and not keys[pygame.K_a] and not keys[pygame.K_d]:
                for i in range(2):
                    Particle(random.randint(playr.x, playr.x + 20), playr.y + 10, 5,  orange, 0.1)

        if dash_cooldown >= 20 or dash_cooldown <= 0:
            if keys[pygame.K_a]:
                playr.x += -5
                for i in range(1):
                    Particle(playr.x + 10, random.randint(playr.y, playr.y + 20), 5,  orange, 0.1)
            elif keys[pygame.K_d]:
                playr.x += 5
                for i in range(1):
                    Particle(playr.x + 10, random.randint(playr.y, playr.y + 20), 5,  orange, 0.1)

            if keys[pygame.K_w]:
                playr.y += -5
            elif keys[pygame.K_s]:
                playr.y += 5

            # Just for particles
            if keys[pygame.K_w] and not keys[pygame.K_a] and not keys[pygame.K_d]:
                for i in range(1):
                    Particle(random.randint(playr.x, playr.x + 20), playr.y + 10, 5,  orange, 0.1)
            elif keys[pygame.K_s] and not keys[pygame.K_a] and not keys[pygame.K_d]:
                for i in range(1):
                    Particle(random.randint(playr.x, playr.x + 20), playr.y + 10, 5,  orange, 0.1)

    # drawing everything
    for i in projectiles:
        i.draw()
    for i in particles:
        i.display()
    for i in enemies:
        i.display(playr)
    for i in wall_list:
        i.display()
    for i in explosion_particles:
        i.display()

    # player collision with enemies
    for i in enemies:
        if playr.rect.colliderect(i.rect) and playr.alive:
            death_sound.play()
        if playr.rect.colliderect(i.rect):
            wave = 1
            count = 1
            playr.health -= 1
            if playr.health == 0:
                pBullet(playr.x, playr.y, (10, 0), orange, 10)
                pBullet(playr.x, playr.y, (5, 5), orange, 10)
                pBullet(playr.x, playr.y, (-10, 0), orange, 10)
                pBullet(playr.x, playr.y, (-5, 5), orange, 10)
                pBullet(playr.x, playr.y, (0, 10), orange, 10)
                pBullet(playr.x, playr.y, (5, -5), orange, 10)
                pBullet(playr.x, playr.y, (0, -10), orange, 10)
                pBullet(playr.x, playr.y, (-5, -5), orange, 10)
            if playr.alive:
                playr.x = (x_width / 2)
                playr.y = (y_width / 2)
            for i in enemies:
                try:
                    enemies.remove(i)
                except ValueError:
                    pass

    # damage resets
    if playr.health >= 1:
        rect_30 = pygame.Rect(30, 30, 50, 25)
        rect_31 = pygame.Rect(32, 32, 46, 21)
        pygame.draw.rect(win, orange, rect_30)
        pygame.draw.rect(win, red, rect_31)

    if playr.health >= 2:
        rect_30 = pygame.Rect(85, 30, 50, 25)
        rect_31 = pygame.Rect(87, 32, 46, 21)
        pygame.draw.rect(win, orange, rect_30)
        pygame.draw.rect(win, red, rect_31)

    if playr.health >= 3:
        rect_30 = pygame.Rect(140, 30, 50, 25)
        rect_31 = pygame.Rect(142, 32, 46, 21)
        pygame.draw.rect(win, orange, rect_30)
        pygame.draw.rect(win, red, rect_31)

    # the dash bar
    if playr.alive:
        rect_dash_bar_0 = pygame.Rect(30, 60, 160, 25)
        if dash_cooldown != 0:
            rect_dash_bar_1 = pygame.Rect(34, 64, 3*dash_cooldown, 17)
        else:
            rect_dash_bar_1 = pygame.Rect(34, 64, 152, 17)
        pygame.draw.rect(win, orange, rect_dash_bar_0)
        pygame.draw.rect(win, dark_purple, rect_dash_bar_1)

    # death
    if playr.health == 0:
        playr.alive = False
        playr.x = x_width + 100
        playr.y = y_width + 100

    # border collision
    if playr.y < 25 and playr.alive:
        playr.y = 25
    if playr.y > y_width - 45 and playr.alive:
        playr.y = y_width - 45
    if playr.x < 25 and playr.alive:
        playr.x = 25
    if playr.x > x_width - 45 and playr.alive:
        playr.x = x_width - 45

    # Text displaying the current wave and score
    if playr.alive:
        wave_display = font_small.render('Wave: {}'.format(str(wave)), True, white)
        win.blit(wave_display, (int(x_width/2 - 30), 30))
        score_display = font_tiny.render('Score: {}'.format(str(playr.score)), True, white)
        win.blit(score_display, (int(x_width/2 - 20), 60))

    # Game over screen
    if playr.alive is False:
        highscore = open(HScore_file).read()[11:]
        if playr.score > int(highscore):
            f = open(HScore_file, 'w')
            f.write('highscore: {}'.format(str(playr.score)))
            highscore = str(playr.score)
            f.close()
        cursor_rect = pygame.Rect(mouse_x, mouse_y, 10, 10)

        rect_flair_1 = pygame.Rect(int(x_width / 8), int(y_width/4), int(x_width * (3 / 4)), 10)
        rect_flair_2 = pygame.Rect(int(x_width / 8), int(y_width * (3 / 4)), int(x_width * (3 / 4)), 10)

        rect_flair_3 = pygame.Rect(int(x_width/8 + 30), int(y_width/2), 180, 90)
        rect_flair_4 = pygame.Rect(int(x_width * (3 / 4) - 70), int(y_width / 2), 180, 90)

        gameover_text = font_large.render('Play Again?'.format(str(wave)), True, white)

        yes_text = font_large.render('Yes', True, white)
        no_text = font_large.render('No', True, white)

        score_text = font_small.render('Your Score: {}'.format(playr.score), True, white)
        highscore_text = font_small.render('High Score: {}'.format(highscore), True, white)

        if cursor_rect.colliderect(rect_flair_3):
            pygame.draw.rect(win, light_blue, rect_flair_3)
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                playr.health = 3
                playr.alive = True
                playr.x = (x_width/2)
                playr.y = (y_width/2)
                wave = 1
                playr.score = 0
        if cursor_rect.colliderect(rect_flair_4):
            pygame.draw.rect(win, light_blue, rect_flair_4)
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                running = False

        win.blit(gameover_text, (int(x_width/2 - 180), int(y_width/4 + 30)))
        win.blit(yes_text, (int(x_width/8 + 60), int(y_width/2)))
        win.blit(no_text, (int(x_width * (3 / 4) - 20), int(y_width / 2)))

        win.blit(score_text, (int(x_width/2 - 80), int(y_width/2)))
        win.blit(highscore_text, (int(x_width / 2 - 80), int(y_width / 2 + 30)))

        pygame.draw.rect(win, white, rect_flair_1)
        pygame.draw.rect(win, white, rect_flair_2)

    pygame.display.update()