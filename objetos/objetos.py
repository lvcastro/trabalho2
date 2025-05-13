from OpenGL.GL import *
import loaders
from core import utils

class Object3D:
    def __init__(self, obj_file=None, texture_file=None, cor=None):
        self.verticeInicial = 0
        self.quantosVertices = 0
        self.texture_id = None
        self.position = [0.0, 0.0, -20.0]  # posição padrão (x, y, z)
        self.rotation = [0.0, 0.0, 0.0]  # angulo em graus (x, y, z)
        self.scale = [1.0, 1.0, 1.0]  # escala x, y, z
        self.obj_file = obj_file
        self.texture_file = texture_file
        self.cor = cor

    def carregar_objeto(self, vertices_list, textures_coord_list):
        self.verticeInicial, self.quantosVertices, self.texture_id = loaders.load_obj_and_texture(
            self.obj_file,
            [self.texture_file] if self.texture_file else [],
            vertices_list,
            textures_coord_list
        )
    
    def set_position(self, x, y, z):
            self.position = [x, y, z]
            
    def set_rotation(self, x, y, z):
        self.rotation = [x, y, z]

    def set_scale(self, x, y, z):
        self.scale = [x, y, z]

    def desenhar(self, program):
        # Obtém valores de transformação
        r_x, r_y, r_z = self.rotation
        t_x, t_y, t_z = self.position
        s_x, s_y, s_z = self.scale
        
        # Aplica transformações
        mat_model = utils.model(r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
        loc_model = glGetUniformLocation(program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
        
        # Configura o uso de textura ou cor sólida
        loc_usar_textura = glGetUniformLocation(program, "usarTextura")
        
        if self.texture_id is not None and self.cor is None:
            # Usa textura
            glUniform1i(loc_usar_textura, GL_TRUE)  # Habilita textura no shader
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
        else:
            # Usa cor sólida
            loc_color = glGetUniformLocation(program, "color")
            glUniform1i(loc_usar_textura, GL_FALSE)  # Desabilita textura no shader
            glUniform4f(loc_color, *self.cor, 1.0)
            
        # Desenha o objeto
        glDrawArrays(GL_TRIANGLES, self.verticeInicial, self.quantosVertices)

class Cama(Object3D):
    def __init__(self):
        super().__init__(
            obj_file='objetos/cama/Maya_Bed.obj',
            texture_file='objetos/cama/cama.jpg'
        )
        # Define os limites da casa onde a cama pode ser posicionada
        self.limites_casa = {
            'min_x': -6.5,  # Ajuste conforme as dimensões da sua casa
            'max_x': 6.5,
            'min_z': -6.5,
            'max_z': 6.5,
            'min_y': -1.0,
            'max_y': 4.0
        }
        
        # Dimensões aproximadas da cama
        self.dimensoes_cama = {
            'largura': 2.0,  # Largura da cama (eixo X)
            'altura': 1.0, # Altura da cama (eixo Y)
            'comprimento': 3.0   # Comprimento da cama (eixo Z)
        }
    
    def set_position(self, x, y, z):
        # Calcula as bordas da cama considerando sua posição e dimensões
        meia_largura = self.dimensoes_cama['largura'] / 2
        meio_comprimento = self.dimensoes_cama['comprimento'] / 2
        
        # Limita as coordenadas x e z para manter a cama dentro da casa
        limited_x = max(self.limites_casa['min_x'] + meia_largura, 
                      min(self.limites_casa['max_x'] - meia_largura, x))
        
        limited_y = max(self.limites_casa['min_y'], 
                      min(self.limites_casa['max_y'], y))
        
        limited_z = max(self.limites_casa['min_z'] + meio_comprimento, 
                      min(self.limites_casa['max_z'] - meio_comprimento, z))
        
        # Atualiza a posição com os valores limitados
        self.position = [limited_x, limited_y, limited_z]
        
        # Retorna se a posição foi limitada (True se foi alterada)
        return x != limited_x or z != limited_z

class Relogio(Object3D):
    def __init__(self):
        super().__init__(
            obj_file='objetos/relogio/relogio2.obj', 
            texture_file='objetos/relogio/relogio2.png'
        )

class Mesa(Object3D):
    def __init__(self):
        super().__init__(
            obj_file='objetos/mesa/mesa.obj', 
            texture_file='objetos/mesa/Wood1_Albedo.png'
        )

class Banco(Object3D):
    def __init__(self):
            super().__init__(
                obj_file='objetos/banco/bench.obj', 
                texture_file='objetos/banco/benchs_diffuse.jpg'
            )

class Chao(Object3D):
    def __init__(self):
            super().__init__(
                obj_file='objetos/chao/chao.obj', 
                texture_file='objetos/chao/grama.jpg'
            )

class Placa(Object3D):
    def __init__(self):
            super().__init__(
                obj_file='objetos/placa/placa.obj', 
                texture_file='objetos/placa/placa.jpg'
            )

class Skybox(Object3D):
    def __init__(self):
            super().__init__(
                obj_file='objetos/skybox/skybox.obj', 
                texture_file='objetos/skybox/ceu.png'
                # cor=[0.0667, 0.9294, 0.9098]
            )

class Casa(Object3D):
    def __init__(self):
        super().__init__(
            obj_file='objetos/casa/casa.obj', 
            texture_file='objetos/casa/Diffuse.png'
        )

class Bicicleta(Object3D):
    def __init__(self):
        super().__init__(
            obj_file='objetos/bicicleta/bicicleta.obj', 
            texture_file='objetos/bicicleta/bicicleta.jpg'
        )

# class Quarto(Object3D):
#     def __init__(self):
#         super().__init__(
#             obj_file='objetos/quarto/quarto.obj',
            # cor=[0.9, 0.85, 0.7]  # Cor bege claro para o quarto
#         )