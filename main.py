# %%
import glfw
from OpenGL.GL import *
from core.shader import Shader
from core import utils
from core.camera import Camera
import objetos.objetos as obj
import numpy as np
import loaders
import glm

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

skyboxShader = Shader("skybox_vertex.vs", "skybox_fragment.fs")
skyboxShader.use()

skyboxProgram = skyboxShader.getProgram()

skybox_vertices = np.array([
    -1,  1, -1,  -1, -1, -1,   1, -1, -1,
     1, -1, -1,   1,  1, -1,  -1,  1, -1,

    -1, -1,  1,  -1, -1, -1,  -1,  1, -1,
    -1,  1, -1,  -1,  1,  1,  -1, -1,  1,

     1, -1, -1,   1, -1,  1,   1,  1,  1,
     1,  1,  1,   1,  1, -1,   1, -1, -1,

    -1, -1,  1,  -1,  1,  1,   1,  1,  1,
     1,  1,  1,   1, -1,  1,  -1, -1,  1,

    -1,  1, -1,   1,  1, -1,   1,  1,  1,
     1,  1,  1,  -1,  1,  1,  -1,  1, -1,

    -1, -1, -1,  -1, -1,  1,   1, -1, -1,
     1, -1, -1,  -1, -1,  1,   1, -1,  1
], dtype=np.float32)

skybox_VAO = glGenVertexArrays(1)
skybox_VBO = glGenBuffers(1)

glBindVertexArray(skybox_VAO)
glBindBuffer(GL_ARRAY_BUFFER, skybox_VBO)
glBufferData(GL_ARRAY_BUFFER, skybox_vertices.nbytes, skybox_vertices, GL_STATIC_DRAW)
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * skybox_vertices.itemsize, ctypes.c_void_p(0))
glBindVertexArray(0)

faces = [
    "objetos/skybox/posx.jpg", # direita
    "objetos/skybox/negx.jpg", # esquerda
    "objetos/skybox/posy.jpg", # cima
    "objetos/skybox/negy.jpg", # baixo
    "objetos/skybox/posz.jpg", # frente
    "objetos/skybox/negz.jpg" # trás
]

cubemap_texture = utils.load_cubemap(faces)
# %%
# CONFIGURAÇÕES DE EXIBIÇÃO
# glEnable(GL_TEXTURE_2D)
glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
glEnable( GL_BLEND )
glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
glEnable(GL_LINE_SMOOTH)

# LISTA DE VERTICES E TEXTURA USADA NO PROGRAMA
global vertices_list
vertices_list = []    
global textures_coord_list
textures_coord_list = []
global normals_list
normals_list = []
# %%
# CARREGA OBJETOS

# tv = obj.Tv()

casa = obj.Casa()
casa.carregar_objeto(vertices_list, textures_coord_list, normals_list)
casa.set_position(0.0, -2.0, 0.0)
casa.set_scale(5, 5, 5)
casa.set_rotation(0, 90, 0)

cama = obj.Cama()
cama.carregar_objeto(vertices_list, textures_coord_list, normals_list)
cama.set_position(-9.0, -0.75, 0.0)
cama.set_scale(0.75, 0.75, 0.75)

mesa = obj.Mesa()
mesa.carregar_objeto(vertices_list, textures_coord_list, normals_list)
mesa.set_position(-7.0, -0.8, 3.2)
mesa.set_scale(4, 4, 4)
mesa.set_rotation(0, 90, 0)

relogio = obj.Relogio()
relogio.carregar_objeto(vertices_list, textures_coord_list, normals_list)
relogio.set_position(-7.0, 1.1, 3.2)
relogio.set_scale(0.09, 0.09, 0.09)

chao = obj.Chao()
chao.carregar_objeto(vertices_list, textures_coord_list, normals_list)
chao.set_position(0.0, -2.0, 0.0)
chao.set_rotation(90, 0, 0)
chao.set_scale(10, 10, 1)

banco = obj.Banco()
banco.carregar_objeto(vertices_list, textures_coord_list, normals_list)
banco.set_position(0.0, -1.25, -20.0)
banco.set_scale(0.05, 0.05, 0.05)

placa = obj.Placa()
placa.carregar_objeto(vertices_list, textures_coord_list, normals_list)
placa.set_position(-10.0, -2.0, -20.0)
placa.set_scale(0.025, 0.025, 0.025)
placa.set_rotation(-90, 0, 0)

bicicleta = obj.Bicicleta()
bicicleta.carregar_objeto(vertices_list, textures_coord_list, normals_list)
bicicleta.set_position(6.8, -2.0, -9.1)
bicicleta.set_rotation(-80, 0, 0)
bicicleta.set_scale(0.075, 0.075, 0.075)

celular = obj.Celular()
celular.carregar_objeto(vertices_list, textures_coord_list, normals_list)
celular.set_position(-6.6, 0.87, 3.2)
celular.set_rotation(0.0, 90.0, 90.0)
celular.set_scale(0.055, 0.055, 0.055)

ventilador = obj.Ventilador()
ventilador.carregar_objeto(vertices_list, textures_coord_list, normals_list)
ventilador.set_position(0, 8.1, 0)
ventilador.set_rotation(0, 90, 0)
ventilador.set_scale(2.5, 2.5, 2.5)

carro = obj.Carro()
carro.carregar_objeto(vertices_list, textures_coord_list, normals_list)
carro.set_scale(2, 2, 2)
carro.set_position(0, -1.5, -30)
carro.set_rotation(0, 90, 0)

luz1 = obj.Luz()
luz1.carregar_objeto(vertices_list, textures_coord_list, normals_list)
luz1.set_position(3.9, -0.1, -28.07)
luz1.set_scale(0.15, 0.15, 0.15)
# luz.set_position(3.9, -0.1, -30.75)
luz2 = obj.Luz()
luz2.carregar_objeto(vertices_list, textures_coord_list, normals_list)
luz2.set_position(3.9, -0.1, -30.75)
luz2.set_scale(0.15, 0.15, 0.15)
luz_celular = obj.Luz_Celular()
luz_celular.carregar_objeto(vertices_list, textures_coord_list, normals_list)
luz_celular.set_position(-6.6, 0.87, 3.2)
luz_celular.set_rotation(0.0, 90.0, 0.0)
luz_celular.set_scale(10, 10, 10)

luz_ventilador = obj.Luz_Ventilador()
luz_ventilador.carregar_objeto(vertices_list, textures_coord_list, normals_list)
luz_ventilador.set_position(0.0, 8.1, 0.0)
luz_ventilador.set_rotation(0.0, 90.0, 0.0)
luz_ventilador.set_scale(10, 10, 10)
# %%
# BUFFERS DE VERTICE E TEXTURA
utils.setup_buffers(program, vertices_list, textures_coord_list, normals_list)

# %%
utils.definir_objetos_manipulaveis(
    obj_translacao=luz1,    # Objeto que será movido
    obj_rotacao=relogio,    # Objeto que será rotacionado 
    obj_escala=banco         # Objeto que será escalado
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
    if camera.malha:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    currentFrame = glfw.get_time()
    camera.deltaTime = currentFrame - camera.lastFrame
    camera.lastFrame = currentFrame

    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(1.0, 1.0, 1.0, 1.0)

    glDepthFunc(GL_LEQUAL)
    glUseProgram(skyboxProgram)

    mat_view = camera.view()
    mat_projection = camera.projection(largura, altura)
    view_skybox = glm.mat4(glm.mat3(camera.view()))  # remove a translação

    glUniformMatrix4fv(glGetUniformLocation(skyboxProgram, "view"), 1, GL_FALSE, glm.value_ptr(view_skybox))
    glUniformMatrix4fv(glGetUniformLocation(skyboxProgram, "projection"), 1, GL_TRUE, mat_projection)

    glBindVertexArray(skybox_VAO)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_CUBE_MAP, cubemap_texture)
    glDrawArrays(GL_TRIANGLES, 0, 36)
    glBindVertexArray(0)
    glDepthFunc(GL_LESS)

    # Ativa o shader
    glUseProgram(program)

    # Atualiza uniforms da câmera
    glUniformMatrix4fv(glGetUniformLocation(program, "view"), 1, GL_TRUE, mat_view)
    glUniformMatrix4fv(glGetUniformLocation(program, "projection"), 1, GL_TRUE, mat_projection)

    # Uniforms da luz (ajuste os valores como quiser)
    # loc_ka = glGetUniformLocation(program, "ka") # recuperando localizacao da variavel ka na GPU
    # loc_kd = glGetUniformLocation(program, "kd") # recuperando localizacao da variavel kd na GPU
    # loc_ks = glGetUniformLocation(program, "ks") # recuperando localizacao da variavel ks na GPU
    # loc_ns = glGetUniformLocation(program, "ns") # recuperando localizacao da variavel ns na GPU
    # glUniform3f(glGetUniformLocation(program, "lightPos"), 3.9, -0.1, -30.75)

    # # Posição da câmera
    glUniform3f(glGetUniformLocation(program, "viewPos"), *camera.cameraPos)
    # directional light
    ourShader.setVec3("dirLight.direction", 0.0, -1.0, 0.0)
    ourShader.setVec3("dirLight.ambient", 0.5, 0.5, 0.5)
    ourShader.setVec3("dirLight.diffuse", 0.4, 0.4, 0.4)
    ourShader.setVec3("dirLight.specular", 0.0, 0.0, 0.0)

    ourShader.setVec3("pointLights[0].position", glm.vec3(4.0, -0.1, -28.07))
    ourShader.setVec3("pointLights[0].ambient", 0.1, 0.1, 0.1)
    ourShader.setVec3("pointLights[0].diffuse", 1.0, 0.95, 0.8)
    ourShader.setVec3("pointLights[0].specular", 1.0, 0.95, 0.8)
    ourShader.setFloat("pointLights[0].constant", 1.0)
    ourShader.setFloat("pointLights[0].linear", 0.09)
    ourShader.setFloat("pointLights[0].quadratic", 0.032)
    ourShader.setBool("pointLights[0].on", True)

    ourShader.setVec3("pointLights[1].position", glm.vec3(4.0, -0.1, -30.75))
    ourShader.setVec3("pointLights[1].ambient", 0.1, 0.1, 0.1)
    ourShader.setVec3("pointLights[1].diffuse", 1.0, 0.95, 0.8)
    ourShader.setVec3("pointLights[1].specular", 1.0, 0.95, 0.8)
    ourShader.setFloat("pointLights[1].constant", 1.0)
    ourShader.setFloat("pointLights[1].linear", 0.09)
    ourShader.setFloat("pointLights[1].quadratic", 0.032)
    ourShader.setBool("pointLights[1].on", True)

    ourShader.setVec3("pointLights[2].position", glm.vec3(-4.0, -0.1, -28.07))
    ourShader.setVec3("pointLights[2].ambient", 0.05, 0.0, 0.0)
    ourShader.setVec3("pointLights[2].diffuse", 0.9, 0.1, 0.1)
    ourShader.setVec3("pointLights[2].specular", 1.0, 0.2, 0.2)
    ourShader.setFloat("pointLights[2].constant", 1.0)
    ourShader.setFloat("pointLights[2].linear", 0.09)
    ourShader.setFloat("pointLights[2].quadratic", 0.032)
    ourShader.setBool("pointLights[2].on", True)

    ourShader.setVec3("pointLights[3].position", glm.vec3(-4.0, -0.1, -30.75))
    ourShader.setVec3("pointLights[3].ambient", 0.05, 0.0, 0.0)
    ourShader.setVec3("pointLights[3].diffuse", 0.9, 0.1, 0.1)
    ourShader.setVec3("pointLights[3].specular", 1.0, 0.2, 0.2)
    ourShader.setFloat("pointLights[3].constant", 1.0)
    ourShader.setFloat("pointLights[3].linear", 0.09)
    ourShader.setFloat("pointLights[3].quadratic", 0.032)
    ourShader.setBool("pointLights[3].on", True)
    # Desenha os objetos
    luz1.desenhar(program)
    luz2.desenhar(program)
    casa.desenhar(program)
    cama.desenhar(program)
    mesa.desenhar(program)
    relogio.desenhar(program)
    banco.desenhar(program)
    chao.desenhar(program)
    placa.desenhar(program)
    bicicleta.desenhar(program)
    celular.desenhar(program)
    ventilador.desenhar(program)
    # luz_celular.desenhar_luz(0.0, 0.0, 1.0, 1.0, 1.0, 1000, program, 'lightPos1')
    # luz_ventilador.desenhar_luz(0.0, 0.0, 1.0, 1.0, 1.0, 1000, program, 'lightPos2')
    carro.desenhar(program)
    # glUniform1i(glGetUniformLocation(program, "isLampada"), True)  # ao desenhar a lâmpada
    # glUniform1i(glGetUniformLocation(program, "isLampada"), False) # ao desenhar o abajur
    # tv.desenhar(program, 1, 0.7, 0.5, 32)
    glfw.swap_buffers(window)

glfw.terminate()