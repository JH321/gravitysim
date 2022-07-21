###
#Can change
###

DIMENSIONS = (600, 600) #Dimension of the screen, first index represents width, second index represents height


G = 500 #The gravitational constant value, can tweak but this number seems to work the best. This is not the actual constant from 
        #Newton's law of gravitation but we aren't working with si units in the program.

FPS = 500 #This controls the maximum number of screen refreshes made by the program, this number is high so that the maximum number of refreshes can be made 
          #per second. The gravitational calculations rely on the time between refreshes, with a higher frequency of refreshes resulting in a more accurate
          #approximation

MAX_LINES = 65 #Controls the maximum number of trailing lines that a body will have on the screen

RATIO_EPSILON = 0.75 #The ratio used for the barnes hut approximation to determine if a node is sufficiently far away

###
#DO NOT CHANGE, these are global variables needed to conveniently modify the program or values that should not be changed
###

WIDTH = DIMENSIONS[0]
HEIGHT = DIMENSIONS[1]

#Necessary for the treelib testing done to verify the BH tree construction algorithm worked correctly
TESTING_TREE = False
TREE = None
NODE_COUNTER = 0



RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
MENU_COLOR = (51, 153, 255)

#Controls whether the program will generate random masses
RANDOM_MASS = False


#Controls whether the Barnes Hut algorithm will be used by the program
B_H_OPTIMIZATION = False

#Needed to calculate how far down the BH tree has been constructed. From testing, the maximum depth of the nodes in the tree never exceeded 10
MAX_DEPTH = 10
MAX_DEPTH_ACHIEVED = 0
