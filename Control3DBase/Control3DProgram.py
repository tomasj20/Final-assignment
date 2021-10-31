from OpenGL.GL import *
from OpenGL.GLUT import *
from math import *
import pygame
from pygame.locals import *
import sys
from objloader import *
from Base3DObjects import *
from Shaders import *
from Matrices import *
from Control3DBase import objloader

class GraphicsProgram3D:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)
        self.shader = Shader3D()
        self.shader.use()
        self.lvl = 1
        self.model_matrix = ModelMatrix()
        self.view_matrix = ViewMatrix()
        self.view_matrix.look(Point(7, 1, 5), Point(7, 1.0, 0.0), Vector(0, 1, 0))
        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        self.shooting = False
        """Sounds"""
        #self.crash_sound = pygame.mixer.Sound("sounds/scream.wav")
        #self.lvlup_sound = pygame.mixer.Sound("sounds/lvlcomplete.wav")
        #self.flashlight_click = pygame.mixer.Sound("sounds/flashlight.wav")
        #self.jumpscare = pygame.mixer.Sound("sounds/jumpscare.wav")


        self.flashlight_angle = 3*pi/2 #To calculate flashlight yaw
        self.player_angle = 0

        """Textures"""
        self.shader.set_diffuse_texture(0)
        self.tex_id_wall_diffuse = self.load_texture("./textures/window_texture.jpeg")
        self.shader.set_specular_texture(1)
        self.tex_id_wall_specular = self.load_texture("./textures/window_texture.jpeg")


        self.tex_id_flashlight_diffuse = self.load_texture("./textures/AR.jpg")
        self.tex_id_flashlight_specular = self.load_texture("./textures/AR.jpg")

        self.tex_id_building_diffuse = self.load_texture("./textures/building.jpg")
        self.tex_id_building_specular = self.load_texture("./textures/building.jpg")

        self.tex_id_building2_diffuse = self.load_texture("./textures/building2.jpg")
        self.tex_id_building2_specular = self.load_texture("./textures/building2.jpg")

        self.tex_id_floorandceiling = self.load_texture("./textures/road.jpg")
        self.tex_id_floorandceiling_specular = self.load_texture("./textures/road.jpg")

        self.tex_id_brick_diff = self.load_texture("./textures/trainwall.jpg")
        self.tex_id_brick_spec = self.load_texture("./textures/trainwall.jpg")

        self.tex_id_sirene_diff = self.load_texture("./textures/sirene01.jpg")
        self.tex_id_sirene_spec = self.load_texture("./textures/sirene01.jpg")

        """Ignore the name this is the start  up screen"""
        self.tex_id_jumpscare_diffuse = self.load_texture("./textures/screen.png")
        self.tex_id_jumpscare_specular = self.load_texture("./textures/screen.png")

        self.tex_id_tunnel_diffuse = self.load_texture("./textures/tunnel2.jpg")
        self.tex_id_tunnel_specular = self.load_texture("./textures/tunnel2.jpg")

        self.tex_id_stop_diffuse = self.load_texture("./textures/stop.png")
        self.tex_id_stop_specular = self.load_texture("./textures/stop.png")

        self.tex_id_win_screen_diffuse = self.load_texture("./textures/winscreen.png")
        self.tex_id_win_screen_specular = self.load_texture("./textures/winscreen.png")

        self.tex_id_train_diffuse = self.load_texture("./textures/train.png")
        self.tex_id_train_specular = self.load_texture("./textures/train.png")

        self.tex_id_player_diffuse = self.load_texture("./textures/unwrap.jpg")
        self.tex_id_player_specular = self.load_texture("./textures/unwrap.jpg")

        self.tex_id_roadintersection_dif = self.load_texture("./textures/roadint.png")
        self.tex_id_roadintersection_spec = self.load_texture("./textures/roadint.png")

        self.tex_id_rail_dif = self.load_texture("./textures/rail.jpg")
        self.tex_id_rail_spec = self.load_texture("./textures/rail.jpg")

        self.tex_id_car_dif = self.load_texture("./textures/car.png")
        self.tex_id_car_spec = self.load_texture("./textures/car.png")

        self.tex_id_car1_dif = self.load_texture("./textures/car1.png")
        self.tex_id_car1_spec = self.load_texture("./textures/car1.png")

        self.tex_id_humvee_dif = self.load_texture("./textures/humvee.png")
        self.tex_id_humvee_spec = self.load_texture("./textures/humvee.png")

        self.tex_id_station_dif = self.load_texture("./textures/gas.png")
        self.tex_id_station_spec = self.load_texture("./textures/gas.png")


        self.projection_matrix = ProjectionMatrix()
        self.fov = pi / 2
        self.projection_matrix.set_perspective(pi / 2, 800/600, 0.5, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())
        self.cube = Cube()
        self.scale = Point(1, 1, 1)
        self.clock = pygame.time.Clock()

        """Obj models"""
        self.obj_model_flashlight = objloader.load_obj_file(sys.path[0] + '/objects/', 'gun.obj')
        #self.obj_model_player = objloader.load_obj_file(sys.path[0] + '/objects/', 'bomber.obj')
        self.obj_model_car = objloader.load_obj_file(sys.path[0] + '/objects/', 'car.obj')
        self.obj_model_car1 = objloader.load_obj_file(sys.path[0] + '/objects/', 'car1.obj')
        self.obj_model_train = objloader.load_obj_file(sys.path[0] + '/objects/', 'train.obj')
        #self.obj_model_humvee = objloader.load_obj_file(sys.path[0] + '/objects/', 'humvee.obj')
        self.obj_model_station = objloader.load_obj_file(sys.path[0] + '/objects/', 'station.obj')
        self.obj_model_stop = objloader.load_obj_file(sys.path[0] + '/objects/', 'stop.obj')

        #self.obj_model_building = objloader.load_obj_file(sys.path[0] + '/objects/', 'building.obj')


        """Walls: x, y, z positions, and x, y, z scale"""
        self.wall_list2 = [
            [11.1, 2.0, 1.5,2, 3, 7.5],
            [5.1, 2.0, 1.5, 2, 3, 7.5],
            [8.0232, 0.45, 4.1309, 0.8, 1.0, 1.0],
            [8.2, 0.45, 1.4405, 0.8, 1.0, 1.2],
            [6.1, 1.0, -3.5, 0.5, 2.0, 2.0],
            [6.1, 1.0, -7.0, 0.5, 2.0, 2.0],
            [14.9, 0.5, -6, 2.5, 0.4, 5.5],
            [5.85, 1.0, -3.25, 0.5, 2.0, 2.0],
            [5.85, 1.0, -7.3, 0.5, 2.0, 3.25],
            [4.85, 1.0, -9.0, 2.5, 2.0, 0.5],
            [0.5, 1.0, -3.25, 10.2, 2.0, 0.5],
            [-0.5, 1.0, -6.7, 8.2, 2.0, 0.5],
            [3.7, 1.0, -7.6, 0.5, 2.0, 2.3],
            [-4.6, 1.0, -4.975, 0.5, 2.0, 3.0]
        ]

        self.train_station = [
            [5.85, 1.0, -3.25, 0.5, 2.0, 2.0],
            [5.85, 1.0, -7.3, 0.5, 2.0, 3.25],
            [4.85, 1.0, -9.0, 2.5, 2.0, 0.5],
            [0.5, 1.0, -3.25, 10.2, 2.0, 0.5],
            [-0.5, 1.0, -6.7, 8.2, 2.0, 0.5],
            [3.7, 1.0, -7.6, 0.5, 2.0, 2.3],
        ]

        self.close_walls = []

        """A lot of stuff we need"""

        self.collisionLeftWall = False
        self.collisionRightWall = False
        self.collisionTopWall = False
        self.collisionBottomWall = False
        self.A_key_down = False
        self.D_key_down = False
        self.T_key_down = False
        self.G_key_down = False
        self.UP_key_down = False
        self.falling = False
        self.collison_check()
        self.SPACE_key_down = False
        self.p_key_down = False
        self.aiming = False
        self.won = False
        self.ENTER_key_down = True

    def get_walls_closest(self):
        if self.lvl == 1:
            for item in self.wall_list2:
                if item[0]-4.0 <= self.view_matrix.eye.x <= item[0]+4.0:
                    if item[2]-4.0 <= self.view_matrix.eye.z <= item[2]+4.0:
                        if item not in self.close_walls:
                            self.close_walls.append(item)
                            continue
                    else:
                        if item in self.close_walls:
                            self.close_walls.remove(item)

    def collison_check(self):
        if self.lvl == 1:
            for item in self.close_walls:
                wall_min_x = item[0] - item[3] / 2
                wall_max_x = item[0] + item[3] / 2
                wall_min_z = item[2] - item[5] / 2
                wall_max_z = item[2] + item[5] / 2
                if wall_max_x+0.2 >= self.view_matrix.eye.x >= wall_max_x+0.1:
                    if wall_min_z-0.1 <= self.view_matrix.eye.z <= wall_max_z+0.1:
                        self.collisionRightWall = True
                        return True
                else:
                    self.collisionRightWall = False

                if wall_min_x-0.2 <= self.view_matrix.eye.x <= wall_min_x-0.1:
                    if wall_min_z-0.2 <= self.view_matrix.eye.z <= wall_max_z+0.1:
                        self.collisionLeftWall = True
                        return True
                else:
                    self.collisionLeftWall = False

                if wall_min_z-0.2 <= self.view_matrix.eye.z <= wall_min_z-0.1:
                    if wall_min_x-0.1 <= self.view_matrix.eye.x <= wall_max_x+0.1:
                        self.collisionTopWall = True
                        return True
                else:
                    self.collisionTopWall = False

                if wall_max_z+0.2 >= self.view_matrix.eye.z >= wall_max_z+0.1:
                    if wall_min_x-0.1 <= self.view_matrix.eye.x <= wall_max_x+0.1:
                        self.collisionBottomWall = True
                        return True
                else:
                    self.collisionBottomWall = False


    def load_texture(self, image):
        """ Loads a texture into the buffer """
        texture_surface = pygame.image.load(image)
        texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
        width = texture_surface.get_width()
        height = texture_surface.get_height()

        texid = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, texid)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        return texid

    def update(self):
        delta_time = self.clock.tick() / 1000.0

        if self.A_key_down:
            self.view_matrix.yaw(-120*delta_time)
            self.flashlight_angle += -((2*pi)/3) * delta_time
            self.player_angle += -((2*pi)/3) * delta_time
        if self.D_key_down:
            self.view_matrix.yaw(120 * delta_time)
            self.flashlight_angle += ((2*pi)/3) * delta_time
            self.player_angle += ((2*pi)/3) * delta_time
        if self.T_key_down:
            self.fov -= 0.25 * delta_time
        if self.G_key_down:
            self.fov += 0.25 * delta_time
        if self.UP_key_down and not self.collisionLeftWall and not self.collisionRightWall and not self.collisionTopWall and not self.collisionBottomWall:
            self.view_matrix.slide(0, 0, -1.5 * delta_time)
        if self.SPACE_key_down:
            self.aiming = True
            self.fov -= self.fov - 0.75
        if not self.SPACE_key_down:
            self.aiming = False
            self.fov = pi/2
        if self.falling:
            pygame.mixer.Sound.play(self.crash_sound)
            self.view_matrix.eye.y -= 3 * delta_time
        """
        Check for direction of player and make him slide accordingly, we also check what part of the wall
        the player is hitting. If the player is looking away from the wall that he is colliding with he can walk freely
        this fixes the bug that the player can get stuck to the wall. The collisions are very smooth in our program.
        """
        if self.UP_key_down:
            """Right side of wall"""
            if self.collisionRightWall and self.view_matrix.n.z >= 0 and self.view_matrix.n.x >= 0:
                self.view_matrix.slide(1 * delta_time, 0, 0)

            if self.collisionRightWall and self.view_matrix.n.z >= 0 and self.view_matrix.n.x <= 0:
                self.view_matrix.slide(0, 0, -1 * delta_time)

            if self.collisionRightWall and self.view_matrix.n.z <= 0 and self.view_matrix.n.x >= 0:
                self.view_matrix.slide(-1 * delta_time, 0, 0)

            if self.collisionRightWall and self.view_matrix.n.z <= 0 and self.view_matrix.n.x <= 0:
                self.view_matrix.slide(0, 0, -1 * delta_time)

            """Left side of wall"""

            if self.collisionLeftWall and self.view_matrix.n.z <= 0 and self.view_matrix.n.x <= 0:
                self.view_matrix.slide(1 * delta_time, 0, 0)

            if self.collisionLeftWall and self.view_matrix.n.z <= 0 and self.view_matrix.n.x >= 0:
                self.view_matrix.slide(0, 0, -1 * delta_time)

            if self.collisionLeftWall and self.view_matrix.n.z >= 0 and self.view_matrix.n.x <= 0:
                self.view_matrix.slide(-1 * delta_time, 0, 0)

            if self.collisionLeftWall and self.view_matrix.n.z >= 0 and self.view_matrix.n.x >= 0:
                self.view_matrix.slide(0, 0, -1 * delta_time)

            """Bottom side of wall"""

            if self.collisionBottomWall and self.view_matrix.n.z >= 0 and self.view_matrix.n.x >= 0:
                self.view_matrix.slide(-1 * delta_time, 0, 0)

            if self.collisionBottomWall and self.view_matrix.n.z <= 0 and self.view_matrix.n.x >= 0:
                self.view_matrix.slide(0, 0, -1 * delta_time)

            if self.collisionBottomWall and self.view_matrix.n.z >= 0 and self.view_matrix.n.x <= 0:
                self.view_matrix.slide(1 * delta_time, 0, 0)

            if self.collisionBottomWall and self.view_matrix.n.z <= 0 and self.view_matrix.n.x <= 0:
                self.view_matrix.slide(0, 0, -1 * delta_time)

            """Top side of wall"""

            if self.collisionTopWall and self.view_matrix.n.z <= 0 and self.view_matrix.n.x >= 0:
                self.view_matrix.slide(1 * delta_time, 0, 0)

            if self.collisionTopWall and self.view_matrix.n.z >= 0 and self.view_matrix.n.x <= 0:
                self.view_matrix.slide(0, 0, -1 * delta_time)

            if self.collisionTopWall and self.view_matrix.n.z <= 0 and self.view_matrix.n.x <= 0:
                self.view_matrix.slide(-1 * delta_time, 0, 0)

            if self.collisionTopWall and self.view_matrix.n.z >= 0 and self.view_matrix.n.x >= 0:
                self.view_matrix.slide(0, 0, -1 * delta_time)

        """If player is falling, the game ends"""
        if self.view_matrix.eye.y <= -4:
            pygame.quit()
            quit()
            print("You died, don't walk away from the area")
            """Our functions must be called here in the update"""
        if self.SPACE_key_down:
            self.shooting_vector = self.view_matrix.n


        self.collison_check()
        self.get_walls_closest()

    def display(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_FRAMEBUFFER_SRGB)
        glShadeModel(GL_SMOOTH)
        glLoadIdentity()
        glMatrixMode(GL_PROJECTION)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glViewport(0, 0, 800, 600)

        self.projection_matrix.set_perspective(self.fov, 800 / 600, 0.01, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)

        """"LIGHTS"""
        self.shader.set_normal_light_direction(Point(1.5, 1, -2))
        self.shader.set_normal_light_color(Color(1.0, 1.0, 1.0))
        self.shader.set_other_light_direction(Point(-1.5, -1, -2))


        """
        This is almost exactly like the flashlight except we need to point the vector down on the player,
        so he get's a nice lantern like lighting around him
        """
        self.shader.set_light_direction(self.view_matrix.v)
        self.shader.set_light_color(Color(0.9725, 0.7647, 0.4667))
        self.shader.set_light_position(
        Point(self.view_matrix.eye.x, self.view_matrix.eye.y+0.7, self.view_matrix.eye.z))
        self.shader.set_light_cutoff(cos((40 + 6.5) * pi / 180))
        self.shader.set_light_outer_cutoff(cos((40 + 11.5) * pi / 180))
        self.shader.set_light_constant(1.0)
        self.shader.set_light_linear(0.14)
        self.shader.set_light_quad(0.07)

        """Drawing and some more drawing....."""

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_floorandceiling)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_floorandceiling_specular)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(8.1, 0.0, 1.0)
        self.model_matrix.add_scale(4.0, 1.0, 8.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()
        glDisable(GL_TEXTURE_2D)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_brick_diff)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_brick_spec)
        for item in self.train_station:
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(item[0], item[1], item[2])
            self.model_matrix.add_scale(item[3], item[4], item[5])
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.cube.draw()
            self.model_matrix.pop_matrix()
        glDisable(GL_TEXTURE_2D)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_roadintersection_dif)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_roadintersection_spec)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(7.9, 0.0, -5.0)
        self.model_matrix.add_scale(8.0, 1.0, 8.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()
        glDisable(GL_TEXTURE_2D)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_tunnel_diffuse)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_tunnel_specular)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(-5.0, 1.0, -4.975)
        self.model_matrix.add_scale(0.5, 2.0, 3.0)
        self.model_matrix.add_rotate_y(3*pi/2)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()
        glDisable(GL_TEXTURE_2D)



        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_rail_dif)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_rail_spec)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(1.0, 0.0, -5.0)
        self.model_matrix.add_scale(8.0, 1.0, 3.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()
        glDisable(GL_TEXTURE_2D)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_building_diffuse)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_building_specular)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(11.1, 2.0, 1.5)
        self.model_matrix.add_scale(2, 3, 7.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()
        glDisable(GL_TEXTURE_2D)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_building2_diffuse)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_building2_specular)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(5.1, 2.0, 1.5)
        self.model_matrix.add_scale(2, 3, 7.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()
        glDisable(GL_TEXTURE_2D)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_flashlight_diffuse)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_flashlight_specular)
        self.shader.set_material_diffuse(Color(0.7, 0.7, 0.7))
        self.shader.set_material_specular(Color(0.5, 0.5, 0.5))
        self.shader.set_material_shiny(10)
        self.shader.set_material_emit(0.0)
        self.model_matrix.push_matrix()
        if self.aiming == False:
            self.model_matrix.add_translation(self.view_matrix.eye.x+0.1, self.view_matrix.eye.y-0.3, self.view_matrix.eye.z)
        if self.aiming == True:
            self.model_matrix.add_translation(self.view_matrix.eye.x, self.view_matrix.eye.y-0.2, self.view_matrix.eye.z)
        self.model_matrix.add_rotate_y(-self.flashlight_angle)
        self.model_matrix.add_scale(0.1, 0.1, 0.15)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.obj_model_flashlight.draw(self.shader)
        self.model_matrix.pop_matrix()
        glDisable(GL_TEXTURE_2D)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_car_dif)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_car_spec)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(8.0, 0.55, 4.0)
        self.model_matrix.add_rotate_y(pi)
        self.model_matrix.add_scale(0.03, 0.07, 0.03)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.obj_model_car.draw(self.shader)
        self.model_matrix.pop_matrix()
        glDisable(GL_TEXTURE_2D)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_car1_dif)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_car1_spec)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(4.5, 0.45, 1.0)
        self.model_matrix.add_rotate_y(pi)
        self.model_matrix.add_scale(0.8, 1.0, 1.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.obj_model_car1.draw(self.shader)
        self.model_matrix.pop_matrix()
        glDisable(GL_TEXTURE_2D)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_train_diffuse)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_train_specular)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(0.5, 0.4, -5.0)
        self.model_matrix.add_rotate_y(pi/2)
        self.model_matrix.add_scale(0.3, 0.2, 0.1)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.obj_model_train.draw(self.shader)
        self.model_matrix.pop_matrix()
        glDisable(GL_TEXTURE_2D)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_stop_diffuse)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_stop_specular)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(3.0, 0.4, -3.9)
        self.model_matrix.add_rotate_y(pi / 2)
        self.model_matrix.add_scale(0.0017, 0.0017, 0.0017)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.obj_model_stop.draw(self.shader)
        self.model_matrix.pop_matrix()
        glDisable(GL_TEXTURE_2D)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_stop_diffuse)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_stop_specular)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(3.0, 0.4, -6.1)
        self.model_matrix.add_rotate_y(pi / 2)
        self.model_matrix.add_scale(0.0017, 0.0017, 0.0017)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.obj_model_stop.draw(self.shader)
        self.model_matrix.pop_matrix()
        glDisable(GL_TEXTURE_2D)

        """glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_humvee_dif)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_humvee_spec)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(11.0, 1.0, -7.2)
        self.model_matrix.add_rotate_y(3*pi/2)
        self.model_matrix.add_scale(0.35, 0.4, 0.3)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.obj_model_humvee.draw(self.shader)
        self.model_matrix.pop_matrix()
        glDisable(GL_TEXTURE_2D)"""

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_station_dif)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_station_spec)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(11.0, 0.5, -4.2)
        self.model_matrix.add_rotate_y(3*pi/2)
        self.model_matrix.add_scale(0.35, 0.4, 0.3)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.obj_model_station.draw(self.shader)
        self.model_matrix.pop_matrix()
        glDisable(GL_TEXTURE_2D)

        """glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_player_diffuse)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_player_specular)
        self.shader.set_material_diffuse(Color(0.7, 0.7, 0.7))
        self.shader.set_material_specular(Color(0.5, 0.5, 0.5))
        self.shader.set_material_shiny(10)
        self.shader.set_material_emit(0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(self.view_matrix.eye.x, self.view_matrix.eye.y-0.3, self.view_matrix.eye.z)
        self.model_matrix.add_rotate_y(-self.player_angle)
        self.model_matrix.add_scale(0.02, 0.025, 0.02)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.obj_model_player.draw(self.shader)
        self.model_matrix.pop_matrix()
        glDisable(GL_TEXTURE_2D)"""

        glDisable(GL_BLEND)
        pygame.display.flip()


    def program_loop(self):
        exiting = False
        while not exiting:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting!")
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        print("Escaping!")
                        exiting = True

                    if event.key == K_w:
                        self.UP_key_down = True

                    if event.key == K_DOWN:
                        self.DOWN_key_down = True

                    if event.key == K_a:
                        self.A_key_down = True

                    if event.key == K_d:
                        self.D_key_down = True

                    if event.key == K_t:
                        self.T_key_down = True

                    if event.key == K_g:
                        self.G_key_down = True

                    if event.key == K_SPACE:
                        self.SPACE_key_down = True

                    if event.key == K_RETURN:
                        self.shooting = True

                    if event.key == K_p and self.won:
                        self.p_key_down = True

                    if event.key == K_q:
                        pygame.quit()
                        quit()

                elif event.type == pygame.KEYUP:
                    if event.key == K_w:
                        self.UP_key_down = False

                    if event.key == K_DOWN:
                        self.DOWN_key_down = False

                    if event.key == K_a:
                        self.A_key_down = False

                    if event.key == K_d:
                        self.D_key_down = False

                    if event.key == K_t:
                        self.T_key_down = False

                    if event.key == K_g:
                        self.G_key_down = False

                    if event.key == K_SPACE:
                        self.SPACE_key_down = False

                    if event.key == K_RETURN:
                        self.shooting = False

            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()


    def start(self):
        self.program_loop()

if __name__ == "__main__":
    GraphicsProgram3D().start()