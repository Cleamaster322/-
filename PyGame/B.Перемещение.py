import pygame

colorr = pygame.Color(255, 255, 255)

size = width, height = (300, 300)
screen = pygame.display.set_mode(size)
pygame.init()

running = True
flag = False #Флаг на рисование квадрата
coord = (0,0)
pygame.draw.rect(screen, pygame.color.Color('white'), (coord[0], coord[1],30,30))
pygame.display.flip()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] >=coord[0] and event.pos[0] < coord[0] + 30 or event.pos[1] >coord[1] and event.pos[1] <= coord[1] + 30 == True: 
                flag = True

        if event.type == pygame.MOUSEBUTTONUP:
            flag = False
        
        if flag == True:
            coord = (event.pos[0],event.pos[1])
            screen.fill((0, 0, 0))
            pygame.draw.rect(screen, pygame.color.Color(colorr), (coord[0], coord[1],30,30))
            pygame.display.flip()
    

pygame.quit()