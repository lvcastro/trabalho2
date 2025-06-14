import glfw
from OpenGL.GL import *
from core.shader import Shader
from core import utils
from core.camera import Camera
import objetos.objetos as obj
import numpy as np
import loaders
import glm

# %% CONFIGURAÇÃO DA JANELA
altura = 1080
largura = 1080
window = utils.criar_janela(altura, largura)

# %% SHADERS
ourShader = Shader("vertex_shader.vs", "fragment_shader.fs")
ourShader.use()

program = ourShader.getProgram()

# %% SKYBOX - define a geometria e as texturas do cubo
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
# %% CONFIG OPENGL
glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
glEnable( GL_BLEND )
glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
glEnable(GL_LINE_SMOOTH)

# %% LISTAS DE VÉRTICES GLOBAIS
global vertices_list
vertices_list = []    
global textures_coord_list
textures_coord_list = []
global normals_list
normals_list = []

# %% OBJETOS INTERNOS E EXTERNOS
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
relogio.set_position(-7.2, 1.1, 3.2)
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

# %% BUFFERS
utils.setup_buffers(program, vertices_list, textures_coord_list, normals_list)

# %% CONTROLES E CALLBACKS
camera = Camera(largura, altura)
key_callback_combinado = utils.combine_callbacks(camera.key_event, utils.iluminacao_key_callback)

# Registra os callbacks no GLFW
glfw.set_key_callback(window, key_callback_combinado)
glfw.set_framebuffer_size_callback(window, utils.framebuffer_size_callback)
glfw.set_cursor_pos_callback(window, camera.mouse_callback)
glfw.set_scroll_callback(window, camera.scroll_callback)
glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED) # diz ao GLFW para capturar o mouse

# ABRE A JANELA E FAZ O DESENHO
glfw.show_window(window)
glEnable(GL_DEPTH_TEST)

estado_carro = {"fase": 0, "inicio": glfw.get_time()}

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
    # Ativa o shader da skybox
    glUseProgram(skyboxProgram)

    mat_view = camera.view()
    mat_projection = camera.projection(largura, altura)
    view_skybox = glm.mat4(glm.mat3(camera.view()))  # remove a translação para desenhar a skybox

    glUniformMatrix4fv(glGetUniformLocation(skyboxProgram, "view"), 1, GL_FALSE, glm.value_ptr(view_skybox))
    glUniformMatrix4fv(glGetUniformLocation(skyboxProgram, "projection"), 1, GL_TRUE, mat_projection)

    # DESENHA A SKYBOX
    glBindVertexArray(skybox_VAO)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_CUBE_MAP, cubemap_texture)
    glDrawArrays(GL_TRIANGLES, 0, 36)
    glBindVertexArray(0)
    glDepthFunc(GL_LESS)

    # Ativa o shader do restante dos objetos
    glUseProgram(program)

    # Atualiza uniforms da câmera
    glUniformMatrix4fv(glGetUniformLocation(program, "view"), 1, GL_TRUE, mat_view)
    glUniformMatrix4fv(glGetUniformLocation(program, "projection"), 1, GL_TRUE, mat_projection)

    # Posição da câmera
    glUniform3f(glGetUniformLocation(program, "viewPos"), *camera.cameraPos)

    # --- OBJETOS E LUZES ---
    # Luz direcional (ambiente)
    ourShader.setVec3("dirLight.direction", 0.0, -1.0, 0.0)
    ourShader.setVec3("dirLight.ambient", *(utils.ambiente_intensidade,) * 3)
    ourShader.setVec3("dirLight.diffuse", *(utils.diffuse_intensidade,) * 3)
    ourShader.setVec3("dirLight.specular", *(utils.specular_intensidade,) * 3)

    # Ligar/desligar luzes internas apenas se a câmera estiver dentro
    if utils.camera_dentro_casa(camera):
        for i in [4, 5]:
            ourShader.setBool(f"pointLights[{i}].on", utils.estado_luzes[i])
        for i in [0, 1, 2, 3]:
            ourShader.setBool(f"pointLights[{i}].on", False)
    # Ligar/desligar luzes externas apenas se a câmera estiver fora
    else:
        for i in [0, 1, 2, 3]:
            ourShader.setBool(f"pointLights[{i}].on", utils.estado_luzes[i])
        for i in [4, 5]:
            ourShader.setBool(f"pointLights[{i}].on", False)

    tempo_atual = glfw.get_time()
    tempo_passado = tempo_atual - estado_carro["inicio"]

    # Define o ciclo: 0=indo, 1=parado, 2=voltando, 3=parado
    if estado_carro["fase"] == 0:  # indo pra frente
        mov_x = -10 + tempo_passado * 5
        if tempo_passado >= 4.0:  # anda 4s
            estado_carro["fase"] = 1
            estado_carro["inicio"] = tempo_atual
    elif estado_carro["fase"] == 1:  # pausa
        mov_x = 10
        if tempo_passado >= 1.5:
            estado_carro["fase"] = 2
            estado_carro["inicio"] = tempo_atual
    elif estado_carro["fase"] == 2:  # voltando
        mov_x = 10 - tempo_passado * 5
        if tempo_passado >= 4.0:
            estado_carro["fase"] = 3
            estado_carro["inicio"] = tempo_atual
    elif estado_carro["fase"] == 3:  # pausa
        mov_x = -10
        if tempo_passado >= 1.5:
            estado_carro["fase"] = 0
            estado_carro["inicio"] = tempo_atual

    carro.set_position(mov_x, -1.5, -30)

    # Atualiza as luzes do carro com base no mov_x como antes
    car_pos = glm.vec3(mov_x, -1.5, -30)

    farol_dir_frente_offset = glm.vec3(+4.0, -0.1, -28.07 + 30)  # Z relativo
    farol_dir_tras_offset   = glm.vec3(+4.0, -0.1, -30.75 + 30)

    farol_esq_frente_offset = glm.vec3(-3.5, -0.1, -28.07 + 30)
    farol_esq_tras_offset   = glm.vec3(-3.5, -0.1, -30.75 + 30)

    # ILUMINAÇÃO EXTERNA (luzes do carro)
    ourShader.setVec3("pointLights[0].position", car_pos + farol_dir_frente_offset)
    ourShader.setVec3("pointLights[1].position", car_pos + farol_dir_tras_offset)
    ourShader.setVec3("pointLights[2].position", car_pos + farol_esq_frente_offset)
    ourShader.setVec3("pointLights[3].position", car_pos + farol_esq_tras_offset)

    ourShader.setVec3("pointLights[0].ambient", 0.1, 0.1, 0.1)
    ourShader.setVec3("pointLights[0].diffuse", 1.0, 0.95, 0.8)
    ourShader.setVec3("pointLights[0].specular", 1.0, 0.95, 0.8)
    ourShader.setFloat("pointLights[0].constant", 1.0)
    ourShader.setFloat("pointLights[0].linear", 0.09)
    ourShader.setFloat("pointLights[0].quadratic", 0.032)

    ourShader.setVec3("pointLights[1].ambient", 0.1, 0.1, 0.1)
    ourShader.setVec3("pointLights[1].diffuse", 1.0, 0.95, 0.8)
    ourShader.setVec3("pointLights[1].specular", 1.0, 0.95, 0.8)
    ourShader.setFloat("pointLights[1].constant", 1.0)
    ourShader.setFloat("pointLights[1].linear", 0.09)
    ourShader.setFloat("pointLights[1].quadratic", 0.032)

    ourShader.setVec3("pointLights[2].ambient", 0.05, 0.0, 0.0)
    ourShader.setVec3("pointLights[2].diffuse", 0.9, 0.1, 0.1)
    ourShader.setVec3("pointLights[2].specular", 1.0, 0.2, 0.2)
    ourShader.setFloat("pointLights[2].constant", 1.0)
    ourShader.setFloat("pointLights[2].linear", 0.09)
    ourShader.setFloat("pointLights[2].quadratic", 0.032)

    ourShader.setVec3("pointLights[3].ambient", 0.05, 0.0, 0.0)
    ourShader.setVec3("pointLights[3].diffuse", 0.9, 0.1, 0.1)
    ourShader.setVec3("pointLights[3].specular", 1.0, 0.2, 0.2)
    ourShader.setFloat("pointLights[3].constant", 1.0)
    ourShader.setFloat("pointLights[3].linear", 0.09)
    ourShader.setFloat("pointLights[3].quadratic", 0.032)

    
    # ILUMINAÇÃO INTERNA
    # Ventilador
    ventilador_pos_luz = glm.vec3(ventilador.position[0], 
                                  ventilador.position[1] - 2.0, 
                                  ventilador.position[2] )
    ourShader.setVec3("pointLights[4].position", ventilador_pos_luz)
    ourShader.setVec3("pointLights[4].ambient", 1.0, 1.0, 0.7)
    ourShader.setVec3("pointLights[4].diffuse", 1.0, 1.0, 0.7)
    ourShader.setVec3("pointLights[4].specular", 0.4, 0.4, 0.2)
    ourShader.setFloat("pointLights[4].constant", 1.0)
    ourShader.setFloat("pointLights[4].linear", 0.09)
    ourShader.setFloat("pointLights[4].quadratic", 0.032)

    # Celular
    celular_pos_luz = glm.vec3(celular.position[0], 
                               celular.position[1] + 1.0, 
                               celular.position[2])
    ourShader.setVec3("dirLight.direction", 0.1, 1.0, 0.1)
    ourShader.setVec3("pointLights[5].position", celular_pos_luz)
    ourShader.setVec3("pointLights[5].ambient", 0.0, 0.0, 0.9)
    ourShader.setVec3("pointLights[5].diffuse", 0.0, 0.0, 1.0)
    ourShader.setVec3("pointLights[5].specular", 0.0, 0.0, 0.2)
    ourShader.setFloat("pointLights[5].constant", 1.0)
    ourShader.setFloat("pointLights[5].linear", 0.09)
    ourShader.setFloat("pointLights[5].quadratic", 0.032)

    # Desenha os objetos
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
    carro.desenhar(program)

    glfw.swap_buffers(window)

glfw.terminate()