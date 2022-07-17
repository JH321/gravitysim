import pygame as pg
import body as b
import settings
import sprites
import queue
import math

class Body_Sprite(pg.sprite.Sprite):
    body_group = pg.sprite.Group()
    bodies = []
    def __init__(self, mass, radius, pos, vel = (0, 0), in_place = False):
        #call parent constructor (Sprite)
        super().__init__()

        self.body = b.Body(mass, radius, pos, vel, in_place)
        self.image = pg.Surface([radius * 2, radius * 2], pg.SRCALPHA)
        
        
        self.radius = radius
        self.rect = self.image.get_rect(center=self.body.get_pos())
        
        
        self.draw()

        self.ptn_hist = queue.Queue(maxsize=settings.MAX_LINES)

        Body_Sprite.bodies.append(self.body)
        sprites.body_group.add(self)
    
    def get_body(self):
        return self.body

    def draw(self):
        pg.draw.circle(self.image, self.body.get_color(), [self.radius, self.radius], self.radius)

    def update(self, screen, dt):
        #print(self.rect.center)
        old_pos = self.rect.center
        if self.ptn_hist.empty():
            self.ptn_hist.put(old_pos)
        
        self.body.update_pos(Body_Sprite.bodies, dt)
        
        self.rect.center = self.body.get_pos()
        new_pos = self.rect.center
        
        if self.ptn_hist.full():
            self.ptn_hist.get()
        if math.dist(self.ptn_hist.queue[-1], new_pos) > 10:
            self.ptn_hist.put(new_pos)
        
        prev_point = None
        for point in list(self.ptn_hist.queue):
    
            if prev_point == None:
                prev_point = point
                continue
            pg.draw.line(screen, self.body.get_color(), prev_point, point, 1)
            prev_point = point

        


