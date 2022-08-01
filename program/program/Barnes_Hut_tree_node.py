import settings
import body as b
from treelib import Node, Tree

class B_H_Tree_Node():
    '''
    The B_H_Tree_Node object represents a single node that will be used by the quadtree that the Barnes Hut 
    algorithm relies upon.
    
    Args:
        top_left (tuple): The top left coordinate of the quadrant that this node will represent.
        width (int): The width of the quadrant that this node will represent.
        height (int): The height of the quadrant that this node will represent.
        depth (int): The depth of this node in the quadtree.
        body (body.Body): The Body object that this node will represent.
        total_mass (float): The total mass of the Body objects represented by the children of this node if this node is an inner node.
        center_of_mass (tuple): The center of mass of the Body objects represented by the children of this node if this node is an inner node.
        node_param (int): Used to identify and associate this node to a Node in the treelib module. Used for testing purposes when a treelib Tree
                          is to be constructed and drawn that represents the quadtree.
        
    
    Attributes:
        body (body.Body): The Body object that this node will represent.
        children_bodies (list): A list containing all the Body objects that this node's descendents represent.
        children_nodes (list): A list containing all the children nodes of this node
        top_left (tuple): The top left coordinate of the quadrant that this node will represent.
        width (int): The width of the quadrant that this node will represent.
        height (int): The height of the quadrant that this node will represent.
        depth (int): The depth of this node in the quadtree.
        body (body.Body): The Body object that this node will represent.
        total_mass (float): The total mass of the Body objects represented by the children nodes of this node if this node is an inner node.
        center_of_mass (tuple): The center of mass of the Body objects represented by the children nodes of this node if this node is an inner node.
        node_param (int): Used to identify and associate this node to a Node in the treelib module. Used for testing purposes when a treelib Tree
                          is to be constructed and drawn that represents the quadtree.

    '''
    __slots__ = ("top_left", "width", "height", "depth", "body", "total_mass", "center_of_mass", "children_bodies", "children_nodes", "node_param")

    def __init__(self, top_left, width, height, depth, body = None, total_mass = 0, center_of_mass = None, node_param = None):
        self.body = body
        self.total_mass = total_mass
        self.center_of_mass = center_of_mass

        self.children_bodies = []

        self.children_nodes = None
        self.top_left = top_left

        self.width = width
        self.height = height
        
        self.depth = depth
        if depth > settings.MAX_DEPTH_ACHIEVED:
            settings.MAX_DEPTH_ACHIEVED = depth
        #print(depth)
        self.node_param = node_param

    def get_body(self):
        '''
        Getter for the Body object that this node represents.
        
        Returns:
            The Body object represented by this node.
        '''

        return self.body
    
    def get_total_mass(self):
        '''
        Getter for the total mass of the Body objects represented by the children nodes of this node if this node is an inner node.
        
        Returns:
            The total mass of the Body objects represented by this node's descendent nodes.
        '''

        return self.total_mass

    def get_center_of_mass(self):
        '''
        Getter for the center of mass of the Body objects represented by the children nodes of this node if this node is an inner node.
        
        Returns:
            The center of mass of the Body objects represented by this node's descendent nodes.
        '''

        return self.center_of_mass
    
    def get_quadrant(self):
        '''
        Getter for the quadrant of this node. Represented by the top left coordinate of the quadrant represented by this node.
        
        Returns:
            The top left coordinate of the quadrant represented by this node.
        '''
        
        return self.top_left
    
    def get_children_bodies(self):
        '''
        Getter for the Body objects represented by the children nodes of this node if this node is an inner node.
        
        Returns:
            A list of the Body objects represented by this node's descendent nodes.
        '''

        return self.children_bodies

    def get_width(self):
        '''
        Getter for the width of the quadrant represented by this node.
        
        Returns:
            The width of the quadrant represented by this node.
        '''

        return self.width
    
    def get_height(self):
        '''
        Getter for the height of the quadrant represented by this node.
        
        Returns:
            The height of the quadrant represented by this node.
        '''

        return self.height

    def get_children_nodes(self):
        '''
        Getter for the children nodes of this node.
        
        Returns:
            A list of the children nodes of this node.
        '''

        return self.children_nodes

    def get_depth(self):
        '''
        Getter for the depth of this node.
        
        Returns:
            The depth of this node in the quadtree.
        '''

        return self.depth

    def set_body(self, body):
        '''
        Setter for body represented by this node.

        Args:
            body (body.Body): The new Body object that this node should represent.
        '''
        if settings.TESTING_TREE:
            if body is not None:
                settings.TREE.get_node(self.node_param).tag = body.identifier + str(self.get_quadrant()) + str((self.get_width(), self.get_height()))
            else:
                settings.TREE.get_node(self.node_param).tag = "empty" + str(self.get_quadrant()) + str((self.get_width(), self.get_height()))
        self.body = body
    
    def set_total_mass(self, total_mass):
        '''
        Setter for total mass of the Body objects represented by the children nodes of this node if this node is an inner node.

        Args:
            total_mass (float): The new total mass.
        '''

        self.total_mass = total_mass
    
    def set_center_of_mass(self, center_of_mass):
        '''
        Setter for the center of mass of the Body objects represented by the children nodes of this node if this node is an inner node.

        Args:
            center_of_mass (tuple): The new center of mass.
        '''

        self.center_of_mass = center_of_mass
    
    def set_quadrant(self, top_left):
        '''
        Setter for the top_left coordinate of the quadrant represented by this node.

        Args:
            top_left (tuple): The new top left coordinate of the quadrant.
        '''

        self.top_left = top_left
    
    def is_internal_node(self):
        '''
        Determines whether this node is an internal node. An internal node is one that represents the Body objects of its children nodes.

        Returns:
            True if this node is an internal node, false otherwise.
        '''

        return self.get_body() is None and self.get_children_nodes() is not None
    
    def is_external_node(self):
        '''
        Determines whether this node is an external node. An external node represents a single Body object. It is a leaf of the quadtree.

        Returns:
            True if this node is an external node, false otherwise.
        '''

        return self.get_body() is not None and self.get_children_nodes() is None
    
    def is_empty_node(self):
        '''
        Determines whether this node is an empty node. An empty node has no children and has no Body object that it represents.
        The node represents empty space.

        Returns:
            True if this node is an empty node, false otherwise.
        '''

        return self.get_body() is None and self.get_children_nodes() is None

    def update_total_mass(self):
        '''
        Updates the total mass of this node, if this node is an inner node.
        '''

        body_children = self.get_children_bodies()
        mass_sum = 0
        for body in body_children:
            mass_sum += body.get_mass()
        
        self.set_total_mass(mass_sum)
    
    def update_center_of_mass(self):
        '''
        Updates the center of mass represented by this node, if this node is an inner node.
        '''

        body_children = self.get_children_bodies()
        x_cm = 0
        y_cm = 0
        for body in body_children:
            xPos, yPos = body.get_pos()
            mass = body.get_mass()
            x_cm += (xPos * mass) / self.get_total_mass()
            y_cm += (yPos * mass) / self.get_total_mass()
        
        self.set_center_of_mass((x_cm, y_cm))

    def add_body(self, body):
        '''
        Adds a Body object to the rest of the Body objects that this node represents, if this node is an inner node.
        Handles the updates necessary, updating the total mass and the center of mass.

        Args:
            body (body.Body): The Body object to add.
        '''

        self.children_bodies.append(body)
        self.update_total_mass()
        self.update_center_of_mass()

    def in_quadrant(self, body):
        '''
        Determines if a Body object is inside the quadrant represented by this node.

        Args:
            body (body.Body): Will determine if this Body object is inside the quadrant represented by this node.
        Returns:
            True if the inputted Body object is inside the quadrant represented by this node, false otherwise.
        '''

        top_left = self.get_quadrant()
        top_left_x, top_left_y = top_left

        body_pos = body.get_pos()
        body_xPos, body_yPos = body_pos

        return body_xPos >= top_left_x and body_yPos >= top_left_y and body_xPos < top_left_x + self.get_width() and body_yPos < top_left_y + self.get_height() 

    def create_children(self):
        '''
        Creates children for this node. Essentially changes this node to be an inner node in the quadtree.
        '''
        self.children_nodes = []

        half_width = self.get_width() // 2
        half_height = self.get_height() // 2

        curr_top_left = self.get_quadrant()

        top_left_x, top_left_y = curr_top_left
        
        #Necessary for the treelib testing, when testing, nodes should be constructed with the settings.NODE_COUNTER to identify it.
        if settings.TESTING_TREE:
            q1 = B_H_Tree_Node((top_left_x + half_width, top_left_y), half_width, half_height, self.depth + 1, node_param = settings.NODE_COUNTER)
            settings.TREE.create_node("empty" + str(q1.get_quadrant()) + str((half_width, half_height)), settings.NODE_COUNTER, parent = self.node_param)
            settings.NODE_COUNTER += 1

            q2 = B_H_Tree_Node(curr_top_left, half_width, half_height, self.depth + 1, node_param = settings.NODE_COUNTER)
            settings.TREE.create_node("empty" + str(q2.get_quadrant()) + str((half_width, half_height)), settings.NODE_COUNTER, parent = self.node_param)
            settings.NODE_COUNTER += 1

            q3 = B_H_Tree_Node((top_left_x, top_left_y + half_height), half_width, half_height, self.depth + 1, node_param = settings.NODE_COUNTER)
            settings.TREE.create_node("empty" + str(q3.get_quadrant()) + str((half_width, half_height)), settings.NODE_COUNTER, parent =  self.node_param)
            settings.NODE_COUNTER += 1

            q4 = B_H_Tree_Node((top_left_x + half_width, top_left_y + half_height), half_width, half_height, self.depth + 1, node_param = settings.NODE_COUNTER)
            settings.TREE.create_node("empty" + str(q4.get_quadrant()) + str((half_width, half_height)), settings.NODE_COUNTER, parent = self.node_param)
            settings.NODE_COUNTER += 1
        else:
            #Constructs node objects that represent the quadrant represented by this node divided into 4 quadrants.
            q1 = B_H_Tree_Node((top_left_x + half_width, top_left_y), half_width, half_height, self.depth + 1)
            q2 = B_H_Tree_Node(curr_top_left, half_width, half_height, self.depth + 1)
            q3 = B_H_Tree_Node((top_left_x, top_left_y + half_height), half_width, half_height, self.depth + 1)
            q4 = B_H_Tree_Node((top_left_x + half_width, top_left_y + half_height), half_width, half_height, self.depth + 1)

        self.children_nodes.append(q1)
        self.children_nodes.append(q2)
        self.children_nodes.append(q3)
        self.children_nodes.append(q4)

if __name__ == "__main__":
    m_q = B_H_Tree_Node((0, 0), settings.WIDTH, settings.HEIGHT, depth = 1)
    m_q.create_children()
    children = m_q.get_children_nodes()
    for child in children:
        print(child.in_quadrant(b.Body(50, 5, (400, 400))))
        print(child.get_width(), " ", child.get_height())


    


        



    