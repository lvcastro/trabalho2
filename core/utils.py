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

# def setup_texture_buffer(program, textures_list):
#     buffer = glGenBuffers(1)
#     textures = np.zeros(len(textures_list), [("position", np.float32, 2)])
#     textures['position'] = textures_list
#     glBindBuffer(GL_ARRAY_BUFFER, buffer)
#     glBufferData(GL_ARRAY_BUFFER, textures.nbytes, textures, GL_STATIC_DRAW)

#     stride = textures.strides[0]
#     offset = ctypes.c_void_p(0)
#     loc = glGetAttribLocation(program, "texture_coord")
#     glEnableVertexAttribArray(loc)
#     glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)

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
    """Callback para tratar eventos de teclado relacionados aos objetos"""
    # Variáveis para controle de objetos
    velocidade_movimento = 0.1  # Velocidade de translação
    velocidade_rotacao = 5.0    # Velocidade de rotação em graus
    velocidade_escala = 0.001     # Velocidade de escala
    escala_minima = 0.05
    
    # Só processa teclas quando são pressionadas ou mantidas pressionadas
    if action != glfw.PRESS and action != glfw.REPEAT:
        return
    
    # TRANSLAÇÃO - Controlada pelas setas direcionais
    if objeto_translacao:
        x, y, z = objeto_translacao.position
        
    # Controles no eixo Z
    if key == glfw.KEY_RIGHT:
        z -= velocidade_movimento
    elif key == glfw.KEY_LEFT:
        z += velocidade_movimento
    
    # Controles nos eixos Y (com Shift pressionado) e X
    elif key == glfw.KEY_UP:
        if mods & glfw.MOD_SHIFT:
            y += velocidade_movimento
        else:
            x -= velocidade_movimento
    elif key == glfw.KEY_DOWN:
        if mods & glfw.MOD_SHIFT:
            y -= velocidade_movimento
        else:
            x += velocidade_movimento
    
    objeto_translacao.set_position(x, y, z)
    
    # ROTAÇÃO
    if objeto_rotacao:
        r_x, r_y, r_z = objeto_rotacao.rotation
        
        # # Rotação em torno do eixo X
        # if key == glfw.KEY_Y:
        #     r_x += velocidade_rotacao
        # elif key == glfw.KEY_H:
        #     r_x -= velocidade_rotacao
        
        # Rotação em torno do eixo Y
        if key == glfw.KEY_U:
            r_y += velocidade_rotacao
        elif key == glfw.KEY_J:
            r_y -= velocidade_rotacao
        
        # # Rotação em torno do eixo Z
        elif key == glfw.KEY_I:
            r_z += velocidade_rotacao

        elif key == glfw.KEY_K:
            r_z -= velocidade_rotacao
        
    objeto_rotacao.set_rotation(r_x, r_y, r_z)
    
    # ESCALA - Controlada pelas teclas S + setas
    if objeto_escala:
        sx, sy, sz = objeto_escala.scale
        
        # Escala no eixo X
        if key == glfw.KEY_Z:  # Aumenta X
            sx += velocidade_escala
        elif key == glfw.KEY_X:  # Diminui X
            sx = max(escala_minima, sx - velocidade_escala)
        
        # Escala no eixo Y
        # elif key == glfw.KEY_C:  # Aumenta Y
        #     sy += velocidade_escala
        # elif key == glfw.KEY_V:  # Diminui Y
        #     sy = max(escala_minima, sy - velocidade_escala)
        
        # # Escala no eixo Z
        # elif key == glfw.KEY_B:  # Aumenta Z
        #     sz += velocidade_escala
        # elif key == glfw.KEY_N:  # Diminui Z
        #     sz = max(escala_minima, sz - velocidade_escala)

        # # Escala uniforme (todos os eixos)
        # elif key == glfw.KEY_EQUAL or key == glfw.KEY_KP_ADD:  # Aumenta todos
        #     sx += velocidade_escala
        #     sy += velocidade_escala
        #     sz += velocidade_escala
        # elif key == glfw.KEY_MINUS or key == glfw.KEY_KP_SUBTRACT:  # Diminui todos
        #     sx = max(escala_minima, sx - velocidade_escala)
        #     sy = max(escala_minima, sy - velocidade_escala)
        #     sz = max(escala_minima, sz - velocidade_escala)
        
        objeto_escala.set_scale(sx, sy, sz)

def combine_callbacks(*callbacks):
    """Combina múltiplos callbacks em um único"""
    def combined_callback(window, key, scancode, action, mods):
        for callback in callbacks:
            if callback:
                callback(window, key, scancode, action, mods)
    return combined_callback