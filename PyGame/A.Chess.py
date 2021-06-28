import pygame as pg
while True:
    print("Введите размер экрана и кол-во клеток")
    tmp1,tmp2 = map(int,input().split())
    if tmp1 % tmp2 == 0:
        step = tmp1 // tmp2
        break
    elif tmp2 % tmp1 == 0:
        step = tmp2 // tmp1
        break
    print("Ошибка кратности")

pg.init()
# размеры окна
size = width, height = tmp1, tmp1
# screen — холст, на котором рисуем
screen = pg.display.set_mode(size)
for i in range(tmp2):
    for j in range(tmp2):
        if (i+j) % 2 == 0:
            pg.draw.rect(screen, pg.color.Color('black'), (j*step, i*step, step,step))
        else:
            pg.draw.rect(screen, pg.color.Color('white'), (j*step, i*step, step,step))
# отрисовка кадра
pg.display.flip()
# ожидание закрытия окна
while pg.event.wait().type != pg.QUIT:
    pg.display.flip()
# завершение работы
pg.quit()