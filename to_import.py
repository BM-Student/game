import pygame
from colors import *

list_of_class = []

class enemy():
    def __init__(self, x, y, size, tic, color_tic, color=white):
        list_of_class.append(self)
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.rect = pygame.rect.Rect(self.x, self.y, self.size, self.size)
        self.tic = tic
        self.color_tic = color_tic
        self.direction = 0

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