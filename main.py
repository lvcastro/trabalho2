# %%
import glfw
from OpenGL.GL import *
from core.shader import Shader
from core import utils
from core.camera import Camera
import objetos.objetos as obj

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

# %%
# CARREGA OBJETOS
cama = obj.Cama()
cama.carregar_objeto(vertices_list, textures_coord_list)
cama.set_position(2.0, 0.0, -20.0)
cama.set_rotation(-90, 0, 1, 0)

relogio = obj.Relogio()
relogio.carregar_objeto(vertices_list, textures_coord_list)
relogio.set_position(-2.2, 2.5, -18.5)
relogio.set_scale(0.25, 0.25, 0.25)

mesa = obj.Mesa()
mesa.carregar_objeto(vertices_list, textures_coord_list)
mesa.set_position(-2.2, 0.0, -18.5)
mesa.set_scale(6, 6, 6)

banco = obj.Banco()
banco.carregar_objeto(vertices_list, textures_coord_list)
banco.set_position(-4.0, 0.0, -20)

placa = obj.Placa()
placa.carregar_objeto(vertices_list, textures_coord_list)
placa.set_position(-4.0, 0.0, -10)
placa.set_scale(0.05, 0.05, 0.05)

chao = obj.Chao()
chao.carregar_objeto(vertices_list, textures_coord_list)
chao.set_position(0.0, -4.0, -20)

skybox = obj.Skybox()
skybox.carregar_objeto(vertices_list, textures_coord_list)
skybox.set_position(0.0, 8.0, -20)

# %%
# BUFFERS DE VERTICE E TEXTURA
utils.setup_vertex_buffer(program, vertices_list)
utils.setup_texture_buffer(program, textures_coord_list)

# %%
# CRIA A CAMERA
camera = Camera(largura, altura)

# CALLBACKS    
glfw.set_key_callback(window, camera.key_event)
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
    relogio.desenhar(program)
    mesa.desenhar(program)
    banco.desenhar(program)
    chao.desenhar(program)
    placa.desenhar(program)
    skybox.desenhar(program)
    
    mat_view = camera.view()
    loc_view = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(loc_view, 1, GL_TRUE, mat_view)

    mat_projection = camera.projection(largura, altura)
    loc_projection = glGetUniformLocation(program, "projection")
    glUniformMatrix4fv(loc_projection, 1, GL_TRUE, mat_projection)

    glfw.swap_buffers(window)

glfw.terminate()