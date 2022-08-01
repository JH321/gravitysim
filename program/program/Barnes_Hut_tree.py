import math
import Barnes_Hut_tree_node as bh
import body as b
import settings
import time
from treelib import Node, Tree

class B_H_Tree():
    '''
    The B_H_Tree object represents the quadtree used in the Barnes Hut algorithm. It handles
    construction of such a tree and calculating net acceleration on a body from such a tree.
    There is a major issue with this implementation with an unknown cause. It is fairly evident that
    the tree is constructed correctly and acceleration is calculated correctly. However, this implementation proves
    significantly slower than the brute force when it is meant to be able to simulate more bodies in a faster and 
    more efficient way. The issue may stem from python itself.
    
    Args:
        bodies (list): The list that contains all the Body objects represented on the screen. Used to construct a quadtree for 
                       the Barnes Hut algorithm.
    
    Attributes:
        root (Barnes_Hut_tree_node.B_H_Tree_Node): The root of this B_H_Tree object
        brute_force_bodies (list): A list to store objects that shouldn't be stored in the tree. Bruteforce should be used to calculate
                                   the acceleration induced by these objects. This attribute is a temporary measure, might be removed later.

    '''
    def __init__(self, bodies):
        self.root = self.construct_tree(bodies)
        
    
    def construct_tree(self, bodies):
        '''
        Constructs the quadtree

        Args:
            bodies (list): The list that contains all the Body objects represented on the screen.

        Returns:
            The root of the quadtree constructed.
        '''

        #start = time.time()
        
        self.brute_force_bodies = []
        '''i = 1
        while i < len(bodies) - 1:
            j = i + 1
            body_i = bodies[i]
            i_pos = bodies[i].get_pos()
            while j < len(bodies):
                body_j = bodies[j]
                if math.dist(i_pos, body_j.get_pos()) < 10:
                    self.brute_force_bodies.append(body_i)
                    self.brute_force_bodies.append(body_j)
                j += 1
            i += 1'''

        bodies = [body for body in bodies if body not in self.brute_force_bodies]


        if settings.TESTING_TREE:
            settings.NODE_COUNTER = 0
            self.root = bh.B_H_Tree_Node((0, 0), settings.WIDTH, settings.HEIGHT, 0, node_param = settings.NODE_COUNTER)
            settings.TREE = Tree()
            settings.TREE.create_node("Empty", settings.NODE_COUNTER)
            settings.NODE_COUNTER += 1
            for body in bodies:
                B_H_Tree.insert_node(self.root, body)
            print("Final tree")
            settings.TREE.show()
        else:
            self.root = bh.B_H_Tree_Node((0, 0), settings.WIDTH, settings.HEIGHT, 0)
            for body in bodies:
                B_H_Tree.insert_node(self.root, body)
            
        return self.root

        #end = time.time()

        #print("time for construction of tree ", (end - start) * 1000)

    def calc_net_accel(self, body):
        '''
        Calculates the net acceleration on the inputted body.

        Args:
            body (body.Body): The net acceleration on this Body object will be calculated.
        
        Returns:
            The net acceleration on the inputted body.
        '''

        #start = time.time()
        net_accel = B_H_Tree.calc_accel(self.root, body)
        #end = time.time()
        add_accel = body.brute_force_method(self.brute_force_bodies)
        #print("time for calculating accel ", (end - start) * 1000)

        net_accel = (net_accel[0] + add_accel[0], net_accel[1] + add_accel[1])
        return net_accel
    
    def insert_node(root, body):
        '''
        Recursively inserts a node representing a body in the system into the quadtree. This is the crux in
        constructing the quadtree utilized in the Barnes Hut algorithm.
        Check https://www.cs.princeton.edu/courses/archive/fall03/cs126/assignments/barnes-hut.html
        for the algorithm.

        Args:
            root (Barnes_Hut_tree_node.Barnes_Hut_tree_node.B_H_Tree_Node): The node being examined in current recursive call.
            body (body.Body): The Body object that is being inserted into the quadtree.
        '''

        #A precaution that shouldn't trip
        if root.get_depth() > settings.MAX_DEPTH:
            raise Exception("max depth surpassed, this should theoretically not happen")
        
        if root.is_empty_node():
            root.set_body(body)
        
        elif root.is_internal_node():
            root.add_body(body)
            quadrants = root.get_children_nodes()
            for quad in quadrants:
                if quad.in_quadrant(body):
                    B_H_Tree.insert_node(quad, body)
        
         
        elif root.is_external_node():
            body_a = root.get_body() #body that is already in the node
            root.set_body(None)
            
            body_b = body

            body_a_pos = body_a.get_pos()
            body_b_pos = body_b.get_pos()

            root.create_children()
            quadrants = root.get_children_nodes()

            if quadrants is not None:
                for quad in quadrants:
                    if quad.in_quadrant(body_a):
                        B_H_Tree.insert_node(quad, body_a)
                       
                   
                    
                for quad in quadrants:
                    if quad.in_quadrant(body_b):
                        B_H_Tree.insert_node(quad, body_b)
                        
          
            root.add_body(body_a)
            root.add_body(body_b)
          
                    
    def calc_accel(root, body):
        '''
        Recursively calculates the acceleration induced by the other bodies in the quadtree
        on the inputted body.
        Check https://www.cs.princeton.edu/courses/archive/fall03/cs126/assignments/barnes-hut.html
        for the algorithm.

        Args:
            root (Barnes_Hut_tree_node.Barnes_Hut_tree_node.B_H_Tree_Node): The current node being examined in the recursive call.
            body (body.Body): The acceleration induced on this body will be calculated.

        Returns:
            The induced acceleration produced on the inputted body by the body represented by the current node being examined.
            If the a bunch of bodies are far enough, the node will represent a collection of these bodies and the center of mass
            formed by these bodies will be used to calculated the induced acceleration and this will be returned.
        '''

        if root.is_external_node() and root.get_body() is not body:
            return body.calc_accel(root.get_body())
        
        elif root.is_internal_node():
            
            width = root.get_width()

            c_of_mass = root.get_center_of_mass()
            total_mass = root.get_total_mass()
            body_pos = body.get_pos()

            distance = math.dist(c_of_mass, body_pos)

            #a precaution so that a zero division error does not happen
            if distance == 0:
                distance = body.get_radius()

            ratio = width / distance

            if ratio < settings.RATIO_EPSILON:
                
                return body.calc_accel(b.Body(total_mass, pos = c_of_mass))
            else:
                net_accel = (0, 0)
                children_nodes = root.get_children_nodes()
                for node in children_nodes:
                    add_accel = B_H_Tree.calc_accel(node, body)
                    net_accel = (net_accel[0] + add_accel[0], net_accel[1] + add_accel[1])
                return net_accel
        else:
            
            return (0, 0)

#This was used for testing purposes with the treelib module to ensure that the quadtree was
#constructed correctly
if __name__ == '__main__':
    def test_tree_generation():
        bodies = []
        body_a = b.Body(50, pos = (settings.WIDTH // 2 - 50, settings.HEIGHT // 2 - 50), identifier = "a")
        bodies.append(body_a)
        body_b = b.Body(50, pos = (settings.WIDTH // 2 + 100, 50), identifier = "b")
        bodies.append(body_b)
        body_c = b.Body(50, pos = (settings.WIDTH // 2 + 30, 100), identifier = "c")
        bodies.append(body_c)
        body_d = b.Body(50, pos = (settings.WIDTH // 2 + 200, 160), identifier = "d")
        bodies.append(body_d)
        body_e = b.Body(50, pos = (100, settings.HEIGHT // 2 + 70), identifier = "e")
        bodies.append(body_e)
        body_f = b.Body(50, pos = (100, settings.HEIGHT // 2 + 170), identifier = "f")
        bodies.append(body_f)
        body_g = b.Body(50, pos = (170, settings.HEIGHT // 2 + 200), identifier = "g")
        bodies.append(body_g)
        body_h = b.Body(50, pos = (settings.WIDTH // 2 + 30, settings.HEIGHT // 2 + 200), identifier = "h")
        bodies.append(body_h)
        body_i = b.Body(50, pos = (settings.WIDTH // 2 + 30, settings.HEIGHT // 2 + 200), identifier = "i")
        bodies.append(body_i)
        B_H_Tree(bodies)
    settings.TESTING_TREE =  True
    if settings.TESTING_TREE:
        settings.MAX_DEPTH_ACHIEVED = 0
        test_tree_generation()
        print(settings.MAX_DEPTH_ACHIEVED)


        

