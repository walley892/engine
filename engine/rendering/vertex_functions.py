import numpy as np
'''
def generate_plane_vertices(center, normal):
    # pick a vector linearly independant from the normal
    # a random vector will "almost certainly" be linearly
    # independent from the given normal ;)
    vec_li = np.random.rand(3)
    vec_li = vec_li/np.linalg.norm(vec_li)
    
    # get a vector orthognal to the normal
    v = np.cross(normal, vec_li)
    #get a vector orthognol to both v and the normal
    w = np.cross(normal, v)
    # compute vertices
    return np.array([
        center - (v + w),
        center - (v - w),
        center - (-v -w),
        center - (-v + w),
    ], dtype=np.float32)

def generate_plane_triangles():
    return np.array([[0, 1, 2], [0,3,2]], dtype=np.uint32)
'''
def generate_plane_vertices():
    
    return np.array([
        [0.5, 0.5, 0],
        [0.5, -0.5, 0],
        [-0.5, -0.5, 0],
        [-0.5, 0.5, 0],
    ], dtype=np.float32)

def generate_plane_triangles():
    return np.array([[0, 1, 2], [0,3,2]], dtype=np.uint32)


def generate_cube_vertices_and_triangles(center):
    cube_vertex_to_index = {}
    cube_triangles = []
    for i in range(3):
        ui = np.zeros(3)
        ui[i] = 0.5
        plane_i_verts = generate_plane_vertices(center + ui, ui)
        for i, vert in enumerate(plane_i_verts):
            if tuple(vert) not in cube_vertex_to_index:
                cube_vertex_to_index[tuple(vert)] = len(cube_vertex_to_index)
        plane_i_triangles = generate_plane_triangles()
        for index in plane_i_triangles.flatten():
            cube_triangles.append(cube_vertex_to_index[tuple(plane_i_verts[index])])
    return np.array(list(cube_vertex_to_index.keys())), np.array(cube_triangles)
