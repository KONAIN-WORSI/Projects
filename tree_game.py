import pygame as pg
import math

pg.init()
info = pg.display.Info()
w, h = info.current_w, info.current_h
screen = pg.display.set_mode((w, h), pg.FULLSCREEN)
clock = pg.time.Clock()

def draw_tree(x, y, angle, depth, length, color_hue, spread_angle):
    if depth == 0: return

    x2 = x + math.cos(angle) * length
    y2 = y + math.sin(angle) * length

    color = pg.Color(0)
    color.hsva = (color_hue % 360, 100, 100, 100)

    pg.draw.line(screen, color, (x, y), (x2, y2), max(1, depth))

    new_len =  length * 0.75
    draw_tree(x2, y2, angle - spread_angle, depth - 1, new_len, color_hue + 15, spread_angle)
    draw_tree(x2, y2, angle + spread_angle, depth - 1, new_len, color_hue + 15, spread_angle)

running = True

while running:
    screen.fill((0,0,0))

    mx, my = pg.mouse.get_pos()

    mouse_angle = (mx / w) * math.pi
    start_hue = (my / h) * 360
    start_len = h / 4.5

    draw_tree(w // 2, h , -math.pi/2, 11, start_len, start_hue, mouse_angle)

    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            running = False

    pg.display.flip()
    clock.tick(60)

pg.quit()
