from engine.rendering.renderer_factory import RenderMode, create_renderer_from_string
from engine.rendering.vertex_functions import *
from OpenGL.GL import *
import numpy as np
from matplotlib.pyplot import imread
import json
from engine.rendering.c_shaders import *

PointCloudRenderer = create_renderer_from_string(VERTEX_POINT, FRAGMENT_STANDARD)
MeshRenderer = create_renderer_from_string(VERTEX_POINT, FRAGMENT_STANDARD)
TexturedMeshRenderer = create_renderer_from_string(VERTEX_TEXTURE, FRAGMENT_TEXTURE)
MultiTexturedMeshRenderer = create_renderer_from_string(VERTEX_MULTI_TEXTURE, FRAGMENT_MULTI_TEXTURE)
ColoredMeshRenderer = create_renderer_from_string(VERTEX_COLOR, FRAGMENT_COLOR)
ColoredPointCloudRenderer = create_renderer_from_string(VERTEX_COLOR, FRAGMENT_COLOR)

class PlaneRenderer(ColoredMeshRenderer):
    def __init__(self, color = [1, 0, 0]):
        super().__init__()
        self.color = color

        self.vertex_buffer = generate_plane_vertices()
        self.color_buffer = self.generate_colors().flatten()
        self.elements = generate_plane_triangles().flatten()
        self.render_mode = RenderMode.ELEMENTS

    def generate_colors(self):
        return np.array([self.color, self.color, self.color, self.color], dtype=np.float32)

class TextRenderer(TexturedMeshRenderer):
    def __init__(self, text, x0, y0, height, width, color=(0,0,0)):
        super().__init__()
        self.x0, self.y0 = x0, y0
        self._font_map = json.load(open('font_textures/font.json'))
        self._font_tex = imread('font_textures/font.png')
        self.tex = self._font_tex[:,:,:].astype(np.float32)
        self.width = width
        self.height = height
        self.text = text
        self.vertex_buffer = self.generate_mesh_vertices().flatten()
        self.elements = self.generate_mesh_triangles().flatten()
        self.vertex_uvs = self.generate_mesh_uvs().flatten()
        self.render_mode = RenderMode.ELEMENTS
        self.texture_mode = GL_RGBA

    def update_text(self, text):
        self.text = text
        self.vertex_buffer = self.generate_mesh_vertices().flatten()
        self.tris_buffer = self.generate_mesh_triangles().flatten()
        self.vertex_uvs = self.generate_mesh_uvs()
        self.elements = self.generate_mesh_triangles().flatten()

    def update_bounds(self, height, width):
        self.height = height
        self.width = width
        self.vertex_buffer = self.generate_mesh_vertices().flatten()
        self.tris_buffer = self.generate_mesh_triangles().flatten()
        self.vertex_uvs = self.generate_mesh_uvs()

    def update_height(self, height):
        self.update_bounds(height, self.width)

    def update_width(self, width):
        self.update_bounds(self.height, width)

    def generate_mesh_uvs(self):
        uvs = []
        if len(self.text) == 0:
            return np.array(uvs)
        for i, c in enumerate(self.text):
            entry = self._font_map['characters'][c]
            uvs.append(np.array([entry['x'], entry['y'] + entry['height']], dtype = np.float32))
            uvs.append(np.array([entry['x'], entry['y']], dtype = np.float32))
            uvs.append(np.array([entry['x']+entry['width'], entry['y']+entry['height']], dtype = np.float32))
            uvs.append(np.array([entry['x']+entry['width'], entry['y']], dtype = np.float32))
        uvs = np.array(uvs, dtype=np.float32)
        uvs[:,0] = uvs[:,0]/self.tex.shape[1]
        uvs[:,1] = uvs[:,1]/self.tex.shape[0]
        return uvs
    
    def generate_mesh_vertices(self):
        n_characters = len(self.text)
        if n_characters == 0:
            return np.array([], dtype=np.float32)
        character_width = self.width/n_characters
        verts = []
        for i, c in enumerate(self.text):
            character_height = self.height
            if c == ',' or c == '_':
                character_height = character_height/4.0
            verts.append(np.array([self.x0+(character_width*i), self.y0, 0], dtype=np.float32))
            verts.append(np.array([self.x0+(character_width*i), self.y0+character_height, 0], dtype=np.float32))
            verts.append(np.array([self.x0+(character_width*i)+character_width, self.y0, 0], dtype=np.float32))
            verts.append(np.array([self.x0+(character_width*i)+character_width, self.y0+character_height, 0], dtype=np.float32))
        return np.array(verts)

    def generate_mesh_triangles(self):
        tris = []
        for i in range(len(self.text)):
            tris.append(np.array([i*4, i*4 + 1, i*4 + 2], dtype=np.uint32))
            tris.append(np.array([i*4+1, i*4 + 3, i*4 + 2], dtype=np.uint32))
        return np.array(tris)

class CubeRenderer(PointCloudRenderer):
    def __init__(self, center):
        super().__init__()
        self.center = center
        self.vertex_buffer, self.elements = generate_cube_vertices_and_triangles(center)
        self.render_mode = RenderMode.ELEMENTS
