from to_import import *
from colors import *
import pygame
import sys
import math
import random

pygame.init()

clock = pygame.time.Clock()
running = True

x_width = 1066
y_width = 800
win = pygame.display.set_mode((x_width, y_width))

color_list = color_switch(white, orange, 25)
color_list_2 = color_switch(orange, red, 26)
for i in color_list_2:
    color_list.append(i)
print(color_list)

class pixel(enemy):
    def display(self):
        self.rect = pygame.rect.Rect(self.x, self.y, self.size, self.size)
        #pygame.draw.rect(win, self.color, self.rect)
        pygame.draw.circle(win, self.color, (self.x, self.y), self.size)

number_n = 50

for j in range(number_n):
    pi_equiv = (j/number_n)*math.pi
    actual_x = (j*(x_width))/number_n + 10
    actual_y = math.sin(pi_equiv)*y_width
    pixel(x=actual_x, y=actual_y, size=5, tic=j, color_tic=j)


while running:
    clock.tick(60)

    for event in pygame.event.get():
         if event.type == pygame.QUIT:
            running = False
            sys.exit()

    win.fill(blue)

    for i in list_of_class:
        i.tic += 0.05
        if i.direction == 0:
            i.color_tic += 0.5
            i.color = color_list[int(i.color_tic)]
        elif i.direction == 1:
            i.color_tic -= 0.5
            i.color = color_list[int(i.color_tic)]
        i.y = ((math.sin((i.tic/number_n)*math.pi*2)*y_width)/6)+(y_width/2)
        i.size = 10

        if int(i.color_tic) == 50:
            i.direction = 1
        if int(i.color_tic) == 0:
            i.direction = 0

        i.display()



    pygame.display.update()