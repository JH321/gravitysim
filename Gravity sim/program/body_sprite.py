import pygame as pg
import body as b
import settings
import queue
import math
import Barnes_Hut_tree as bh

class Body_Sprite(pg.sprite.Sprite):
    '''
    The Body_Sprite object represents a body as a pygame Sprite object to be drawn.

    Args:
        mass (float): Represents the mass of the body, will be passed to the Body constructor.
        radius (int): Represents the radius of the body (the body is represented as a circle on the screen), will be passed to the Body constructor.
        pos (tuple): Represents the starting position of the body, will be passed to the Body constructor.
        vel (tuple): Represents the initial velocity of the body, will be passed to the Body constructor.
        in_place (Boolean): Determines whether the body is in place (unmovable), will be passed to the Body constructor.
    
    Attributes:
        body (body.Body): Holds the actual Body object that this Sprite object represents.
        image (pygame.Surface): The surface of the this Sprite object, can be drawn on.
        radius (int): The radius of the Body object being represented.
        rect (pygame.Rect): The rectangle representation of the image attribute.
        ptn_hist (queue.Queue): Holds the previous points of the Body object, used to draw the trace that the Body object makes on the screen.
    '''

    def __init__(self, mass, radius, pos, vel = (0, 0), in_place = False):
        #call parent constructor (Sprite)
        super().__init__()

        self.body = b.Body(mass, radius, pos, vel, in_place)
        self.radius = self.body.get_radius()

        #Necessary for pygame to recognize and draw this object as a sprite on the screen
        self.image = pg.Surface([self.radius * 2, self.radius * 2], pg.SRCALPHA)
        self.rect = self.image.get_rect(center=self.body.get_pos())
        
        #Draws the circle representation of the body on the Sprite's surface
        self.draw()


        self.ptn_hist = queue.Queue(maxsize=settings.MAX_LINES)
        if settings.MAX_LINES > 0:
            self.ptn_hist.put(self.rect.center)

      
    
    def get_body(self):
        '''
        Getter for the Body object.

        Returns:
            The Body object this Sprite object represents.
        '''
        return self.body

    def draw(self):
        '''
        Draws the circle representation of the Body on the Sprite surface.
        '''
        pg.draw.circle(self.image, self.body.get_color(), [self.radius, self.radius], self.radius)

    def draw_trace(self, screen, point_hist, new_point):
        '''
        Draws the trace formed by the movement of the Body on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the trace onto.
            point_hist (queue.Queue): The queue that contains the Body's previous coordinates.
            new_point (tuple): Represents the Body's most current coordinate.
        '''


        if point_hist.full():
            point_hist.get()

        #Only adds the current coordinate if it is more than 10 pixels away from the last coordinate in the history.
        #This is for optimization purposes.
        if point_hist.empty() or math.dist(point_hist.queue[-1], new_point) > 10:
            
            point_hist.put(new_point)

        prev_point = None

        #Draws a line on the screen for each pair of coordinates in the point history
        for point in list(self.ptn_hist.queue):
    
            if prev_point is None:
                prev_point = point
                continue
            pg.draw.line(screen, self.body.get_color(), prev_point, point, 1)
            prev_point = point



    def update(self, screen, body_sprite_group, dt):
        '''
        Updates the Sprite representing the Body by changing its current position.

        Args:
            screen (pygame.Surface): The surface to draw the Sprite and its traces onto.
            body_sprite_group (pygame.sprite.Group): The Sprite group that contains the Sprites representing all the bodies on the screen.
            dt (float): The change in time between screen refreshes.
        '''

        #Gets all the bodies represented on the screen as Body objects
        bodies = [sprite.get_body() for sprite in body_sprite_group]

        #Construct a Barnes Hut tree if settings.B_H_OPTIMIZATION is enabled
        if settings.B_H_OPTIMIZATION:
            body_tree = bh.B_H_Tree(bodies)
        else:
            body_tree = None

        #Updates the position of the Body object that this Sprite object represents
        self.body.update_pos(bodies, body_tree, dt)
        
        #Updates the position of the Sprite object to reflect the change in the Body Object's position
        self.rect.center = self.body.get_pos()
        new_pos = self.rect.center
        
        #Draw the trace of the body on the screen
        if settings.MAX_LINES > 0:
            self.draw_trace(screen, self.ptn_hist, new_pos)

        
       

        


