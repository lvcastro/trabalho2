from OpenGL.GL import *
import loaders
from core import utils

class Object3D:
    def __init__(self, obj_file=None, texture_file=None):
        self.verticeInicial = 0
        self.quantosVertices = 0
        self.texture_id = None
        self.position = [0.0, 0.0, -20.0]  # posição padrão (x, y, z)
        self.rotation = [0.0, 0.0, 0.0, 1.0]  # ângulo, x, y, z
        self.scale = [1.0, 1.0, 1.0]  # escala x, y, z
        self.obj_file = obj_file
        self.texture_file = texture_file

    def carregar_objeto(self, vertices_list, textures_coord_list):
        self.verticeInicial, self.quantosVertices, self.texture_id = loaders.load_obj_and_texture(
            self.obj_file,
            [self.texture_file] if self.texture_file else [],
            vertices_list,
            textures_coord_list
        )
    
    def set_position(self, x, y, z):
            self.position = [x, y, z]
            
    def set_rotation(self, angle, x, y, z):
        self.rotation = [angle, x, y, z]

    def set_scale(self, x, y, z):
        self.scale = [x, y, z]

    def desenhar(self, program):
        # Obtém valores de transformação
        angle, r_x, r_y, r_z = self.rotation
        t_x, t_y, t_z = self.position
        s_x, s_y, s_z = self.scale
        
        # Aplica transformações
        mat_model = utils.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
        loc_model = glGetUniformLocation(program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
        
        # Usa a textura específica deste objeto
        if self.texture_id is not None:
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            
        # Desenha o objeto
        glDrawArrays(GL_TRIANGLES, self.verticeInicial, self.quantosVertices)

class Cama(Object3D):
    def __init__(self):
        super().__init__(
            obj_file='objetos/cama/cama.obj',
            texture_file='objetos/cama/Fabric_D.jpg'
        )

class Relogio(Object3D):
    def __init__(self):
        super().__init__(
            obj_file='objetos/relogio/relogio.obj', 
            texture_file='objetos/relogio/Texture_Diff.png'
        )