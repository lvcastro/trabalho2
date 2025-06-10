from OpenGL.GL import *
from PIL import Image
import core.utils as utils

def load_model_from_file(filename):
    """Loads a Wavefront OBJ file. """
    vertices = []
    texture_coords = []
    normals = [] # <<< NOVO: Lista para as normais
    faces = []

    material = None

    for line in open(filename, "r"):
        if line.startswith('#'): continue
        values = line.split()
        if not values: continue

        if values[0] == 'v':
            vertices.append(values[1:4])
        elif values[0] == 'vt':
            texture_coords.append(values[1:3])
        elif values[0] == 'vn': # <<< NOVO: Lendo as normais
            normals.append(values[1:4])
        elif values[0] in ('usemtl', 'usemat'):
            material = values[1]
        elif values[0] == 'f':
            face = []
            face_texture = []
            face_normal = [] # <<< NOVO: Lista para os índices de normal
            for v in values[1:]:
                w = v.split('/')
                face.append(int(w[0]))
                if len(w) >= 2 and len(w[1]) > 0:
                    face_texture.append(int(w[1]))
                else:
                    face_texture.append(0)
                if len(w) >= 3 and len(w[2]) > 0: # <<< NOVO: Lendo o índice da normal
                    face_normal.append(int(w[2]))
                else:
                    face_normal.append(0)
            faces.append((face, face_texture, face_normal, material)) # <<< NOVO: Adiciona normais à face

    model = {}
    model['vertices'] = vertices
    model['texture'] = texture_coords
    model['normals'] = normals # <<< NOVO
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
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
    return texture_id

def load_obj_and_texture(objFile, material_to_texture, vertices_list, textures_coord_list, normals_list):
    modelo = load_model_from_file(objFile)
    
    print(f'Processando modelo {objFile}.')

    objetos_por_material = {}
    
    # Agrupar faces por material
    for face in modelo['faces']:
        mat = face[3] or "default"
        if mat not in objetos_por_material:
            objetos_por_material[mat] = []
        objetos_por_material[mat].append(face)
    
    resultados = []

    if "chao" in objFile.lower():
        REPETICAO_UV = 4.0  # ou outro valor proporcional ao seu scale
    else:
        REPETICAO_UV = 1.0  # objetos normais continuam com UVs normais

    for material, faces in objetos_por_material.items():
        vertice_inicial = len(vertices_list)
        
        for face in faces:
            # face[0] -> índices de vértice
            # face[1] -> índices de textura
            # face[2] -> índices de normal

            # Processa vértices
            for vertice_id in utils.circular_sliding_window_of_three(face[0]):
                vertices_list.append(modelo['vertices'][vertice_id - 1])
            
            # Processa coordenadas de textura
            for texture_id in utils.circular_sliding_window_of_three(face[1]):
                # Verifica se o modelo['texture'] e o texture_id são válidos
                if modelo['texture'] and texture_id > 0 and texture_id <= len(modelo['texture']):
                    uv = modelo['texture'][texture_id - 1]
                    u = float(uv[0]) * REPETICAO_UV
                    v = float(uv[1]) * REPETICAO_UV
                    textures_coord_list.append([u, v])
                else:
                    # Adiciona uma coordenada de textura padrão se não houver
                    textures_coord_list.append([0.0, 0.0])

            for normal_id in utils.circular_sliding_window_of_three(face[2]):
                # Verifica se o modelo['normals'] e o normal_id são válidos
                if modelo['normals'] and normal_id > 0 and normal_id <= len(modelo['normals']):
                    normals_list.append(modelo['normals'][normal_id - 1])
                else:
                    # Adiciona uma normal padrão se não houver (apontando para cima)
                    normals_list.append([0.0, 1.0, 0.0])
        
        vertice_final = len(vertices_list)
        num_vertices = vertice_final - vertice_inicial

        textura_path = material_to_texture.get(material)
        texture_id = load_texture_from_file(textura_path) if textura_path else None

        resultados.append({
            'material': material,
            'vertice_inicial': vertice_inicial,
            'num_vertices': num_vertices,
            'texture_id': texture_id
        })
    
    return resultados