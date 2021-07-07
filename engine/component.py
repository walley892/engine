from engine.game_object import GameObject

class Component(object):
    '''
    A component acts on/on behalf of a game object every game frame via update(), a gameobject can have many components
    '''
    
    def __init__(self):
        self.game_object = None

    '''
    The interface. Override these in a subclass to add functionality
    '''

    def update(self):
        # called once per game frame
        return

    def keyboard_callback(self, key):
        # called once per frame when a key is pressed
        return

    def mouse_callback(self, button, state, x, y, camera):
        # called once per frame when a mouse button is pressed
        return 
    
    def _set_game_object(self, game_object):
        # set the gameobject that this component acts on
        # DO NOT CALL DIRECTLY
        self.game_object = game_object
