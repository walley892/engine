from engine import Window, start_main_loop
from engine.standard_game_objects import Camera, Cube
from engine.component import Component

class Rotator(Component):
    def update(self):
        # a component acts on a gameobject (accessed through self.game_object)
        # once per frame via update()
        self.game_object.transform.rotate(0, 0.0003, 0.0002)

if __name__=='__main__':
    cube1 = Cube()
    cube1.add_component(Rotator())
    cube1.transform.translate(0.75, 0, -4)
    
    cube2 = Cube()
    cube2.add_component(Rotator())
    cube2.transform.translate(-0.75, 0, -4)
    
    w = Window(game_objects=[cube1, cube2])
    start_main_loop()
