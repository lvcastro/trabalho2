# %%
import glfw
from OpenGL.GL import *
from core.shader import Shader
from core import utils
from core.camera import Camera
import objetos.objetos as obj
import numpy as np

# # %%
# CRIANDO A JANELA
altura = 1080
largura = 1080
window = utils.criar_janela(altura, largura)

# %%
# DEFININDO SHADERS E CRIANDO PROGRAMA
ourShader = Shader("vertex_shader.vs", "fragment_shader.fs")
ourShader.use()

program = ourShader.getProgram()

# %%
# CONFIGURAÇÕES DE EXIBIÇÃO
glEnable(GL_TEXTURE_2D)
glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
glEnable( GL_BLEND )
glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
glEnable(GL_LINE_SMOOTH)

# LISTA DE VERTICES E TEXTURA USADA NO PROGRAMA
global vertices_list
vertices_list = []    
global textures_coord_list
textures_coord_list = []
eixos_vertices = np.array([
    # eixo X (vermelho)
    # 0.0, 0.0, 0.0,
    # 5.0, 0.0, 0.0,

    # eixo Y (verde)
    0.0, 0.0, 0.0,
    0.0, 5.0, 0.0,

    # eixo Z (azul)
    0.0, 0.0, 0.0,
    0.0, 0.0, 5.0,
], dtype=np.float32)

eixos_cores = np.array([
    1, 0, 0, 1,  # vermelho para X
    1, 0, 0, 1,

    0, 1, 0, 1,  # verde para Y
    0, 1, 0, 1,

    0, 0, 1, 1,  # azul para Z
    0, 0, 1, 1,
], dtype=np.float32)
# %%
# CARREGA OBJETOS
casa = obj.Casa()
casa.carregar_objeto(vertices_list, textures_coord_list)
casa.set_position(0.0, -2.0, 0.0)
casa.set_scale(5, 5, 5)
# casa.set_rotation(90, 0, 1, 0)
casa.set_rotation(0, 90, 0)

cama = obj.Cama()
cama.carregar_objeto(vertices_list, textures_coord_list)
cama.set_position(-7.0, -0.5, 0.0)
cama.set_scale(0.75, 0.75, 0.75)

mesa = obj.Mesa()
mesa.carregar_objeto(vertices_list, textures_coord_list)
mesa.set_position(-6.0, -0.5, 3.0)
mesa.set_scale(4, 4, 4)
# mesa.set_rotation(90, 0, 1, 0)
mesa.set_rotation(0, 90, 0)
relogio = obj.Relogio()
relogio.carregar_objeto(vertices_list, textures_coord_list)
relogio.set_position(-6.0, 1.25, 3.0)
relogio.set_scale(0.1, 0.1, 0.1)
# relogio.set_rotation(90, 0, 1, 0)
relogio.set_rotation(0, 90, 0)

# banco = obj.Banco()
# banco.carregar_objeto(vertices_list, textures_coord_list)
# banco.set_position(-4.0, 0.0, -20.0)

# placa = obj.Placa()
# placa.carregar_objeto(vertices_list, textures_coord_list)
# placa.set_position(-4.0, 0.0, -10)
# placa.set_scale(0.05, 0.05, 0.05)

# chao = obj.Chao()
# chao.carregar_objeto(vertices_list, textures_coord_list)
# chao.set_position(0.0, -4.0, -20.0)

# skybox = obj.Skybox()
# skybox.carregar_objeto(vertices_list, textures_coord_list)
# skybox.set_position(0.0, 8.0, -20.0)

# %%
# BUFFERS DE VERTICE E TEXTURA
utils.setup_vertex_buffer(program, vertices_list)
utils.setup_texture_buffer(program, textures_coord_list)

### APAGAR DEPOIS
# CRIAÇÃO DOS BUFFERS DOS EIXOS
eixos_vao = glGenVertexArrays(1)
glBindVertexArray(eixos_vao)

# VBO dos vértices dos eixos
eixos_vbo_vertices = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, eixos_vbo_vertices)
glBufferData(GL_ARRAY_BUFFER, eixos_vertices.nbytes, eixos_vertices, GL_STATIC_DRAW)
glEnableVertexAttribArray(0)  # layout location 0 (posição)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

# VBO das cores dos eixos
eixos_vbo_cores = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, eixos_vbo_cores)
glBufferData(GL_ARRAY_BUFFER, eixos_cores.nbytes, eixos_cores, GL_STATIC_DRAW)
glEnableVertexAttribArray(1)  # layout location 1 (cor)
glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 0, None)

glBindBuffer(GL_ARRAY_BUFFER, 0)
glBindVertexArray(0)

# %%
utils.configurar_objetos_manipulaveis(
    obj_translacao=cama,    # Objeto que será movido
    obj_rotacao=relogio,    # Objeto que será rotacionado 
    obj_escala=mesa         # Objeto que será escalado
)
# CRIA A CAMERA
camera = Camera(largura, altura)

key_callback_combinado = utils.combine_callbacks(camera.key_event, utils.objeto_key_event)

# CALLBACKS    
glfw.set_key_callback(window, key_callback_combinado)
glfw.set_framebuffer_size_callback(window, utils.framebuffer_size_callback)
glfw.set_cursor_pos_callback(window, camera.mouse_callback)
glfw.set_scroll_callback(window, camera.scroll_callback)

# tell GLFW to capture our mouse
glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

# %%
# ABRE A JANELA E FAZ O DESENHO
glfw.show_window(window)
glEnable(GL_DEPTH_TEST) ### importante para 3D
   
while not glfw.window_should_close(window):

    currentFrame = glfw.get_time()
    camera.deltaTime = currentFrame - camera.lastFrame
    camera.lastFrame = currentFrame

    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    
    # DESENHA OBJETOS
    cama.desenhar(program)
    mesa.desenhar(program)
    relogio.desenhar(program)
    # banco.desenhar(program)
    # chao.desenhar(program)
    # placa.desenhar(program)
    # skybox.desenhar(program)
    casa.desenhar(program)
    # glBindVertexArray(eixos_vao)
    # glDrawArrays(GL_LINES, 0, 6)
    # glBindVertexArray(0)
    
    mat_view = camera.view()
    loc_view = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(loc_view, 1, GL_TRUE, mat_view)

    mat_projection = camera.projection(largura, altura)
    loc_projection = glGetUniformLocation(program, "projection")
    glUniformMatrix4fv(loc_projection, 1, GL_TRUE, mat_projection)

    glfw.swap_buffers(window)

glfw.terminate()