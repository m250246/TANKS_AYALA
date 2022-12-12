import pygame, random, math
from load_save import load_image


def new_ground():
    MIN = 30
    MAX = 330

    angle = float(random.randint(0, 360))

    ground = {}
    ground[0] = random.randint(MIN, MAX - 20)
    elevation = float(ground[0])
    counter = 0
    ajustment = 0.0

    max_height = ground[0]

    i = 1
    while i < 800:
        if counter == 0:
            counter = random.randint(5, 40)
            ajustment = float(random.randint(-4, 6))
        if counter < 25:
            angle = angle + ajustment
        if angle >= 360.0:
            angle = 0.0
        elevation = elevation + math.cos(math.radians(angle)) * 1.5
        if elevation < MIN:
            angle = 280.0
            counter = random.randint(5, 20)
            ajustment = float(random.randint(1, 3))
        elif elevation > MAX:
            angle = 100.0
            counter = random.randint(5, 20)
            ajustment = float(random.randint(1, 3))
        if (75 <= i <= 125) or (675 <= i <= 725):
            elevation = float(ground[i - 1])
        else:
            elevation += ((random.random() * 4) - 2)
        ground[i] = int(elevation)
        if ground[i] > max_height:
            max_height = ground[i]
        counter -= 1
        i += 1
    return ground, max_height


def draw_ground(Game):
    surface = Game.screen
    ground = Game.ground
    for i in range(0, 800):
        pygame.draw.line(surface, (240, 255, 220), (i, 600 - ground[i]), (i, 599))
        pygame.draw.line(surface, (37, 45, 35), (i, 600 - ground[i]), (i, 600 - ground[i] + 2))
        pygame.draw.line(surface, (102, 124, 38), (i, 600 - ground[i] + 3), (i, 600 - ground[i] + 6))


def update_screen(Game):
    image = load_image('background.png', 'sprites')
    image = pygame.transform.scale(image, (1000, 600))
    Game.screen.blit(image, (0, 0))
    draw_ground(Game)
    return Game.screen.copy()
