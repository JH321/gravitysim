import pygame as pg
import body as b
import settings
import queue
import math

class Body_Sprite(pg.sprite.Sprite):

    #body_group = []

    def __init__(self, mass, radius, pos, vel = (0, 0), in_place = False):
        #call parent constructor (Sprite)
        super().__init__()

        self.body = b.Body(mass, radius, pos, vel, in_place)
        self.image = pg.Surface([radius * 2, radius * 2], pg.SRCALPHA)
        
        
        self.radius = radius
        self.rect = self.image.get_rect(center=self.body.get_pos())
        
        
        self.draw()

        self.ptn_hist = queue.Queue(maxsize=settings.MAX_LINES)
        if settings.MAX_LINES > 0:
            self.ptn_hist.put(self.rect.center)

        #Body_Sprite.body_group.append(self.body)
    
    def get_body(self):
        return self.body

    def draw(self):
        pg.draw.circle(self.image, self.body.get_color(), [self.radius, self.radius], self.radius)

    def draw_trace(self, screen, point_hist, new_point):
        
        if point_hist.full():
            point_hist.get()
    
        if point_hist.empty() or math.dist(point_hist.queue[-1], new_point) > 10:
            
            point_hist.put(new_point)

        prev_point = None
        for point in list(self.ptn_hist.queue):
    
            if prev_point == None:
                prev_point = point
                continue
            pg.draw.line(screen, self.body.get_color(), prev_point, point, 1)
            prev_point = point



    def update(self, screen, body_sprite_group, dt):
        #print(self.rect.center)
        bodies = [sprite.get_body() for sprite in body_sprite_group]

        self.body.update_pos(bodies, dt)
        
        self.rect.center = self.body.get_pos()
        new_pos = self.rect.center
        
        if settings.MAX_LINES > 0:
            self.draw_trace(screen, self.ptn_hist, new_pos)

        
       

        


