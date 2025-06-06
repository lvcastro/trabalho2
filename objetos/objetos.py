from OpenGL.GL import *
import loaders
from core import utils


from OpenGL.GL import *
import loaders
from core import utils

class Object3D:
    def __init__(self, obj_file=None, textures_map=None, cor=None): # Alterado: texture_file -> textures_map
        self.materiais = []  # Cada item: {'material': str, 'vertice_inicial': int, 'num_vertices': int, 'texture_id': int}
        self.position = [0.0, 0.0, -20.0]
        self.rotation = [0.0, 0.0, 0.0]
        self.scale = [1.0, 1.0, 1.0]
        self.obj_file = obj_file
        self.textures_map = textures_map if textures_map is not None else {} # Alterado: self.texture_file -> self.textures_map
        self.cor = cor

    def carregar_objeto(self, vertices_list, textures_coord_list, normals_list):
        self.materiais = loaders.load_obj_and_texture(
            self.obj_file,
            self.textures_map, # Alterado: passa o dicionário diretamente
            vertices_list,
            textures_coord_list,
            normals_list
        )
    
    def set_position(self, x, y, z):
        self.position = [x, y, z]
            
    def set_rotation(self, x, y, z):
        self.rotation = [x, y, z]

    def set_scale(self, x, y, z):
        self.scale = [x, y, z]

    def desenhar(self, program):
        r_x, r_y, r_z = self.rotation
        t_x, t_y, t_z = self.position
        s_x, s_y, s_z = self.scale

        mat_model = utils.model(r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
        loc_model = glGetUniformLocation(program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)

        loc_usar_textura = glGetUniformLocation(program, "usarTextura")
        loc_color = glGetUniformLocation(program, "color")

        for mat_info in self.materiais: # Renomeado 'mat' para 'mat_info' para clareza
            if mat_info['texture_id'] is not None and self.cor is None:
                glUniform1i(loc_usar_textura, GL_TRUE)
                glBindTexture(GL_TEXTURE_2D, mat_info['texture_id'])
            else:
                glUniform1i(loc_usar_textura, GL_FALSE)
                if self.cor:
                    glUniform4f(loc_color, *self.cor, 1.0)
                else:
                    # Cor branca padrão se não houver textura e nem cor do objeto definida
                    glUniform4f(loc_color, 1.0, 1.0, 1.0, 1.0) 

            # CORREÇÃO IMPORTANTE AQUI:
            # As chaves retornadas por load_obj_and_texture são 'vertice_inicial' e 'num_vertices'
            glDrawArrays(GL_TRIANGLES, mat_info['vertice_inicial'], mat_info['num_vertices'])
    # def desenhar(self, program):
    #     # Obtém valores de transformação
    #     r_x, r_y, r_z = self.rotation
    #     t_x, t_y, t_z = self.position
    #     s_x, s_y, s_z = self.scale
        
    #     # Aplica transformações
    #     mat_model = utils.model(r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    #     loc_model = glGetUniformLocation(program, "model")
    #     glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
        
    #     # Configura o uso de textura ou cor sólida
    #     loc_usar_textura = glGetUniformLocation(program, "usarTextura")
        
    #     if self.texture_id is not None and self.cor is None:
    #         # Usa textura
    #         glUniform1i(loc_usar_textura, GL_TRUE)  # Habilita textura no shader
    #         glBindTexture(GL_TEXTURE_2D, self.texture_id)
    #     else:
    #         # Usa cor sólida
    #         loc_color = glGetUniformLocation(program, "color")
    #         glUniform1i(loc_usar_textura, GL_FALSE)  # Desabilita textura no shader
    #         glUniform4f(loc_color, *self.cor, 1.0)
            
    #     # Desenha o objeto
    #     glDrawArrays(GL_TRIANGLES, self.verticeInicial, self.quantosVertices)

# objetos.py (continuação)

class Cama(Object3D):
    def __init__(self):
        super().__init__(
            obj_file='objetos/cama/cama.obj',
            textures_map={'Wood': 'objetos/cama/Wood_D.jpg', 'Fabric_Plain.001': 'objetos/cama/Fabric_D.jpg', 'Fabric': 'objetos/cama/Fabric_D.jpg', 'Material.002': 'objetos/cama/Lamp.png', "Material.003": 'objetos/cama/Fabric_D.jpg', 'Material.005': 'objetos/cama/Wood_D.jpg'} # Exemplo: assumindo que cama.obj usa 'default' ou não especifica material
        )
        self.limites_casa = {
            'min_x': -9.0, 'max_x': 3.5,
            'min_z': -6.0, 'max_z': 6.5,
            'min_y': -1.0, 'max_y': 4.0
        }
        self.dimensoes_cama = {
            'largura': 2.0, 'altura': 1.0, 'comprimento': 3.0
        }
    
    def set_position(self, x, y, z):
        meia_largura = self.dimensoes_cama['largura'] / 2
        meio_comprimento = self.dimensoes_cama['comprimento'] / 2
        limited_x = max(self.limites_casa['min_x'] + meia_largura, 
                        min(self.limites_casa['max_x'] - meia_largura, x))
        limited_y = max(self.limites_casa['min_y'], 
                        min(self.limites_casa['max_y'], y))
        limited_z = max(self.limites_casa['min_z'] + meio_comprimento, 
                        min(self.limites_casa['max_z'] - meio_comprimento, z))
        self.position = [limited_x, limited_y, limited_z]
        return x != limited_x or z != limited_z

class Relogio(Object3D):
    def __init__(self):
        super().__init__(
            obj_file='objetos/relogio/relogio2.obj', 
            textures_map={'clock_texture': 'objetos/relogio/relogio2.png'} # Ajuste a chave do material se necessário
        )

class Mesa(Object3D):
    def __init__(self):
        super().__init__(
            obj_file='objetos/mesa/mesa.obj', 
            textures_map={'default': 'objetos/mesa/Wood1_Albedo.png'} # Ajuste a chave do material se necessário
        )

class Banco(Object3D):
    def __init__(self):
        super().__init__(
            obj_file='objetos/banco/bench.obj', 
            textures_map={'default': 'objetos/banco/benchs_diffuse.jpg'} # Ajuste a chave do material se necessário
        )

class Chao(Object3D):
    def __init__(self):
        super().__init__(
            obj_file='objetos/chao/chao.obj', 
            textures_map={'None': 'objetos/chao/grama2.jpg'},
            # cor=[0.2, 0.7, 0.15]
            # textures_map={'None': 'objetos/chao/grama.jpg'} # Ajuste a chave do material se necessário
        )

class Placa(Object3D):
    def __init__(self):
        super().__init__(
            obj_file='objetos/placa/placa.obj', 
            textures_map={'13920_Wall_Street': 'objetos/placa/placa.jpg'} # Ajuste a chave do material se necessário
        )

class Skybox(Object3D):
    def __init__(self):
        super().__init__(
            obj_file='objetos/skybox/skybox.obj', 
            textures_map={}, # Skybox usa cor, então um mapa de texturas vazio
            cor=[0.0667, 0.9294, 0.9098]
        )

class Casa(Object3D): # Classe que causou o erro
    def __init__(self):
        super().__init__(
            obj_file='objetos/casa/casa.obj', 
            # Como o log mostrou "Material default", usamos 'default' como chave
            textures_map={'default': 'objetos/casa/Diffuse.png'} 
        )

class Bicicleta(Object3D):
    def __init__(self):
        super().__init__(
            obj_file='objetos/bicicleta/bicicleta.obj', 
            textures_map={'bicycle': 'objetos/bicicleta/bicicleta.jpg'} # Ajuste a chave do material se necessário
        )