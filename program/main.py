import operator
import sys
import pygame as pg
import settings
import body as b
import body_sprite as bs
import math
import random
import time

class Game():
    '''
    The Game object represents the simulation itself. It is necessary for the graphical element of the simulation and
    setting up the necessary objects for the simulation.

    Attributes:
        base_font (pygame.font.Font): Controls the base font used when drawing text to the screen.
        body_sprite_group (pygame.sprite.Group): A list of all the Sprites that each represent a Body object. 
    '''
    def __init__(self):
        #initialize pygame
        pg.init()
        
        self.base_font = pg.font.SysFont('Arial', 12)
        
        self.body_sprite_group = pg.sprite.Group()

        #main loop 
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    Game.quit()
            self.menu()
            self.run()

    def menu(self):
        '''
        Creates the menu for the program including all the buttons.
        '''

        #The main screen
        screen = pg.display.set_mode(size = settings.DIMENSIONS)
        running = True

        #The rectangle element of the button to start up a circular orbit
        circular_but = pg.Rect(100, 100, 100, 25)
        circle_but_text = self.base_font.render("Circular orbit", True, settings.BLACK)

        #The rectangle element of the button to start up a elliptical orbit
        elliptical_but = pg.Rect(250, 100, 100, 25)
        ellipse_but_text = self.base_font.render("Elliptical orbit", True, settings.BLACK)

        #The rectangle element of the button to set the random mass option
        random_mass_but = pg.Rect(250, 200, 150, 25)
        settings.RANDOM_MASS = False

        #The rectangle element of the button to set the Barnes Hut algorithm option
        enable_b_h_opt_but = pg.Rect(250, 250, 225, 25)
        settings.B_H_OPTIMIZATION = False

        #The rectangle element of the button to start up the n-body option
        n_but = pg.Rect(100, 300, 100, 25)
        n_but_text = self.base_font.render("n-bodies", True, settings.BLACK)
        
        #The rectangle element of the text box to take in the value of n from the user (n for the number of bodies to create in the sim)
        n_text_box = pg.Rect(250, 300, 100, 25)
        n_text_box_label = self.base_font.render("Enter n for n-bodies sim", True, settings.BLACK)
       

        #Variable to store whether the textbox is active and actively taking in user input from the keyboard
        n_text_box_active = False
        n_text = ""

        #menu loop
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    Game.quit()
                
                #For each keyboard press
                if event.type == pg.KEYDOWN:

                    #The functionality of the textbox to take in the value of n from the user
                    if n_text_box_active:
                        if event.key == pg.K_BACKSPACE:
                            n_text = n_text[:-1]
                        else:
                            if event.unicode.isdigit() and len(n_text) < 14:
                                n_text += event.unicode
  
                #For each mouse press
                if event.type == pg.MOUSEBUTTONDOWN:

                    mouse_pos = event.pos
                    #print(mouse_pos)

                    #These if statements check if a button or a text box has been clicked on,
                    #if so, the correct action is then taken. Setting running to False means
                    #that the menu loop is exited as well as this function. Then the run() function
                    #is running, and this is where the actual simulation is run.

                    if circular_but.collidepoint(mouse_pos):
                        self.circular_orbit()
                        running = False
                        break

                    if elliptical_but.collidepoint(mouse_pos):
                        self.elliptical_orbit()
                        running = False
                        break

                    if random_mass_but.collidepoint(mouse_pos):
                        settings.RANDOM_MASS = not settings.RANDOM_MASS
                    
                    if enable_b_h_opt_but.collidepoint(mouse_pos):
                        settings.B_H_OPTIMIZATION = not settings.B_H_OPTIMIZATION


                    if n_but.collidepoint(mouse_pos):
                        #a precaution so that a non integer input
                        #for n is not inadvertently taken in.
                        try:
                            n = int(n_text)
                        except ValueError:
                            n = 2
                        
                        self.n_body(n)
                        running = False
                        break
                
                    #Activates the textbox
                    if n_text_box.collidepoint(mouse_pos):
                        if not n_text_box_active:
                            n_text_box_active = True
                    else:
                        n_text_box_active = False
                

            
            screen.fill(settings.MENU_COLOR)

            #Draws the rectangle elements of the buttons and text boxes to the screen

            pg.draw.rect(screen, settings.WHITE, circular_but)
            screen.blit(circle_but_text, circular_but.topleft)

            pg.draw.rect(screen, settings.WHITE, elliptical_but)
            screen.blit(ellipse_but_text, elliptical_but.topleft)

            pg.draw.rect(screen, settings.WHITE, n_but)
            screen.blit(n_but_text, n_but.topleft)

            #Makes sure to correctly set the text for the enable random mass button
            if not settings.RANDOM_MASS:
                random_mass_but_text = self.base_font.render("Enable random masses", True, settings.BLACK)
            else:
                random_mass_but_text = self.base_font.render("Disable random masses", True, settings.BLACK)
            
            pg.draw.rect(screen, settings.WHITE, random_mass_but)
            screen.blit(random_mass_but_text, random_mass_but.topleft)

            #Makes sure to correctly set the text for the enable Barnes Hut optimization button
            if not settings.B_H_OPTIMIZATION:
                b_h_opt_but_text = self.base_font.render("Enable Barnes Hut Optimization masses", True, settings.BLACK)
            else:
                b_h_opt_but_text = self.base_font.render("Disable Barnes Hut Optimization masses", True, settings.BLACK)
            
            pg.draw.rect(screen, settings.WHITE, enable_b_h_opt_but)
            screen.blit(b_h_opt_but_text, enable_b_h_opt_but.topleft)

            #Changes the color of the text box for taking in the value of n based on whether the textbox is active
            if n_text_box_active:
                color = (255, 235, 205)
            else:
                color = settings.WHITE

            pg.draw.rect(screen, color, n_text_box)
            n_text_box_text = self.base_font.render(n_text, True, settings.BLACK)
            loc = (n_text_box.topleft[0], n_text_box.topleft[1] - n_text_box.size[1] + 10)
            screen.blit(n_text_box_label, loc)
            screen.blit(n_text_box_text, n_text_box.topleft)

            pg.display.flip()

    def circular_orbit(self):
        '''
        Sets up the simulation for a circular orbit.
        '''
        
        #Creates random masses for the bodies if settings.RANDOM_MASS is True
        if settings.RANDOM_MASS:
            m1 = random.randint(5, 200)
            m2 = random.randint(5, 200)
        else:
            m1 = 50
            m2 = 100
        
        r1 = m1 / 10
        r2 = m2 / 10
        pos_diff = random.randint(50, 100) #pixel difference in position

        p1 = bs.Body_Sprite(m1, r1, (settings.WIDTH / 2 + pos_diff, settings.HEIGHT / 2), vel=(0, -math.sqrt((m2 * settings.G) / pos_diff)))
        p2 = bs.Body_Sprite(m2, r2, (settings.WIDTH / 2, settings.HEIGHT / 2), in_place = True)
        self.body_sprite_group.add(p1)
        self.body_sprite_group.add(p2)

    def elliptical_orbit(self):
        '''
        Sets up the simulation for an elliptical orbit.
        '''

        m1 = 50
        r1 = 5
        m2 = 100
        r2 = 10
        pos_diff = 100 #100 pixel difference in position
        p1 = bs.Body_Sprite(m1, r1, (settings.WIDTH / 2 + pos_diff, settings.HEIGHT / 2), vel=(0, -15))
        p2 = bs.Body_Sprite(m2, r2, (settings.WIDTH / 2, settings.HEIGHT / 2), in_place = True)
        self.body_sprite_group.add(p1)
        self.body_sprite_group.add(p2)
    
    def n_body(self, n_tot):
        '''
        Sets up the n body simulation with the value of n given as a parameter.

        Args:
            n_tot (int): the value of n that represents the number of bodies to generate in the simulation.
        '''
        #start = time.time()

        for n in range(n_tot):
            if settings.RANDOM_MASS:
                mass = random.randint(5, 200)
            else:
                mass = 50
            p1 = bs.Body_Sprite(mass, mass / 10, (random.randint(0, settings.WIDTH), random.randint(0, settings.HEIGHT)), vel=(random.randint(-20, 20), random.randint(-20, 20)))
            self.body_sprite_group.add(p1)

        #end = time.time()

        #print("to create sprites ", (end - start) * 1000)

    def run(self):
        '''
        Runs the actual simulation.
        '''

        #print(settings.B_H_OPTIMIZATION)

        screen = pg.display.set_mode(size = settings.DIMENSIONS)
        running = True

        #The rectangle element of the button that will stop the simulation and return to the menu screen
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
                    
                    #When a user clicks on the screen, a body will be generated at the mouse point
                    if settings.RANDOM_MASS:
                        mass = random.randint(5, 200)
                    else:
                        mass = 50
                    p1 = bs.Body_Sprite(mass, mass / 10, mouse_pos, vel=(random.randint(-20, 20), random.randint(-20, 20)))
                    self.body_sprite_group.add(p1)
                    
        
            screen.fill(settings.BLACK)

            #Draws the return to menu button on the screen
            pg.draw.rect(screen, settings.WHITE, menu_but)
            screen.blit(menu_but_text, menu_but.topleft)

            #Draws all the bodies onto the screen
            self.body_sprite_group.draw(screen)
            
            #Both controls the maximum updates per second and gets the time between screen updates.
            #This acceleration during the time between screen updates is approximated to be constant.

            dt = clock.tick_busy_loop(settings.FPS) #time between refresh rates in ms
            #print(dt)
           

            self.body_sprite_group.update(screen, self.body_sprite_group, dt / 1000)
            pg.display.flip()
        
        #Resets the max depth achieved by the Barnes Hut tree
        print("maxdepth: ", settings.MAX_DEPTH_ACHIEVED)
        settings.MAX_DEPTH_ACHIEVED = 0
        
    def quit():
        '''
        Makes sure to exit the program cleanly.
        '''
        pg.display.quit()
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    Game()