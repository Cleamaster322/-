from typing import Counter
import pygame
import random
pygame.init()
font_name = pygame.font.match_font('arial')
class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.count_block = []
        self.mines = []
        self.gen_mines()
        
        
    def gen_mines(self):
        count = 5 #Кол-во мин
        i = 0
        while i != count:
            x = random.randint(0,self.width-1) *self.cell_size + self.left
            y = random.randint(0,self.height-1)*self.cell_size + self.top
            if (x,y) not in self.mines:
                self.mines.append((x,y))
                i+=1
        print(self.mines)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
    
    def draw_text(self, surf, text, size, x, y):
        font_name = pygame.font.match_font('arial')
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                x1 = self.left + self.cell_size * j
                y1 = self.left + self.cell_size * i
                x2 = self.cell_size
                y2 = self.cell_size
                pygame.draw.rect(screen,(255,255,255),((x1,y1),(x2,y2)),1)
                for elem in self.mines:
                    pygame.draw.rect(screen,(255,0,0),((elem),(x2,y2)))
                for elem in self.count_block:
                    self.draw_text(screen,f"{elem[2]}",15,elem[0]+self.cell_size//2,elem[1])
        
    def get_cell(self, mouse_pos):
        x,y = mouse_pos
        x_cell,y_cell = self.left,self.top
        if y > self.cell_size*self.height or x > self.cell_size*self.width or x<self.left or y < self.top: #Уход за границу поля
            return None
        while x_cell <x or y_cell <y:
            if x_cell<x:
                x_cell+=self.cell_size
            if y_cell<y:
                y_cell+=self.cell_size

        return(x_cell-self.cell_size,y_cell-self.cell_size)
    
    def add_turple(self,x,y,move):
        a,b =move[0],move[1]
        a *= self.cell_size
        b *= self.cell_size
        return x+a,y+b

    def check_mine(self,coord):
        count = 0
        x,y = coord[0],coord[1]
        move = [(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0)]
        for elem in move:
            tmp1,tmp2 = self.add_turple(x,y,elem)
            if (tmp1,tmp2) in self.mines:
                count +=1
        return count
        
    def on_click(self,mouse_pos):
        coords = self.get_cell(mouse_pos)
        if coords != None and coords not in self.mines:
            count = self.check_mine(coords)
            self.count_block.append((coords[0],coords[1],count))
            
size = width, height = (900, 900)
screen = pygame.display.set_mode(size)
running = True

board = Board(5, 7)
board.render(screen)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            a =board.on_click(mouse_pos)      
    screen.fill((0, 0, 0))
    board.render(screen)
    pygame.display.flip()


# for event in pygame.event.get():
#     if event.type == pygame.QUIT:
#         running = False                
# screen.fill((0, 0, 0))
# board.render(screen)
# pygame.display.flip()