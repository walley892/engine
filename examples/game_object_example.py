from engine import Window, start_main_loop
from engine.game_object import GameObject

class FrameCountPrinter(GameObject):
    # a GameObject is something that executes some piece
    # of code every game frame
    def __init__(self):
        super().__init__()
        self._frames = 0
    
    def update(self):
        # update() defines the code that is executed by this
        # GameObject every frame
        super().__init__()
        self._frames += 1
        print(self._frames)


if __name__ == '__main__':
    f = FrameCountPrinter()

    # windows contain and (if applicable) render game objects
    w = Window(name="Frame Counter", game_objects = [f])

    # once start_main_loop is executed,
    # every game object in every window begins to update
    start_main_loop()
