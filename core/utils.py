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

def model(r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z):
    r_x = math.radians(r_x)
    r_y = math.radians(r_y)
    r_z = math.radians(r_z)
    
    matrix_transform = glm.mat4(1.0) # instanciando uma matriz identidade
    
    # aplicando translacao (terceira operação a ser executada)
    matrix_transform = glm.translate(matrix_transform, glm.vec3(t_x, t_y, t_z))    
    
    # aplicando rotacao (segunda operação a ser executada)
    # ordem: Y -> X -> Z (para evitar gimbal lock)
    matrix_transform = glm.rotate(matrix_transform, r_z, [0, 0, 1])
    matrix_transform = glm.rotate(matrix_transform, r_x, [1, 0, 0])
    matrix_transform = glm.rotate(matrix_transform, r_y, [0, 1, 0])
    
    # aplicando escala (primeira operação a ser executada)
    matrix_transform = glm.scale(matrix_transform, glm.vec3(s_x, s_y, s_z))
    matrix_transform = np.array(matrix_transform)
    
    return matrix_transform

def setup_buffers(program, vertices_list, textures_list, normals_list):
    # BUFFER DE VÉRTICE
    buffer_vertice = glGenBuffers(1)
    vertices = np.zeros(len(vertices_list), [("position", np.float32, 3)])
    vertices['position'] = vertices_list
    glBindBuffer(GL_ARRAY_BUFFER, buffer_vertice)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    stride_vertice = vertices.strides[0]
    offset_vertice = ctypes.c_void_p(0)
    loc = glGetAttribLocation(program, "position")
    glEnableVertexAttribArray(loc)
    glVertexAttribPointer(loc, 3, GL_FLOAT, False, stride_vertice, offset_vertice)

    # BUFFER DE TEXTURA
    buffer_textura = glGenBuffers(1)
    texturas = np.zeros(len(textures_list), [("position", np.float32, 2)])
    texturas['position'] = textures_list
    glBindBuffer(GL_ARRAY_BUFFER, buffer_textura)
    glBufferData(GL_ARRAY_BUFFER, texturas.nbytes, texturas, GL_STATIC_DRAW)

    stride_textura = texturas.strides[0]
    offset_textura = ctypes.c_void_p(0)
    loc = glGetAttribLocation(program, "texture_coord")
    glEnableVertexAttribArray(loc)
    glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride_textura, offset_textura)

    # BUFFER DE NORMAL
    buffer_normal = glGenBuffers(1)
    normais = np.zeros(len(normals_list), [("position", np.float32, 3)])
    normais['position'] = normals_list
    glBindBuffer(GL_ARRAY_BUFFER, buffer_normal)
    glBufferData(GL_ARRAY_BUFFER, normais.nbytes, normais, GL_STATIC_DRAW)

    stride_normal = normais.strides[0]
    offset_normal = ctypes.c_void_p(0)
    loc = glGetAttribLocation(program, "normals")
    glEnableVertexAttribArray(loc)
    glVertexAttribPointer(loc, 3, GL_FLOAT, False, stride_normal, offset_normal)

from PIL import Image
import numpy as np
from OpenGL.GL import *

def load_cubemap(faces):
    textureID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_CUBE_MAP, textureID)

    for i, face in enumerate(faces):
        image = Image.open(face).convert('RGB')
        image_data = np.array(image, dtype=np.uint8)
        width, height = image.size
        glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)

    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)

    return textureID

# Objetos específicos para manipulação
objeto_translacao = None  # O objeto que será transladado
objeto_rotacao = None     # O objeto que será rotacionado
objeto_escala = None      # O objeto que será escalado

def definir_objetos_manipulaveis(obj_translacao, obj_rotacao, obj_escala):
    """Define quais objetos serão manipulados por translação, rotação e escala"""
    global objeto_translacao, objeto_rotacao, objeto_escala
    objeto_translacao = obj_translacao
    objeto_rotacao = obj_rotacao
    objeto_escala = obj_escala

def objeto_key_event(window, key, scancode, action, mods):
        pass

ambiente_intensidade = 0.5
diffuse_intensidade = 0.4
specular_intensidade = 0.0
estado_luzes = [True, True, True, True, True, True]

def iluminacao_key_callback(window, key, scancode, action, mods):
    global ambiente_intensidade, diffuse_intensidade, specular_intensidade, estado_luzes

    if action == glfw.PRESS or action == glfw.REPEAT:
        # Intensidade ambiente
        if key == glfw.KEY_KP_ADD or key == glfw.KEY_EQUAL:
            print("1")
            ambiente_intensidade = min(1.0, ambiente_intensidade + 0.05)
        elif key == glfw.KEY_KP_SUBTRACT or key == glfw.KEY_MINUS:
            print("2")
            ambiente_intensidade = max(0.0, ambiente_intensidade - 0.05)

        # Difusa
        elif key == glfw.KEY_T:
            print("3")
            diffuse_intensidade = min(1.0, diffuse_intensidade + 0.05)
        elif key == glfw.KEY_Y:
            print("4")
            diffuse_intensidade = max(0.0, diffuse_intensidade - 0.05)

        # Especular
        elif key == glfw.KEY_G:
            print("5")
            specular_intensidade = min(1.0, specular_intensidade + 0.05)
        elif key == glfw.KEY_H:
            print("6")
            specular_intensidade = max(0.0, specular_intensidade - 0.05)

        # Interruptores das luzes
        elif key == glfw.KEY_1:
            print("7")
            estado_luzes[0] = not estado_luzes[0]
        elif key == glfw.KEY_2:
            estado_luzes[1] = not estado_luzes[1]
        elif key == glfw.KEY_3:
            estado_luzes[2] = not estado_luzes[2]
        elif key == glfw.KEY_4:
            estado_luzes[3] = not estado_luzes[3]
        elif key == glfw.KEY_5:
            estado_luzes[4] = not estado_luzes[4]
        elif key == glfw.KEY_6:
            estado_luzes[5] = not estado_luzes[5]


def combine_callbacks(*callbacks):
    """Combina múltiplos callbacks em um único"""
    def combined_callback(window, key, scancode, action, mods):
        for callback in callbacks:
            if callback:
                callback(window, key, scancode, action, mods)
    return combined_callback