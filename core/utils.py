# %%
import glfw
from OpenGL.GL import *
import math
import glm
import numpy as np

def criar_janela(altura, largura):
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)

    window = glfw.create_window(altura, largura, "Programa", None, None)

    if (window == None):
        print("Failed to create GLFW window")
        glfw.terminate()
        
    glfw.make_context_current(window)
    return window

# def definir_shader():
#     ourShader = Shader("vertex_shader.vs", "fragment_shader.fs")
#     ourShader.use()

'''
É possível encontrar, na Internet, modelos .obj cujas faces não sejam triângulos. Nesses casos, precisamos gerar triângulos a partir dos vértices da face.
A função abaixo retorna a sequência de vértices que permite isso. Créditos: Hélio Nogueira Cardoso e Danielle Modesti (SCC0650 - 2024/2).
'''
def circular_sliding_window_of_three(arr):
    if len(arr) == 3:
        return arr
    circular_arr = arr + [arr[0]]
    result = []
    for i in range(len(circular_arr) - 2):
        result.extend(circular_arr[i:i+3])
    return result

def framebuffer_size_callback(window, largura, altura):
    # make sure the viewport matches the new window dimensions note that width and 
    # height will be significantly larger than specified on retina displays.
    glViewport(0, 0, largura, altura)

def model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z):
    
    angle = math.radians(angle)
    
    matrix_transform = glm.mat4(1.0) # instanciando uma matriz identidade
       
    # aplicando translacao (terceira operação a ser executada)
    matrix_transform = glm.translate(matrix_transform, glm.vec3(t_x, t_y, t_z))    
    
    # aplicando rotacao (segunda operação a ser executada)
    if angle!=0:
        matrix_transform = glm.rotate(matrix_transform, angle, glm.vec3(r_x, r_y, r_z))
    
    # aplicando escala (primeira operação a ser executada)
    matrix_transform = glm.scale(matrix_transform, glm.vec3(s_x, s_y, s_z))
    matrix_transform = np.array(matrix_transform)
    
    return matrix_transform

def setup_vertex_buffer(program, vertices_list):
    buffer = glGenBuffers(1)
    vertices = np.zeros(len(vertices_list), [("position", np.float32, 3)])
    vertices['position'] = vertices_list
    glBindBuffer(GL_ARRAY_BUFFER, buffer)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    stride = vertices.strides[0]
    offset = ctypes.c_void_p(0)
    loc = glGetAttribLocation(program, "position")
    glEnableVertexAttribArray(loc)
    glVertexAttribPointer(loc, 3, GL_FLOAT, False, stride, offset)
    return buffer

def setup_texture_buffer(program, textures_list):
    buffer = glGenBuffers(1)
    textures = np.zeros(len(textures_list), [("position", np.float32, 2)])
    textures['position'] = textures_list
    glBindBuffer(GL_ARRAY_BUFFER, buffer)
    glBufferData(GL_ARRAY_BUFFER, textures.nbytes, textures, GL_STATIC_DRAW)

    stride = textures.strides[0]
    offset = ctypes.c_void_p(0)
    loc = glGetAttribLocation(program, "texture_coord")
    glEnableVertexAttribArray(loc)
    glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)
    return buffer
