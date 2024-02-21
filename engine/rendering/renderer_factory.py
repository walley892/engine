from OpenGL.arrays import vbo
from OpenGL.GL import shaders
from OpenGL.GL import *
import numpy as np
from engine.rendering.c_shaders import *
from enum import Enum
import re


NUMPY_TYPE_TO_GL_TYPE = {
    np.float32: GL_FLOAT,
    np.uint32: GL_UNSIGNED_INT
}

class RenderMode(Enum):
    POINTS = 0
    ELEMENTS = 1


class Renderer(object):
    def __init__(self):
        # a list of vertex buffer objects
        self._attribute_vbos = []
        self._elements = np.array([])
        self._element_vbo = vbo.VBO(np.zeros(9))
        self._queue_texture_update = False
        self._texture_data = np.array([])
        self._gl_shader_id = None
        self._gl_texture_id = None
        self._shader = None
        self._shaders_compiled = False
        self._uniform_update_queue = {}
        self.initialize_gpu_arrays()
        self._render_mode = RenderMode.POINTS
        self._game_object = None
        self._n_points = 0
        self.texture_mode = GL_RGB

    @property
    def game_object(self):
        return self._game_object

    @game_object.setter
    def game_object(self, go):
        self._game_object = go
    
    @property
    def render_mode(self):
        return self._render_mode
    
    @render_mode.setter
    def render_mode(self, mode):
        self._render_mode = mode

    @property
    def static(self):
        return True

    def compile_shaders(self):
        vertex_shader = shaders.compileShader(self.vertex_shader, GL_VERTEX_SHADER)

        fragment_shader = shaders.compileShader(self.fragment_shader, GL_FRAGMENT_SHADER)

        self._shader = shaders.compileProgram(vertex_shader, fragment_shader)

        self._shaders_compiled = True
    
    def initialize_gpu_arrays(self):
        for index, (data_type, count) in enumerate(self.buffer_data_spec):
            self._attribute_vbos.append(
                vbo.VBO(np.zeros(9))
            )

    def queue_update_uniform(self, name, data):
        self._uniform_update_queue[name] = data

    def execute_uniform_updates(self):
        for name, data in self._uniform_update_queue.items():
            self.update_uniform(name, data)
        self._uniform_update_queue = {}

    def update_uniform(self, name, data):
        data_type = self.uniform_data_spec[name]
        location = glGetUniformLocation(self._shader, name)
        if data_type == 'mat4x4':
            glUniformMatrix4fv(
                location,
                1, 
                False,
                data,
            )
        elif data_type == 'int':
            glUniform1i(
                location,
                data,
            )
        elif data_type == 'vec3':
            glUniform3f(
                location,
                data[0],
                data[1],
                data[2],
            )
        elif 'sampler' in data_type:
            self.update_gpu_texture(name, data)

    def update_gpu_texture(self, name, data):
        dimension = len(data.shape) - 1
        if self._gl_texture_id is None:
            self._gl_texture_id = glGenTextures(1)
        if dimension == 3:
            d, h, w = data.shape[:3]
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_3D, self._gl_texture_id)
            glTexImage3D(GL_TEXTURE_3D, 
                0, 
                GL_RGB,
                w,
                h,
                d,
                0,
                self.texture_mode,
                GL_FLOAT,
                data
            )
            glUniform1i(
                glGetUniformLocation(self._shader, name),
                0,
            )
            glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER);
            glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER);
            glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_BORDER);
        elif dimension == 2:
            h, w = data.shape[:2]
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self._gl_texture_id)
            glTexImage2D(GL_TEXTURE_2D, 
                0,
                GL_RGB,
                w,
                h,
                0,
                self.texture_mode,
                GL_FLOAT,
                data
            )
            glUniform1i(
                glGetUniformLocation(self._shader, name),
                0,
            )
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    def update_gpu_array(self, index, data):
        vbo = self._attribute_vbos[index]
        vbo.set_array(data)

    def set_attribute_pointers(self):
        for index, (data_type, count) in enumerate(self.buffer_data_spec):
            vbo = self._attribute_vbos[index]
            vbo.bind()
            glEnableVertexAttribArray(index)
            glBindBuffer(GL_ARRAY_BUFFER, vbo.buffer)
            gl_type = NUMPY_TYPE_TO_GL_TYPE[data_type]
            if gl_type == GL_FLOAT:
                glVertexAttribPointer(
                    index,
                    count, 
                    GL_FLOAT, 
                    GL_FALSE,
                    data_type().itemsize*count, 
                    vbo
                )
            else:
                glVertexAttribIPointer(
                    index,
                    count,
                    gl_type,
                    data_type().itemsize*count,
                    vbo
                )
    
    @property
    def vertex_shader(self):
        return self._vertex_shader

    @vertex_shader.setter
    def vertex_shader(self, vertex_shader):
        self._vertex_shader = vertex_shader
        self.queue_shader_recompile()
        
    @property
    def fragment_shader(self):
        return self._fragment_shader

    @fragment_shader.setter
    def fragment_shader(self, fragment_shader):
        self._fragment_shader = fragment_shader
        self.queue_shader_recompile()
     
    def queue_shader_recompile(self):
        self._shaders_compiled = False

    def setup_draw(self):
        if not self._shaders_compiled:
            self.compile_shaders()
        self.set_attribute_pointers()
        shaders.glUseProgram(self._shader)

    @property
    def shader(self):
        return self._shader
    
    @property
    def n_points(self):
        return self._n_points
    
    @n_points.setter
    def n_points(self, pts):
        self._n_points = pts

    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, elements):
        self._elements = elements
        self._element_vbo.set_array(elements)

    def draw_to_camera(self, camera):
        if self.game_object is None:
            return
        self.rotMat = np.matmul(camera.perspective.transpose(), np.matmul(camera.transform.transformation, self.game_object.get_transform())).transpose()
        self.setup_draw()
        self.execute_uniform_updates()
        if self.render_mode == RenderMode.POINTS:
            glDrawArrays(GL_POINTS, 0, self.n_points)
        elif self.render_mode == RenderMode.ELEMENTS:
            self._element_vbo.bind()
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._element_vbo.buffer)
            glDrawElements(
                GL_TRIANGLES,
                len(self.elements),
                GL_UNSIGNED_INT,
                self._element_vbo,
            )

    def is_clicked(self, x, y, camera):
        if not hasattr(self, 'vertex_buffer'):
            return False
        x = (x - 0.5)*2
        y = (-y + 0.5)*2
        xy = np.array([x, y])
        def area(a, b, c):
            return abs((a[0]*(b[1]-c[1]) + b[0]*(c[1]-a[1])+ c[0]*(a[1]-b[1]))/2.0)
        
        for i in range(0, len(self._elements), 3):
            ai = self._elements[i]
            bi = self._elements[i+1]
            ci = self._elements[i+2]
            a = self.vertex_buffer[ai]
            b = self.vertex_buffer[bi]
            c = self.vertex_buffer[ci]
            proj = np.matmul(camera.perspective.transpose(), np.matmul(camera.transform.transformation, self.game_object.get_transform()))
            a = np.matmul(proj, np.array([a[0], a[1], a[2], 1]))
            b = np.matmul(proj, np.array([b[0], b[1], b[2], 1]))
            c = np.matmul(proj, np.array([c[0], c[1], c[2], 1]))
            if a[3] == 0 or b[3] == 0 or c[3] == 0:
                continue
            a = a[:3]/a[3]
            b = b[:3]/b[3]
            c = c[:3]/c[3]
            if a[2] > 0 and b[2] > 0 and c[2] > 0 and a[2] < 1 and b[2] < 1 and c[2] < 1:
                a1 = area(a, b, xy)
                a2 = area(a, c, xy)
                a3 = area(b, c, xy)
                at = area(a, b, c)
                if abs(a1 + a2 + a3 - at) < 0.02:
                    return True
        return False
class Base(object):
    def foo(self):
        print('foo')

    @property
    def thing(self):
        return 'whatever'

def generate_subclass_with_properties(attributes, setters):
    class Sub(Renderer):
        pass
    def generate_setter(i, attribute_name):
        def setter(self, data):
            self.__dict__["_"+attribute_name] = data
            setters[i](self, data)
        return setter
    def generate_getter(attribute_name):
        def getter(self):
            return self.__getattribute__("_"+attribute_name)
        return getter
    for i, attribute_name in enumerate(attributes):
        # create the 'real' private variable storing the value
        # use whatever default insetad of 'None'
        setattr(Sub, "_"+attribute_name, None)

        # getter just returns the value of the 'real' private variable
        getter = property(generate_getter(attribute_name))
        setattr(Sub, attribute_name, getter)

        setattr(Sub, attribute_name, getter.setter(generate_setter(i, attribute_name)))
    return Sub

GLSL_STR_TO_NP_TYPE = {
    'bool': bool,
    'int': np.int32,
    'uint': np.uint32,
    'float': np.float32,
    'double': np.float64,
    'bvec': bool,
    'ivec': np.int32,
    'uvec': np.uint32,
    'vec': np.float32,
    'dvec': np.float64,
}

def create_renderer_from_string(vertex_shader_str, fragment_shader_str):
    buffer_data_spec, uniform_data_spec = get_shader_inputs(vertex_shader_str + fragment_shader_str)
    data_spec = []
    setters = []
    def generate_buffer_data_setter(index):
        def set_data(self, data):
            self.update_gpu_array(index, data)
        return set_data
    def generate_uniform_data_setter(name):
        def set_data(self, data):
            self.queue_update_uniform(name, data)
        return set_data

    for i, (name, (index, data_type, count)) in enumerate(buffer_data_spec.items()):
        data_spec.append((data_type, count)) 
        setters.append(generate_buffer_data_setter(index))
    
    for i, (name, data_type_str) in enumerate(uniform_data_spec.items()):
        setters.append(generate_uniform_data_setter(name))

    T = generate_subclass_with_properties(
        [key for key in buffer_data_spec] + [key for key in uniform_data_spec],
        setters
    )
    setattr(T, 'buffer_data_spec', data_spec)
    setattr(T, 'uniform_data_spec', uniform_data_spec)
    setattr(T, '_vertex_shader', vertex_shader_str)
    setattr(T, '_fragment_shader', fragment_shader_str)
    return T


def glsl_type_str_to_type_and_count(type_str):
    if 'vec' in type_str:
        data_type = GLSL_STR_TO_NP_TYPE[
            re.findall('.*vec', type_str)[0]
        ]
        count = int(
            re.findall('(?<=vec).', type_str)[0]
        )
        return data_type, count
    else:
        data_type = GLSL_STR_TO_NP_TYPE[
            type_str
        ]
        return data_type, 1

def get_shader_inputs(shader_source):
    buffer_data = {}
    uniform_data = {}
    for line in shader_source.splitlines():
        if 'layout(' in line:
            location = int(re.findall('(?<=location=).', line)[0])
            data_type_str = re.findall('(?<=in ).+(?=\ )', line)[0]
            name = re.findall('(?<={} ).+(?=;)'.format(data_type_str), line)[0]

            data_type, count = glsl_type_str_to_type_and_count(data_type_str)

            buffer_data[name] = (location, data_type, count)
        if 'uniform' in line:
            data_type_str = re.findall('(?<=uniform ).*(?=\ )', line)[0]
            name = re.findall('(?<={} ).+(?=;)'.format(data_type_str), line)[0]
            uniform_data[name] = data_type_str
    return buffer_data, uniform_data
