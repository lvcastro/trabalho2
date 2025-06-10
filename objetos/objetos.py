from OpenGL.GL import *
import loaders
from core import utils


# Classe base para qualquer objeto 3D carregado de um arquivo .obj
class Object3D:
    def __init__(self, obj_file=None, textures_map=None, cor=None, material_specular=None, material_shininess=None):
        # Lista de dicionários com materiais carregados do modelo
        self.materiais = []  # Cada item: {'material': str, 'vertice_inicial': int, 'num_vertices': int, 'texture_id': int}
        
        # Transformações básicas
        self.position = [0.0, 0.0, -20.0]
        self.rotation = [0.0, 0.0, 0.0]
        self.scale = [1.0, 1.0, 1.0]

        # Arquivo .obj associado ao objeto
        self.obj_file = obj_file

        # Dicionário que mapeia nomes de materiais para caminhos de texturas
        self.textures_map = textures_map if textures_map is not None else {}

        # Cor difusa, usada caso o material não tenha textura
        self.cor = cor if cor is not None else [1.0, 1, 1]

        # Parâmetros de iluminação especular
        self.material_specular = material_specular if material_specular is not None else [0.5, 0.5, 0.5]
        self.material_shininess = material_shininess if material_shininess is not None else 32.0

    # Carrega o modelo .obj e suas texturas associadas
    def carregar_objeto(self, vertices_list, textures_coord_list, normals_list):
        self.materiais = loaders.load_obj_and_texture(
            self.obj_file,
            self.textures_map,
            vertices_list,
            textures_coord_list,
            normals_list
        )
    
    # Métodos de transformação
    def set_position(self, x, y, z):
        self.position = [x, y, z]
            
    def set_rotation(self, x, y, z):
        self.rotation = [x, y, z]

    def set_scale(self, x, y, z):
        self.scale = [x, y, z]

    # Desenha o objeto na tela com base no shader atual
    def desenhar(self, program):
        r_x, r_y, r_z = self.rotation
        t_x, t_y, t_z = self.position
        s_x, s_y, s_z = self.scale

        # Aplica transformação de modelagem
        mat_model = utils.model(r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
        loc_model = glGetUniformLocation(program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)

        # Envia parâmetros de material ao shader
        loc_use_diffuse = glGetUniformLocation(program, "material.useDiffuseMap")
        glUniform3fv(glGetUniformLocation(program, "material.solidSpecular"), 1, self.material_specular)
        glUniform1f(glGetUniformLocation(program, "material.shininess"), self.material_shininess)

        # Para cada material associado ao objeto
        for mat_info in self.materiais:
            if mat_info['texture_id'] is not None:
                # Usa a textura associada
                glUniform1i(loc_use_diffuse, GL_TRUE)
                glBindTexture(GL_TEXTURE_2D, mat_info['texture_id'])
            else:
                # Usa a cor sólida caso não haja textura
                glUniform1i(loc_use_diffuse, 0)
                glUniform3fv(glGetUniformLocation(program, "material.solidDiffuse"), 1, self.cor)
                
            # Desenha os triângulos associados ao material
            glDrawArrays(GL_TRIANGLES, mat_info['vertice_inicial'], mat_info['num_vertices'])

# A partir daqui são subclasses de Object3D para diferentes modelos
# Cada uma define seu caminho .obj e o dicionário de texturas

class Cama(Object3D):
    def __init__(self):
        super().__init__(
            material_shininess=32.0,
            material_specular=[1.0, 1.0, 1.0],
            obj_file='objetos/cama/cama.obj',
            textures_map={'Wood': 'objetos/cama/Wood_D.jpg',
                          'Fabric_Plain.001': 'objetos/cama/Fabric_D.jpg',
                          'Fabric': 'objetos/cama/Fabric_D.jpg',
                          'Material.002': 'objetos/cama/Lamp.png',
                          'Material.003': 'objetos/cama/Fabric_D.jpg',
                          'Material.005': 'objetos/cama/Wood_D.jpg'}
        )
        # Limites da cabana para evitar que a cama atravesse paredes
        self.limites_casa = {'min_x': -9.0, 'max_x': 3.5, 'min_z': -6.0, 'max_z': 6.5, 'min_y': -1.0, 'max_y': 4.0}
        self.dimensoes_cama = {'largura': 2.0, 'altura': 1.0, 'comprimento': 3.0}

    # Sobrescreve a posição para respeitar os limites
    def set_position(self, x, y, z):
        meia_largura = self.dimensoes_cama['largura'] / 2
        meio_comprimento = self.dimensoes_cama['comprimento'] / 2
        limited_x = max(self.limites_casa['min_x'] + meia_largura, min(self.limites_casa['max_x'] - meia_largura, x))
        limited_y = max(self.limites_casa['min_y'], min(self.limites_casa['max_y'], y))
        limited_z = max(self.limites_casa['min_z'] + meio_comprimento, min(self.limites_casa['max_z'] - meio_comprimento, z))
        self.position = [limited_x, limited_y, limited_z]
        return x != limited_x or z != limited_z

class Relogio(Object3D):
    def __init__(self):
        super().__init__(
            material_shininess=32.0,
            material_specular=[1.0, 1.0, 1.0],
            obj_file='objetos/relogio/relogio2.obj', 
            textures_map={'clock_texture': 'objetos/relogio/relogio2.png'}
        )

class Mesa(Object3D):
    def __init__(self):
        super().__init__(
            material_shininess=32.0,
            material_specular=[1.0, 1.0, 1.0],
            obj_file='objetos/mesa/mesa.obj', 
            textures_map={'default': 'objetos/mesa/Wood1_Albedo.png'}
        )

class Banco(Object3D):
    def __init__(self):
        super().__init__(
            material_shininess=32.0,
            material_specular=[1.0, 1.0, 1.0],
            obj_file='objetos/banco/bench.obj', 
            textures_map={'default': 'objetos/banco/benchs_diffuse.jpg'}
        )

class Chao(Object3D):
    def __init__(self):
        super().__init__(
            material_shininess=32.0,
            material_specular=[1.0, 1.0, 1.0],
            obj_file='objetos/chao/chao.obj', 
            textures_map={'None': 'objetos/chao/grama2.jpg'}
        )

class Placa(Object3D):
    def __init__(self):
        super().__init__(
            material_shininess=32.0,
            material_specular=[1.0, 1.0, 1.0],
            obj_file='objetos/placa/placa.obj', 
            textures_map={'13920_Wall_Street': 'objetos/placa/placa.jpg'}
        )

class Casa(Object3D):
    def __init__(self):
        super().__init__(
            material_shininess=32.0,
            material_specular=[1.0, 1.0, 1.0],
            obj_file='objetos/casa/casa.obj', 
            textures_map={'default': 'objetos/casa/Diffuse.png'} 
        )

class Bicicleta(Object3D):
    def __init__(self):
        super().__init__(
            material_shininess=32.0,
            material_specular=[1.0, 1.0, 1.0],
            obj_file='objetos/bicicleta/bicicleta.obj', 
            textures_map={'bicycle': 'objetos/bicicleta/bicicleta.jpg'}
        )

class Celular(Object3D):
    def __init__(self):
        super().__init__(
            material_shininess=32.0,
            material_specular=[1.0, 1.0, 1.0],
            obj_file='objetos/celular/cel.obj',
            textures_map={'Material__0': 'objetos/celular/cel.jpg'}
        )

class Ventilador(Object3D):
    def __init__(self):
        super().__init__(
            material_shininess=32.0,
            material_specular=[1.0, 1.0, 1.0],
            obj_file='objetos/ventilador/ventilador.obj',
            textures_map={'ceiling_fan': 'objetos/ventilador/ceiling_fan_BaseColor.png'}
        )

class Carro(Object3D):
    def __init__(self):
        super().__init__(
            material_shininess=32.0,
            material_specular=[1.0, 1.0, 1.0],
            obj_file='objetos/carro/carro.obj',
            textures_map={'goma':'objetos/texturas/pneu.jpg',
                        'vidre__pla':'objetos/texturas/vidro.jpg',
                        'cromat':'objetos/texturas/metal.jpg',
                        'vidre_tronja':'objetos/texturas/vidro.jpg',
                        'matricula':'objetos/texturas/metal.jpg',
                        'vidre_vermell':'objetos/texturas/madeira.jpg',
                        'textil_seients':'objetos/texturas/metal.jpg',
                        'Material.002:':'objetos/texturas/madeira.jpg',
                        'vidre_':'objetos/texturas/metal.jpg',
                        'metall':'objetos/texturas/metal_vermelho.jpg',
                        'M_Bulb': 'objetos/texturas/metal.jpg'}
        )