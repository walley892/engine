import numpy as np
from math import sin, cos

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

class Transform(object):
    
    def look_at(self, target):
        D = normalize(self.position - target)
        up = np.array([0, 1, 0])
        R = normalize(np.cross(up, D))
        U = normalize(np.cross(D, R))
        
        self.transformation = np.array(
            [
                [R[0], R[1], R[2], self.position[0]],
                [U[0], U[1], U[2], self.position[1]],
                [D[0], D[1], D[2], self.position[2]],
                [0,0,0,1],
            ]
        )

    
    @classmethod
    def x_rotation(cls, deg):
        return np.array(
            [
                [1, 0, 0, 0],
                [0, cos(deg), -sin(deg), 0],
                [0, sin(deg), cos(deg), 0],
                [0, 0, 0, 1],
            ]
        )
    
    @classmethod
    def y_rotation(cls, deg):
        return np.array(
            [
                [cos(deg), 0, sin(deg), 0],
                [0, 1, 0, 0],
                [-sin(deg), 0, cos(deg), 0],
                [0, 0, 0, 1],
            ]
        )
    
    @classmethod
    def z_rotation(cls, deg):
        return np.array(
            [
                [cos(deg), -sin(deg), 0, 0],
                [sin(deg), cos(deg), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )
    
    def __init__(self):
        self.rotation_matrix = np.identity(4)
        self.translation_matrix = np.identity(4)
        self.scale_matrix = np.identity(4)
         
    @property
    def position(self):
        return self.transformation[:3, 3]

    @property
    def transformation(self):
        return np.matmul(self.translation_matrix, np.matmul(self.rotation_matrix, self.scale_matrix))

    def rotate(self, x, y, z):
        self.rotation_matrix = np.matmul(np.matmul(np.matmul(self.z_rotation(z), self.y_rotation(y)), self.x_rotation(x)), self.rotation_matrix)
    
    def reset(self):
        self.rotation_matrix = np.identity(4)
        self.translation_matrix = np.identity(4)
        self.scale_matrix = np.identity(4)

    def scale(self, x, y, z):
        #self.translation_matrix = np.matmul(self.translation_matrix, np.identity(4)*x)
        #self.translation_matrix[:3, 3] *= x
        self.scale_matrix[0, 0] *= x
        self.scale_matrix[1, 1] *= y
        self.scale_matrix[2, 2] *= z
    
    def translate(self, x, y, z):
        self.translation_matrix[0, 3] += x
        self.translation_matrix[1, 3] += y
        self.translation_matrix[2, 3] += z
