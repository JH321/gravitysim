# gravitysim
rough n-body simulation

Intro:

For anybody who stumbled upon this and is thinking of creating their own n-body sim in Python and Pygame, I highly recommend looking into different modules more suited for accurate simulations or a different language altogether. After creating this attempt, my biggest regret is spending my time to create this in Python. I believe Python is too slow for this endeavor and I should have done more research before committing to Python.

This is my own personal attempt at creating a crude n-body simulation. It was created using Python and the Pygame module. The Pygame module was convenient for graphically displaying the n-body simulation.

The simulation offers two ways of simulating gravitational attraction. The first is the naive brute force method that relies on summing up all forces and using the principle of superposition to find the net force and, hence, the net acceleration. The second method is the Barnes Hut algorithm.

The Barnes Hut algorithm was implemented by myself. However, it has significant issues that I am unable to figure out or fix. More details in the issues section. 

The Barnes Hut algorithm was implemented by using this website as the reference:
https://www.cs.princeton.edu/courses/archive/fall03/cs126/assignments/barnes-hut.html

Structure:

main.py: This module initializes pygame, sets up the simulation, and displays everything to the screen.

body_sprite.py: This module represents a Body object as a pygame Sprite object through the Body_Sprite class. In truth, this module is redundant and was more of a choice made early in development with the belief that it would help with code maintainability. It may be removed in the future. This module basically wraps the Body object and allows the Body object to be easily drawn to the pygame screen as a Sprite.

body.py: This module holds the Body class. The Body class represents an individual Body, keeping track of its position, velocity, and acceleration vectors. It also handles updating the acceleration vector according to the gravitational forces induced on the body by other body objects in space.

Barnes_Hut_tree.py: This module holds the B_H_Tree class. This class represents the quadtree that is used in the Barnes Hut algorithm. It holds methods for constructing such a tree from a list of Body objects on the screen, and getting the induced acceleration on a Body.

Barnes_Hut_tree_node.py: This module holds the B_H_Tree_Node class. THis class represents a node in the quadtree. It handles all the operations necessary for a node in the quadtree used in the Barnes Hut algorithm. These include identifying the node as a inner, external, or empty node, constructing children nodes while correctly dividing the quadrant into 4 subquadrants, keeping track of total mass and center of mass of an internal node. 

Issues:

The Barnes Hut algorithm is significantly slower than the brute force method. This should not happen. The brute force method runs in O(n^2) time while the Barnes Hut algorithm runs in O(nlog(n)) time. After doing my own testing, I found that significant time is being allocated to constructing the tree as well as find the acceleration induced on each body in the tree. I did further testing to ensure that the quadtree was being constructed correctly. Also, qualitatively speaking, the bodies behave identically to the brute force method. I could not come to a solid conclusion for why my implementation was not working fast enough. In the end, the possibilities are that there is a fault with my implementation, Python object creation and storage is too slow, or both are the reasons for this issue.

Whenever the pygame screen is dragged by the user while the simulation is running, the current frame freezes. When the user lets go of the screen, the next frame is drawn. The time between these two frames is then inputted to update the simulation, resulting in bodies being incorrectly updated on the screen. Pygame offers no way of determining if the screen is being dragged that I could find. As a result, this issue still persists.
