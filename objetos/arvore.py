from OpenGL.GL import *
import loaders
import core.utils as utils

class Arvore:
    def __init__(self):
        self.verticeInicial = 0
        self.quantosVertices = 0

    def carregar_arvore(self, vertices_list, textures_coord_list):
        self.verticeInicial, self.quantosVertices = loaders.load_obj_and_texture(
            'objetos/arvore/arvore.obj',
            [
                'objetos/arvore/Leaves0120_35_S.png'
            ],
            vertices_list,
            textures_coord_list
        )

    def desenha_arvore(self, program):        
        # rotacao
        angle = 0.0;
        r_x = 0.0; r_y = 0.0; r_z = 1.0;
        
        # translacao
        t_x = 0.0; t_y = 0.0; t_z = -20.0;
        
        # escala
        s_x = 1.0; s_y = 1.0; s_z = 1.0;
        
        mat_model = utils.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
        loc_model = glGetUniformLocation(program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
        
        glBindTexture(GL_TEXTURE_2D, 0)
        # desenha o cama
        glDrawArrays(GL_TRIANGLES, self.verticeInicial, self.quantosVertices) ## renderizando