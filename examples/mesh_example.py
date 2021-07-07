from engine import Window, start_main_loop
from engine.rendering.standard_renderers import MeshRenderer
from engine.rendering.renderer_factory import RenderMode
from engine.game_object import GameObject
import numpy as np

class RectangleMeshObject(GameObject):
    def __init__(self):
        super().__init__()
        self.renderer = MeshRenderer()
        self.add_renderer(self.renderer)
        points = np.array([
            0.5, 0.5, -1.0,
            0.5, -0.5, -1.0,
            -0.5, -0.5, -1.0,
            -0.5, 0.5, -1.0,
        ]).astype(np.float32).flatten()
        triangles = np.array([[0,1,2], [0, 3, 2]]).astype(np.uint32).flatten()
        # a MeshRenderer (renderer) renders the points defined by 
        # renderer.vertex_buffer and the triangles defined by
        # renderer.elements
        self.renderer.vertex_buffer = np.array(points)
        self.renderer.elements = triangles
        self.renderer.render_mode = RenderMode.ELEMENTS

if __name__ == "__main__":
    g = RectangleMeshObject()
    w = Window(game_objects=[g])
    start_main_loop()
