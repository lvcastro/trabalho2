from OpenGL.GL import *
from PIL import Image
import core.utils as utils

def load_model_from_file(filename):
    """Loads a Wavefront OBJ file. """
    objects = {}
    vertices = []
    texture_coords = []
    faces = []

    material = None

    # abre o arquivo obj para leitura
    for line in open(filename, "r"): ## para cada linha do arquivo .obj
        if line.startswith('#'): continue ## ignora comentarios
        values = line.split() # quebra a linha por espaço
        if not values: continue

        ### recuperando vertices
        if values[0] == 'v':
            vertices.append(values[1:4])

        ### recuperando coordenadas de textura
        elif values[0] == 'vt':
            texture_coords.append(values[1:3])

        ### recuperando faces 
        elif values[0] in ('usemtl', 'usemat'):
            material = values[1]
        elif values[0] == 'f':
            face = []
            face_texture = []
            for v in values[1:]:
                w = v.split('/')
                face.append(int(w[0]))
                if len(w) >= 2 and len(w[1]) > 0:
                    face_texture.append(int(w[1]))
                else:
                    face_texture.append(0)

            faces.append((face, face_texture, material))

    model = {}
    model['vertices'] = vertices
    model['texture'] = texture_coords
    model['faces'] = faces

    return model

def load_texture_from_file(img_textura):
    texture_id = glGenTextures(1)  # Gera um ID único para a textura
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    img = Image.open(img_textura)
    img_width = img.size[0]
    img_height = img.size[1]
    image_data = img.tobytes("raw", "RGB", 0, -1)
    #image_data = np.array(list(img.getdata()), np.uint8)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
    # print("TEXTURE ID: ",texture_id)
    return texture_id

def load_obj_and_texture(objFile, material_to_texture, vertices_list, textures_coord_list):
    modelo = load_model_from_file(objFile)
    
    print(f'Processando modelo {objFile}.')

    objetos_por_material = {}
    
    # Agrupar faces por material
    for face in modelo['faces']:
        mat = face[2] or "default"
        if mat not in objetos_por_material:
            objetos_por_material[mat] = []
        objetos_por_material[mat].append(face)
    
    resultados = []

    for material, faces in objetos_por_material.items():
        vertice_inicial = len(vertices_list)
        # print(f'Material {material}, vértice inicial: {vertice_inicial}')
        
        for face in faces:
            for vertice_id in utils.circular_sliding_window_of_three(face[0]):
                vertices_list.append(modelo['vertices'][vertice_id - 1])
            for texture_id in utils.circular_sliding_window_of_three(face[1]):
                uv = modelo['texture'][texture_id - 1]
                u = float(uv[0])
                v = float(uv[1])
                textures_coord_list.append([u, v])
        
        vertice_final = len(vertices_list)
        num_vertices = vertice_final - vertice_inicial

        # carrega a textura associada ao material
        textura_path = material_to_texture.get(material)
        texture_id = load_texture_from_file(textura_path) if textura_path else None

        resultados.append({
            'material': material,
            'vertice_inicial': vertice_inicial,
            'num_vertices': num_vertices,
            'texture_id': texture_id
        })
    
    return resultados  # lista de blocos por material