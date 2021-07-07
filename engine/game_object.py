from engine.transformations import Transform
import numpy as np

class GameObject(object):
    '''
    A gameobject is an object in world space. A gameobject can act every frame via update()
    '''
    def __init__(self):
        # the 'parent' of this gameobject,
        # a gameobject's transform is composed with its parent's
        # to derive its position and rotation in world space
        self.parent = None # type: GameObject

        self.window = None
        
        # a map from the address of a gameobject to that gameobject.
        # this gameobject is the 'parent' of all the values in this map
        self.child_map = {} # type: Dict[str, GameObject]

        # this gameobject's local position. If parent=None,
        # this is also the gameobject's position in world space
        self.transform = Transform()

        # a map from the address of a component to that component
        # the values in this map act on this gameobject
        self.component_map = {} # type: List[Component]

        # a map from the address of a renderer to that Renderer
        # the values in this map render this gameobject
        self.renderer_map = {} # type: List[Renderer]

        self.active = True

    '''
    The interface:
        Subclasses can override these methods to add functionality to the gameobject
    '''
    
    def update(self):
        # called once per frame to update the gameobject
        return

    def keyboard_callback(self, key):
        # called once per frame if a key was pressed
        return 
    
    def mouse_callback(self, button, state, x, y, camera):
        '''
        called once per frame if the mouse was clicked
        '''
        return
    
    '''
    Public methods. Feel free to call these :)
    '''
    def add_component(self, component):
        self.component_map[str(component)] = component
        component._set_game_object(self)

    def remove_component(self, component):
        del self.component_map[str(component)]

    def add_renderer(self, renderer):
        self.renderer_map[str(renderer)] = renderer
        renderer.game_object = self

    def get_components(self):
        return self.components

    def set_window(self, window):
        self.window = window

    @property
    def components(self):
        return list(self.component_map.values())

    @property
    def renderers(self):
        return list(self.renderer_map.values())
    
    def get_renderers(self):
        renderers = []
        if not self.active:
            return renderers
        renderers = renderers + self.renderers
        for child in self.children:
            renderers = renderers + child.get_renderers()
        return renderers
    
    def set_parent(self, parent):
        if not (self.parent is None) and str(self.parent) != str(parent):
            self.parent._remove_child(self)
        self.parent = parent
        self.parent._add_child(self)

    def remove_parent(self):
        if not (self.parent is None):
            self.parent._remove_child(self)

    def _remove_child(self, child):
        del self.child_map[str(child)]

    def _add_child(self, child):
        self.child_map[str(child)] = child
    
    @property
    def children(self):
        return list(self.child_map.values())
     
    def get_transform(self):
        if self.parent is None:
            return self.transform.transformation
        return np.matmul(self.parent.get_transform(), self.transform.transformation)

    '''
    Private methods. do not call >:(
    '''
    def _keyboard_callback(self, key):
        # recursively call keyboard_callback() on this 
        # gameobject and its children
        if self.active:
            self.keyboard_callback(key)
            for child in self.children:
                child._keyboard_callback(key)
            for component in self.components:
                component.keyboard_callback(key)

    def _mouse_callback(self, button, state, x, y, camera):
        # recursively call mouse_callback() on this
        # gameobject and its children
        if self.active:
            self.mouse_callback(button, state, x, y, camera)
            for child in self.children:
                child._mouse_callback(button, state, x, y, camera)
            for component in self.components:
                component.mouse_callback(button, state, x, y, camera)

    def _update(self):
        # recursively call update() on this gameobject
        # and its children
        if self.active:
            self.update()
            for child in self.children:
                child._update()
            for component in self.components:
                component.update()
