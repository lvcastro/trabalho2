import glm
import glfw
import numpy as np

class Camera:
    def __init__(self, largura, altura):
        self.cameraPos   = glm.vec3(6.0, 4.5, 0.0)
        # self.cameraFront = glm.vec3(-0.95, -0.3, 0.0) # tanto faz o valor aqui, já que ele vai ser alterado depois a partir da posição do mouse na cena.
        self.cameraUp    = glm.vec3(0.0, 1.0, 0.0)
        self.malha = False

        self.firstMouse = True
        self.yaw   = -180.0	# yaw is initialized to -90.0 degrees since a yaw of 0.0 results in a direction vector pointing to the right so we initially rotate a bit to the left.
        self.pitch =  -20.0
        self.lastX =  largura / 2.0
        self.lastY =  altura / 2.0
        self.fov   =  45.0

        # Calcular o cameraFront inicial com base nos valores iniciais de yaw e pitch
        front = glm.vec3()
        front.x = glm.cos(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        front.y = glm.sin(glm.radians(self.pitch))
        front.z = glm.sin(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        self.cameraFront = glm.normalize(front)

        # timing
        self.deltaTime = 0.0	# time between current frame and last frame
        self.lastFrame = 0.0

    def key_event(self, window,key,scancode,action,mods):
        # global cameraPos, cameraFront, cameraUp

        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)
        
        cameraSpeed = 25 * self.deltaTime
        if key == glfw.KEY_W and (action == glfw.PRESS or action == glfw.REPEAT):
            self.cameraPos += cameraSpeed * self.cameraFront
        
        if key == glfw.KEY_S and (action == glfw.PRESS or action == glfw.REPEAT):
            self.cameraPos -= cameraSpeed * self.cameraFront
        
        if key == glfw.KEY_A and (action == glfw.PRESS or action == glfw.REPEAT):
            self.cameraPos -= glm.normalize(glm.cross(self.cameraFront, self.cameraUp)) * cameraSpeed
            
        if key == glfw.KEY_D and (action == glfw.PRESS or action == glfw.REPEAT):
            self.cameraPos += glm.normalize(glm.cross(self.cameraFront, self.cameraUp)) * cameraSpeed

        # Alterna modo de visualização da malha com a tecla P
        if key == glfw.KEY_P and action == glfw.PRESS:
            self.malha = not self.malha

        self.cameraPos.x = max(-50.0, min(50.0, self.cameraPos.x))
        self.cameraPos.z = max(-50.0, min(50.0, self.cameraPos.z))
        self.cameraPos.y = max(-1.0, min(50.0, self.cameraPos.y))  # evita que entre no chão

    # glfw: whenever the mouse moves, this callback is called
    # -------------------------------------------------------
    def mouse_callback(self, window, xpos, ypos):
        # global cameraFront, lastX, lastY, firstMouse, yaw, pitch
    
        if (self.firstMouse):
            self.lastX = xpos
            self.lastY = ypos
            self.firstMouse = False
            return

        xoffset = xpos - self.lastX
        yoffset = self.lastY - ypos # reversed since y-coordinates go from bottom to top
        self.lastX = xpos
        self.lastY = ypos

        sensitivity = 0.1 # change this value to your liking
        xoffset *= sensitivity
        yoffset *= sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        # make sure that when pitch is out of bounds, screen doesn't get flipped
        if (self.pitch > 89.0):
            self.pitch = 89.0
        if (self.pitch < -89.0):
            self.pitch = -89.0

        front = glm.vec3()
        front.x = glm.cos(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        front.y = glm.sin(glm.radians(self.pitch))
        front.z = glm.sin(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        self.cameraFront = glm.normalize(front)

    # glfw: whenever the mouse scroll wheel scrolls, this callback is called
    # ----------------------------------------------------------------------
    def scroll_callback(self, window, xoffset, yoffset):
        # global fov

        self.fov -= yoffset
        if (self.fov < 1.0):
            self.fov = 1.0
        if (self.fov > 45.0):
            self.fov = 45.0

    def view(self):
        mat_view = glm.lookAt(self.cameraPos, self.cameraPos + self.cameraFront, self.cameraUp);
        mat_view = np.array(mat_view)
        return mat_view

    def projection(self, largura, altura):
        # perspective parameters: fovy, aspect, near, far
        mat_projection = glm.perspective(glm.radians(self.fov), largura/altura, 0.1, 100.0)
        mat_projection = np.array(mat_projection)
        return mat_projection