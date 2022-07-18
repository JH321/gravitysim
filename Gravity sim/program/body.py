import settings
import operator
import math
import random

class Body:

    color = []

    def __init__(self, mass, radius, pos, vel = (0, 0), in_place = False):
        self.mass = mass

        self.pos = pos

        self.vel = vel

        self.accel = (0, 0)

        self.radius = radius

        self.in_place = in_place

        self.color = Body.generate_new_color()

    def generate_new_color():
        new_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        while new_color in Body.color or new_color < (10, 10, 10):
            new_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        Body.color.append(new_color)

        return new_color

    def get_mass(self):
        return self.mass

    def get_pos(self):
        return self.pos
    
    def update_pos(self, bodies, dt = 1):
        if not self.in_place:
            delta_pos = tuple(el * dt for el in self.get_vel())
            self.pos = tuple(map(sum, zip(self.pos, delta_pos)))
            self.update_vel(bodies, dt)
        pos = self.pos
        if pos[0] <= 0 or pos[0] > settings.WIDTH:
            if pos[0] < 0:
                self.pos = (self.get_radius(), pos[1])
            if pos[0] > settings.WIDTH:
                self.pos = (settings.WIDTH - self.get_radius(), pos[1])
        if pos[1] < 0 or pos[1] > settings.HEIGHT:
            if pos[1] < 0:
                self.pos = (pos[0], self.get_radius())
            if pos[1] > settings.HEIGHT:
                self.pos = (pos[0], settings.HEIGHT - self.get_radius())

        #print(self.pos)
    
    def get_vel(self):
        return self.vel
    
    def update_vel(self, bodies, dt = 1):
        self.update_accel(bodies)
        delta_vel = tuple(el * dt for el in self.get_accel())
        self.vel = tuple(map(sum, zip(self.vel, delta_vel)))

        pos = self.get_pos()
        if pos[0] < 0 or pos[0] > settings.WIDTH:
            self.vel = (-self.vel[0], self.vel[1])
        if pos[1] < 0 or pos[1] > settings.HEIGHT:
            self.vel = (self.vel[0], -self.vel[1])
    
    def get_accel(self):
        return self.accel

    def get_color(self):
        return self.color

    def get_radius(self):
        return self.radius
    

    def update_accel(self, bodies):
        
        new_accel = (0, 0)

        def helper(body):
            self_pos = self.get_pos()
            body_pos = body.get_pos()

            dist = tuple(map(operator.sub, body_pos, self_pos))
            theta = math.atan2(dist[1], dist[0])

            dist_mag = math.dist(self_pos, body_pos)

            if dist_mag <= self.get_radius() + body.get_radius():
                dist_mag = self.get_radius() + body.get_radius()
                a_vect_multiplier = -1
            else:
                a_vect_multiplier = 1
            
        
                #return tuple([0, 0])
            a_vect_mag = (settings.G * body.get_mass()) / (dist_mag ** 2)
            a_vect_mag *= a_vect_multiplier
            a = (a_vect_mag * math.cos(theta), a_vect_mag * math.sin(theta))
            return a

        for body in bodies:
            if id(body) == id(self):
                continue
            a_vec = helper(body)
            new_accel = tuple(map(sum, zip(a_vec, new_accel)))
           
        
        self.accel = new_accel



