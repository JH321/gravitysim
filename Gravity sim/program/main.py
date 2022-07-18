import operator
import sys
import pygame as pg
import settings
import body as b
import body_sprite as bs
import math
import random

class Game():

    def __init__(self):
        pg.init()
        
        self.base_font = pg.font.SysFont('Arial', 12)
        self.body_sprite_group = pg.sprite.Group()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    Game.quit()
            self.menu()
            self.run()

    def menu(self):
        
        screen = pg.display.set_mode(size = settings.DIMENSIONS)
        running = True

        circular_but = pg.Rect(100, 100, 100, 25)
        circle_but_text = self.base_font.render("Circular orbit", True, settings.BLACK)

        elliptical_but = pg.Rect(250, 100, 100, 25)
        ellipse_but_text = self.base_font.render("Elliptical orbit", True, settings.BLACK)

        random_mass_but = pg.Rect(250, 200, 100, 25)
        random_mass_active = False

        n_but = pg.Rect(100, 300, 100, 25)
        n_but_text = self.base_font.render("n-bodies", True, settings.BLACK)
        
        n_text_box_label = self.base_font.render("Enter n for n-bodies sim", True, settings.BLACK)
        n_text_box = pg.Rect(250, 300, 100, 25)

        n_text_box_active = False
        n_text = ""

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    Game.quit()
                
                if event.type == pg.KEYDOWN:
                    if n_text_box_active:
                        if event.key == pg.K_BACKSPACE:
                            n_text = n_text[:-1]
                        else:
                            if event.unicode.isdigit() and len(n_text) < 14:
                                n_text += event.unicode
  
              
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    print(mouse_pos)
                    if circular_but.collidepoint(mouse_pos):
                        self.circular_orbit(random_mass_active)
                        running = False
                        break

                    if elliptical_but.collidepoint(mouse_pos):
                        self.elliptical_orbit()
                        running = False
                        break

                    if random_mass_but.collidepoint(mouse_pos):
                        random_mass_active = not random_mass_active

                    if n_but.collidepoint(mouse_pos):
                        try:
                            n = int(n_text)
                        except ValueError:
                            n = 2
                        
                        self.n_body(n, random_mass_active)
                        running = False
                        break
                        





                        
                    if n_text_box.collidepoint(mouse_pos):
                        if not n_text_box_active:
                            n_text_box_active = True
                    else:
                        n_text_box_active = False
                

            
            screen.fill(settings.MENU_COLOR)

            pg.draw.rect(screen, settings.WHITE, circular_but)
            screen.blit(circle_but_text, circular_but.topleft)

            pg.draw.rect(screen, settings.WHITE, elliptical_but)
            screen.blit(ellipse_but_text, elliptical_but.topleft)

            pg.draw.rect(screen, settings.WHITE, n_but)
            screen.blit(n_but_text, n_but.topleft)

            if not random_mass_active:
                random_mass_but_text = self.base_font.render("Enable random masses", True, settings.BLACK)
            else:
                random_mass_but_text = self.base_font.render("Disable random masses", True, settings.BLACK)
            pg.draw.rect(screen, settings.WHITE, random_mass_but)
            screen.blit(random_mass_but_text, random_mass_but.topleft)

            color = settings.WHITE
            if n_text_box_active:
                color = (255, 235, 205)
            pg.draw.rect(screen, color, n_text_box)
            n_text_box_text = self.base_font.render(n_text, True, settings.BLACK)
            loc = (n_text_box.topleft[0], n_text_box.topleft[1] - n_text_box.size[1])
            screen.blit(n_text_box_label, loc)
            screen.blit(n_text_box_text, n_text_box.topleft)

            pg.display.flip()

    def circular_orbit(self, random_mass):
        if random_mass:
            m1 = random.randint(5, 200)
            m2 = random.randint(5, 200)
        else:
            m1 = 50
            m2 = 100
        
        r1 = m1 / 10
        r2 = m2 / 10
        pos_diff = 100 #100 pixel difference in position
        p1 = bs.Body_Sprite(m1, r1, (settings.WIDTH / 2 + pos_diff, settings.HEIGHT / 2), vel=(0, -math.sqrt((m2 * settings.G) / pos_diff)))
        p2 = bs.Body_Sprite(m2, r2, (settings.WIDTH / 2, settings.HEIGHT / 2), in_place = True)
        self.body_sprite_group.add(p1)
        self.body_sprite_group.add(p2)

    def elliptical_orbit(self):
        m1 = 50
        r1 = 5
        m2 = 100
        r2 = 10
        pos_diff = 100 #100 pixel difference in position
        p1 = bs.Body_Sprite(m1, r1, (settings.WIDTH / 2 + pos_diff, settings.HEIGHT / 2), vel=(0, -15))
        p2 = bs.Body_Sprite(m2, r2, (settings.WIDTH / 2, settings.HEIGHT / 2), in_place = True)
        self.body_sprite_group.add(p1)
        self.body_sprite_group.add(p2)
    
    def n_body(self, n_tot, random_mass):
        
        for n in range(n_tot):
            if random_mass:
                mass = random.randint(5, 200)
            else:
                mass = 50
            p1 = bs.Body_Sprite(mass, mass / 10, (random.randint(0, settings.WIDTH), random.randint(0, settings.HEIGHT)), vel=(random.randint(-20, 20), random.randint(-20, 20)))
            self.body_sprite_group.add(p1)

    def run(self):

        screen = pg.display.set_mode(size = settings.DIMENSIONS)
        running = True

        menu_but = pg.Rect(settings.WIDTH - 100, settings.HEIGHT - 25, 100, 25)
        menu_but_text = self.base_font.render("Menu return", True, settings.BLACK)

        


        clock = pg.time.Clock()

        while running:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    Game.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if menu_but.collidepoint(mouse_pos):
                        self.body_sprite_group.empty()
                        running = False
                        break
        
            screen.fill(settings.BLACK)

            pg.draw.rect(screen, settings.WHITE, menu_but)
            screen.blit(menu_but_text, menu_but.topleft)

            self.body_sprite_group.draw(screen)
            dt = clock.tick_busy_loop(settings.FPS) #time between refresh rates in ms

            #This ensures that when the screen is being moved for a long time, the time of the frame right before the screen is moved 
            #and the time of the frame right after the screen is placed is not accounted for in the sim
            if dt > 50:
                dt = 0
            print(dt)

            self.body_sprite_group.update(screen, self.body_sprite_group, dt / 1000)
            pg.display.flip()
            
    def quit():
        pg.display.quit()
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    Game()