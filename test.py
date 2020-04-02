import pygame
import random


def random_color ():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

def is_rect(pos,rect):
    x,y =pos
    rx,ry,rw,rh = rect
    if (rx <= x <=rx+rw)and(ry <= y <= ry +rh):
        return True
    return False

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((600,400))
    screen.fill((255,255,255))
    rect = {
        'rect': [100, 100, 100, 100],
        'color': random_color()
    }
    pygame.draw.rect(screen, rect['color'], rect['rect'])
    pygame.display.flip()

    is_move = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_rect(event.pos, rect['rect']):
                    is_move = True

            if event.type == pygame.MOUSEBUTTONUP:
                is_move = False

            if event.type == pygame.MOUSEMOTION:
                if is_move:
                    screen.fill((255, 255, 255))
                    rect['rect'][0] += event.rel[0]
                    rect['rect'][1] += event.rel[1]
                    pygame.draw.rect(screen, rect['color'], rect['rect'])
                    pygame.display.update()

