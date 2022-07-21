import settings
import operator
import math
import random
import Barnes_Hut_tree as bh
import time

class Body:

    '''
    The Body object represents a body that is influenced by gravitational forces.
    This class handles all the calculations necessary to simulate gravitational attraction
    on a body, keeping track of and updating a body's position, velocity, and acceleration.

    Args:
        mass (float): Represents the mass of the body.
        radius (int): Represents the radius of the body.
        pos (tuple): Represents the starting position of the body.
        vel (tuple): Represents the initial velocity of the body.
        in_place (Boolean): Determines whether the body is in place (unmovable).
        identifier (str): Optional param that is necessary for the treelib testing.
    
    Attributes:
        mass (float): The mass of this Body object.
        radius (int): The radius of this Body object.
        pos (tuple): The starting position of this Body object.
        vel (tuple): The initial velocity of this Body object.
        in_place (Boolean): Whether this Body object is immovable.
        identifier (str): treelib identifier of this Object.
        color: the color of this Body object on the screen.
    
    Class Attributes:
        color (list): Holds the used colors so that duplicate colors are not produced.
    '''

    color = []

    def __init__(self, mass, radius = 5, pos = (settings.WIDTH // 2, settings.HEIGHT // 2), vel = (0, 0), in_place = False, identifier = None):
        self.mass = mass

        self.pos = pos

        self.vel = vel

        self.accel = (0, 0)

        self.radius = radius

        self.in_place = in_place

        self.color = Body.generate_new_color()

        self.identifier = identifier

    def generate_new_color():
        '''
        Generates a random color that has not been used before for a Body object.

        Returns:
            The new color as a tuple.
        '''
        new_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        while new_color in Body.color or new_color < (100, 100, 100):
            new_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        Body.color.append(new_color)

        return new_color

    def set_pos(self, new_pos):
        '''
        Setter for this Body object's position.
        '''
        self.pos = new_pos

    def get_mass(self):
        '''
        Getter for this Body object's mass.

        Returns:
            This Body object's mass.
        '''

        return self.mass

    def get_pos(self):
        '''
        Getter for this Body object's position.

        Returns:
            This Body object's position.
        '''

        return self.pos
    
    def get_vel(self):
        '''
        Getter for this Body object's velocity.

        Returns:
            This Body object's velocity.
        '''
        return self.vel
    
    def get_accel(self):
        '''
        Getter for this Body object's acceleration.

        Returns:
            This Body object's acceleration.
        '''

        return self.accel

    def get_color(self):
        '''
        Getter for this Body object's color.

        Returns:
            This Body object's color.
        '''

        return self.color

    def get_radius(self):
        '''
        Getter for this Body object's radius.

        Returns:
            This Body object's radius.
        '''

        return self.radius

    
    def update_pos(self, bodies, body_tree = None, dt = 1):
        '''
        Updates this Body object's position based on its current velocity.

        Args:
            bodies (list): The list that contains all the Body objects represented on the screen.
            body_tree (Barnes_Hut_tree.B_H_Tree): The Barnes Hut tree containing all the Body objects represented on the screen.
            dt (float): Time between screen refreshes. Used to update position assuming velocity was constant through this time.

        '''

        #Only update position if this Body object is not meant to be in place
        if not self.in_place:
            delta_pos = tuple(el * dt for el in self.get_vel())
            self.pos = tuple(map(sum, zip(self.pos, delta_pos)))
            self.update_vel(bodies, body_tree, dt)

        #To handle positions when the Body object goes outside of the screen dimensions (meant to make it bounce back)
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

    
    def update_vel(self, bodies, body_tree, dt = 1):
        '''
        Updates this Body object's velocity.

        Args:
            bodies (list): The list that contains all the Body objects represented on the screen.
            body_tree (Barnes_Hut_tree.B_H_Tree): The Barnes Hut tree containing all the Body objects represented on the screen.
            dt (float): Time between screen refreshes. Used to velocity position assuming acceleration was constant through this time.
        '''


        self.update_accel(bodies, body_tree)
        delta_vel = tuple(el * dt for el in self.get_accel())
        self.vel = tuple(map(sum, zip(self.vel, delta_vel)))

        #To handle velocities when the Body object goes outside of the screen dimensions (meant to make it bounce back)
        pos = self.get_pos()
        if pos[0] < 0 or pos[0] > settings.WIDTH:
            self.vel = (-self.vel[0], self.vel[1])
        if pos[1] < 0 or pos[1] > settings.HEIGHT:
            self.vel = (self.vel[0], -self.vel[1])
    
    
    def calc_accel(self, body):
        '''
        Calculates the acceleration from the gravitational force exerted by a different body on this Body object.

        Args:
            body (body.Body): The Body object that exerts a force on this Body object.
        
        Returns:
            The acceleration induced on this Body object by the Body object in args.
        '''

        self_pos = self.get_pos()
        body_pos = body.get_pos()

        dist = tuple(map(operator.sub, body_pos, self_pos))
        theta = math.atan2(dist[1], dist[0])

        dist_mag = math.dist(self_pos, body_pos)

        #If the different Body object and this Body object are overlapping, makes them bounce back from each other 
        if dist_mag <= self.get_radius() + body.get_radius():
            #This is to ensure the distance does not get too small that the bodies experience a sudden growth in acceleration
            dist_mag = self.get_radius() + body.get_radius()
            a_vect_multiplier = -1
        else:
            a_vect_multiplier = 1
        
    
            #return tuple([0, 0])
        a_vect_mag = (settings.G * body.get_mass()) / (dist_mag ** 2)

        #Will make the acceleration vector point in the opposite direction if the bodies are overlapping
        a_vect_mag *= a_vect_multiplier
        a = (a_vect_mag * math.cos(theta), a_vect_mag * math.sin(theta))
        return a

    def brute_force_method(self, bodies):
        '''
        The brute force method for calculating the net acceleration induced on this Body object given a system of n bodies.
        The brute force method is a simple summation of induced accelerations using the principle of superposition.

        Args:
            bodies (list): The list that contains all the Body objects represented on the screen.
        
        Returns:
            The net acceleration induced on this Body object by the system of n bodies.
        '''

        new_accel = (0, 0)

        for body in bodies:
            #Ensures that this Body object does not induce an acceleration on itself
            if body is self:
                continue
            a_vec = self.calc_accel(body)
            new_accel = tuple(map(sum, zip(a_vec, new_accel)))
        
        return new_accel

    def B_H_method(self, body_tree):
        '''
        The Barnes Hut method for calculating acceleration.

        Args:
            body_tree (Barnes_Hut_tree.B_H_Tree): The Barnes Hut tree containing all the Body objects represented on the screen.
        
        Returns:
            The net acceleration induced on this Body object by the system of n bodies, approximated using the Barnes Hut algorithm
        '''

        new_accel = body_tree.calc_net_accel(self)
        return new_accel


    def update_accel(self, bodies, body_tree):
        '''
        Updates the acceleration induced on this Body object

        Args:
            bodies (list): The list that contains all the Body objects represented on the screen.
            body_tree (Barnes_Hut_tree.B_H_Tree): The Barnes Hut tree containing all the Body objects represented on the screen.
        '''

        if body_tree is not None:
            self.accel = self.B_H_method(body_tree)
        else:
            #start = time.time()
            self.accel = self.brute_force_method(bodies)
            #end = time.time()

            #print("time to bruteforce: ", (end - start) * 1000)

    


