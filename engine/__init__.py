import sys
from OpenGL.GL import shaders
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
from engine.standard_game_objects import Camera

# The display() method does all the work; it has to call the appropriate
# OpenGL functions to actually display something.
glutInit(sys.argv)

class Window(object):
    def __init__(self, name='window', game_objects = None, camera = None, x = 0, y = 0):

        if game_objects is not None:
            self.game_objects = game_objects
        else:
            self.game_objects = []
        if camera is None:
            self.camera = Camera()
        else:
            self.camera = camera

        for g in self.game_objects:
            g.set_window(self)

        glutInitWindowPosition(x, y)
        self.window_id = glutCreateWindow(name)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable( GL_BLEND )

       
        glutKeyboardFunc(self.keyboard_callback)
        glutMouseFunc(self.mouse_callback)
        glutDisplayFunc(self.update)
        self.update_window_params()
        self.is_alive = True

    def set_size(self, width, height):
        glutSetWindow(self.window_id)
        glutReshapeWindow(width, height)

    def set_position(self, x, y):
        glutSetWindow(self.window_id)
        glutPositionWindow(x, y)
    
    def update_window_params(self):
        self.height = glutGet(GLUT_WINDOW_HEIGHT)
        self.width = glutGet(GLUT_WINDOW_WIDTH)
        self.x = glutGet(GLUT_WINDOW_X)
        self.y = glutGet(GLUT_WINDOW_Y)

    def destroy(self):
        glutDestroyWindow(self.window_id)
        self.is_alive = False
    
    def keyboard_callback(self, key, x = 0, y = 0):
        for obj in self.game_objects + [self.camera]:
            obj._keyboard_callback(key)

    def mouse_callback(self, button, state, x, y):
        x = x/self.width
        y = y/self.height
        for obj in self.game_objects + [self.camera]:
            obj._mouse_callback(button, state, x, y, self.camera)
            

    def update(self):
        glutSetWindow(self.window_id)
        self.update_window_params()
        # Clear the color and depth buffers
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        for obj in self.game_objects + [self.camera]:
            obj._update()

        for i, obj in enumerate(self.game_objects):
            for renderer in obj.get_renderers():
                renderer.draw_to_camera(self.camera)

        glutSwapBuffers()
        glutPostRedisplay()

# Create a double-buffer RGBA window.   (Single-buffering is possible.
# So is creating an index-mode window.
def start_main_loop():
    glutMainLoop()
