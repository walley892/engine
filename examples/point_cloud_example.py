from engine import Window, start_main_loop
from engine.rendering.standard_renderers import PointCloudRenderer
from engine.game_object import GameObject
import numpy as np

class PlaneCloudObject(GameObject):
    def __init__(self):
        super().__init__()
        self.renderer = PointCloudRenderer()
        self.add_renderer(self.renderer)
        points = []
        for i in range(100):
            for j in range(100):
                # create points from (-0.5, -0.5 -1) to (0.5, 0.5, -1)
                points.append(np.array([0.5 - i/100.0, 0.5 -j/100.0, -1.0]).astype(np.float32))
        # a PointCloudRenderer (renderer) renders the points defined by 
        # renderer.vertex_buffer
        self.renderer.vertex_buffer = np.array(points)
        self.renderer.n_points = len(self.renderer.vertex_buffer)

if __name__ == "__main__":
    g = PlaneCloudObject()
    w = Window(game_objects=[g])
    start_main_loop()
