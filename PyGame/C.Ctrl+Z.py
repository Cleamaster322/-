import pygame

colorr = pygame.Color(255, 255, 255)

size = width, height = (300, 300)
screen = pygame.display.set_mode(size)
pygame.init()
mass_coord = []
running = True
x1, y1, w, h = 0, 0, 0, 0
drawing = False  # режим рисования выключен

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True 

            x1, y1 = event.pos
            w, h = 0,0

        if event.type == pygame.MOUSEBUTTONUP:
            mass_coord.append((x1,y1,w,h))
            drawing = False
            
        if event.type == pygame.MOUSEMOTION:
            w, h = event.pos[0] - x1, event.pos[1] - y1
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_LCTRL] and event.key == pygame.K_z :
                if len(mass_coord) != 0:
                    mass_coord.pop()
                    screen.fill((0, 0, 0))
                    for i in mass_coord:
                        pygame.draw.rect(screen, (255, 255, 255), ((i[0], i[1]), (i[2], i[3])), 5)
            pygame.display.flip()

    if drawing:
        screen.fill((0, 0, 0))
        for i in mass_coord:
            pygame.draw.rect(screen, (255, 255, 255), ((i[0], i[1]), (i[2], i[3])), 5)
        pygame.draw.rect(screen, (255, 255, 255), ((x1, y1), (w, h)), 5)
    pygame.display.flip()
    

pygame.quit()