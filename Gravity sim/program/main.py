import sys
import pygame as pg
import settings
import body as b
import body_sprite as bs
import sprites

def quit():
    pg.display.quit()
    pg.quit()
    sys.exit()

def main():
    pg.init()
    screen = pg.display.set_mode(size = settings.DIMENSIONS)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
        run(screen)
def run(screen):
    running = True

    clock = pg.time.Clock()

    p1 = bs.Body_Sprite(50, 5, (settings.WIDTH / 2 + 100, settings.HEIGHT / 2), vel=(0, -10))
    p2 = bs.Body_Sprite(50, 5, (settings.WIDTH / 2, settings.HEIGHT / 2), vel= (0, 0), in_place = True)
    #p3 = bs.Body_Sprite(50, 5, (200, 200), vel = (5, -10))
    '''bs.Body_Sprite(50, 5, (42, 24), vel = (5, -10))
    bs.Body_Sprite(50, 5, (24, 530), vel = (5, -10))
    bs.Body_Sprite(50, 5, (52, 343), vel = (5, -10))
    bs.Body_Sprite(50, 5, (200, 270), vel = (5, -10))
    bs.Body_Sprite(50, 5, (220, 290), vel = (5, -10))
    bs.Body_Sprite(50, 5, (160, 250), vel = (5, -10))'''
    

    sprite_group = sprites.body_group
    #bodies = [p1, p2, p3, b.Body(500, 5, (400, 200), vel = (20, -10)), b.Body(50, 5, (500, 300), vel = (20, -10)), b.Body(50, 5, (600, 200), vel = (20, -10))]
    #bodies = [p1, p2]

    #pixel_arr = pg.PixelArray(screen)
    while running:
        hold = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
        
        if hold:
            continue
        screen.fill((0, 0, 0))
        sprite_group.draw(screen)
        dt = clock.tick(settings.FPS) / 1000
        print(dt)
        sprite_group.update(screen, dt)
        pg.display.flip()
        


if __name__ == "__main__":
    main()