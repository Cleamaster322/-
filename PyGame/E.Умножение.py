import pygame
from math import cos,sin,radians
import colorsys
White = pygame.Color(255, 255, 255)

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))
tone = 0

size = width, height = (900, 900)
screen = pygame.display.set_mode(size)

multip = 1
radius = 300
total = 360

fps = 60
clock = pygame.time.Clock()

running = True
flag_stop = False
while running:
    clock.tick(fps)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flag_stop = not flag_stop
    
    pygame.draw.circle(screen,hsv2rgb(tone,1,1),(width//2,height//2),radius,1)

    for i in range(total):

        x1 = int(cos(radians(i)) * 300) + height // 2
        y1 = int(sin(radians(i)) * 300) + height // 2.
        x2 = int(cos(radians(i*multip)) * 300) + height // 2
        y2 = int(sin(radians(i*multip)) * 300) + height // 2

        pygame.draw.line(screen,hsv2rgb(tone,1,1),[x1,y1],[x2,y2],1)

    if flag_stop == False:
        multip += 0.01
        tone +=0.001
    pygame.display.update()
    

pygame.quit()