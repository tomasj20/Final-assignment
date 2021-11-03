import OpenGL.error
import OpenGL.GLU
import OpenGL.GL

import sys

from Base3DObjects import *

class Shader3D:
    def __init__(self):
        vert_shader = glCreateShader(GL_VERTEX_SHADER)
        shader_file = open(sys.path[0] + "/simple3D.vert")
        glShaderSource(vert_shader, shader_file.read())
        shader_file.close()
        glCompileShader(vert_shader)
        result = glGetShaderiv(vert_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile vertex shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(vert_shader)))

        frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        shader_file = open(sys.path[0] + "/simple3D.frag")
        glShaderSource(frag_shader,shader_file.read())
        shader_file.close()
        glCompileShader(frag_shader)
        result = glGetShaderiv(frag_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile fragment shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(frag_shader)))

        self.renderingProgramID = glCreateProgram()
        glAttachShader(self.renderingProgramID, vert_shader)
        glAttachShader(self.renderingProgramID, frag_shader)
        glLinkProgram(self.renderingProgramID)

        self.positionLoc			= glGetAttribLocation(self.renderingProgramID, "a_position")
        glEnableVertexAttribArray(self.positionLoc)

        self.normalLoc = glGetAttribLocation(self.renderingProgramID, "a_normal")
        glEnableVertexAttribArray(self.normalLoc)

        self.eyePosition = glGetUniformLocation(self.renderingProgramID, "u_eye_position")

        self.modelMatrixLoc			= glGetUniformLocation(self.renderingProgramID, "u_model_matrix")
        self.viewMatrixLoc			= glGetUniformLocation(self.renderingProgramID, "u_view_matrix")
        self.projectionMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_projection_matrix")

        self.normalLightDirection = glGetUniformLocation(self.renderingProgramID, "u_normal_light_direction")
        self.normalLightColor     = glGetUniformLocation(self.renderingProgramID, "u_normal_light_color")
        self.otherLightDirection = glGetUniformLocation(self.renderingProgramID, "u_other_light_direction")

        self.lightPosition = glGetUniformLocation(self.renderingProgramID, "u_light_position")
        self.lightColor = glGetUniformLocation(self.renderingProgramID, "u_light_color")
        self.lightDirection = glGetUniformLocation(self.renderingProgramID, "u_light_direction")
        self.lightCutoff       = glGetUniformLocation(self.renderingProgramID, "u_light_cutoff")
        self.lightConst  = glGetUniformLocation(self.renderingProgramID, "u_light_constant")
        self.lightLinear    = glGetUniformLocation(self.renderingProgramID, "u_light_linear")
        self.lightQuad = glGetUniformLocation(self.renderingProgramID, "u_light_quad")
        self.lightOuterCutoff  = glGetUniformLocation(self.renderingProgramID, "u_light_outer_cutoff")

        self.materialDiffuseLoc  = glGetUniformLocation(self.renderingProgramID, "u_mat_diffuse")
        self.materialSpecularLoc = glGetUniformLocation(self.renderingProgramID, "u_mat_specular")
        self.materialShinyLoc    = glGetUniformLocation(self.renderingProgramID, "u_mat_shiny")
        self.materialEmit        = glGetUniformLocation(self.renderingProgramID, "u_mat_emit")

        self.textureLoc = glGetAttribLocation(self.renderingProgramID, "a_uv")
        glEnableVertexAttribArray(self.textureLoc)

        self.useTexture = glGetUniformLocation(self.renderingProgramID, "u_use_texture")
        self.diffuse_texture = glGetUniformLocation(self.renderingProgramID, "u_tex_diffuse")
        self.specular_texture = glGetUniformLocation(self.renderingProgramID, "u_tex_specular")

        #self.colorLoc = glGetUniformLocation(self.renderingProgramID, "u_color")


    def use(self):
        try:
            glUseProgram(self.renderingProgramID)   
        except OpenGL.error.Error:
            print(glGetProgramInfoLog(self.renderingProgramID))
            raise



    def set_specular_texture(self, i):
        glUniform1i(self.specular_texture, i)

    def set_diffuse_texture(self, i):
        glUniform1i(self.diffuse_texture, i)

    def set_model_matrix(self, matrix_array):
        glUniformMatrix4fv(self.modelMatrixLoc, 1, True, matrix_array)

    def set_view_matrix(self, matrix_array):
        glUniformMatrix4fv(self.viewMatrixLoc, 1, True, matrix_array)

    def set_projection_matrix(self, matrix_array):
        glUniformMatrix4fv(self.projectionMatrixLoc, 1, True, matrix_array)


    def set_position_attribute(self, vertex_array):
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 0, vertex_array)

    def set_normal_attribute(self, vertex_array):
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 0, vertex_array)

    def set_texture_attribute(self, vertex_array):
        glVertexAttribPointer(self.textureLoc, 2, GL_FLOAT, False, 0, vertex_array)

    def set_eye_position(self, pos):
        glUniform4f(self.eyePosition, pos.x, pos.y, pos.z, 1.0)

    def set_normal_light_direction(self, pos):
        glUniform4f(self.normalLightDirection, pos.x, pos.y, pos.z, 1.0)

    def set_other_light_direction(self, pos):
        glUniform4f(self.otherLightDirection, pos.x, pos.y, pos.z, 1.0)

    def set_normal_light_color(self, rgb):
        glUniform4f(self.normalLightColor, rgb.r, rgb.g, rgb.b, 1.0)



    def set_material_shiny(self, s):
        glUniform1f(self.materialShinyLoc, s)

    def set_material_emit(self, e):
        glUniform1f(self.materialEmit, e)

    def set_use_texture(self, f):
        glUniform1f(self.useTexture, f)

    def set_attribute_buffers(self, vertex_buffer_id):
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(0))
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(3 * sizeof(GLfloat)))
        glVertexAttribPointer(self.textureLoc, 2, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(6 * sizeof(GLfloat)))


    def set_material_diffuse(self, color, alpha=1.0):
        glUniform4f(self.materialDiffuseLoc, color.r, color.g, color.b, alpha)

    def set_material_specular(self, color):
        glUniform4f(self.materialSpecularLoc, color.r, color.g, color.b, 1.0)


class SpriteShader:
    def __init__(self):
        vert_shader = glCreateShader(GL_VERTEX_SHADER)
        shader_file = open(sys.path[0] + "/sprite_shader.vert")
        glShaderSource(vert_shader, shader_file.read())
        shader_file.close()
        glCompileShader(vert_shader)
        result = glGetShaderiv(vert_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile vertex shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(vert_shader)))

        frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        shader_file = open(sys.path[0] + "/sprite_shader.frag")
        glShaderSource(frag_shader,shader_file.read())
        shader_file.close()
        glCompileShader(frag_shader)
        result = glGetShaderiv(frag_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile fragment shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(frag_shader)))

        self.renderingProgramID = glCreateProgram()
        glAttachShader(self.renderingProgramID, vert_shader)
        glAttachShader(self.renderingProgramID, frag_shader)
        glLinkProgram(self.renderingProgramID)

        self.positionLoc			= glGetAttribLocation(self.renderingProgramID, "a_position")
        glEnableVertexAttribArray(self.positionLoc)

        self.modelMatrixLoc			= glGetUniformLocation(self.renderingProgramID, "u_model_matrix")
        self.viewMatrixLoc			= glGetUniformLocation(self.renderingProgramID, "u_view_matrix")
        self.projectionMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_projection_matrix")


        self.textureLoc = glGetAttribLocation(self.renderingProgramID, "a_uv")
        glEnableVertexAttribArray(self.textureLoc)

        self.usingAlphaTextureLoc = glGetUniformLocation(self.renderingProgramID, "u_using_alpha_texture")

        self.opacityLoc = glGetUniformLocation(self.renderingProgramID, "u_opacity")
        self.diffuse_texture = glGetUniformLocation(self.renderingProgramID, "u_tex_diffuse")
        self.alphaTextureLoc = glGetUniformLocation(self.renderingProgramID, "u_tex_specular")




    def use(self):
        try:
            glUseProgram(self.renderingProgramID)
        except OpenGL.error.Error:
            print(glGetProgramInfoLog(self.renderingProgramID))
            raise

    def set_diffuse_texture(self, i):
        glUniform1i(self.diffuse_texture, i)

    def set_opacity(self, i):
        glUniform1f(self.opacityLoc, i)

    def set_model_matrix(self, matrix_array):
        glUniformMatrix4fv(self.modelMatrixLoc, 1, True, matrix_array)

    def set_view_matrix(self, matrix_array):
        glUniformMatrix4fv(self.viewMatrixLoc, 1, True, matrix_array)

    def set_projection_matrix(self, matrix_array):
        glUniformMatrix4fv(self.projectionMatrixLoc, 1, True, matrix_array)

    def set_alpha_texture(self, f):
        if f is None:
            glUniform1f(self.usingAlphaTextureLoc, 0.0)
        else:
            glUniform1f(self.usingAlphaTextureLoc, 1.0)
            glUniform1i(self.alphaTextureLoc, f)

    def set_attribute_buffers(self, vertex_buffer_id):
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 5 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(0))
        glVertexAttribPointer(self.textureLoc, 2, GL_FLOAT, False, 5 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(3 * sizeof(GLfloat)))


