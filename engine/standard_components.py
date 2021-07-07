from engine.component import Component

class ObjectMover(Component):
    def keyboard_callback(self, key):
        if key == b'w':
            self.game_object.transform.rotate(0.1, 0, 0)
        elif key == b's':
            self.game_object.transform.rotate(-0.1, 0, 0)
        
        elif key == b'a':
            self.game_object.transform.rotate(0, -0.1, 0)
        elif key == b'd':
            self.game_object.transform.rotate(0, 0.1, 0)
        
        elif key == b'q':
            self.game_object.transform.rotate(0, 0, -0.1)
        elif key == b'e':
            self.game_object.transform.rotate(0, 0, 0.1)

        elif key == b't':
            self.game_object.transform.translate(0, 0.1, 0)
        elif key == b'g':
            self.game_object.transform.translate(0, -0.1, 0)
        elif key == b'f':
            self.game_object.transform.translate(-0.1,0,  0)
        elif key == b'h':
            self.game_object.transform.translate(0.1,0,  0)
        elif key == b'r':
            self.game_object.transform.translate(0,0,0.1)
        elif key == b'y':
            self.game_object.transform.translate(0, 0, -1)
        elif key == b'k':
            self.game_object.transform.scale(1.1, 0.9, 1)
        elif key == b'l':
            self.game_object.transform.scale(0.9, 1.1, 1)


