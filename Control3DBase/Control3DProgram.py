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
from gameobject import *


class GraphicsProgram3D:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
        self.sprite_shader = SpriteShader()
        self.sprite_shader.use()

        self.shader = Shader3D()
        self.shader.use()
        self.lvl = 1
        self.model_matrix = ModelMatrix()
        self.view_matrix = ViewMatrix()
        self.view_matrix.look(Point(7, 1, 3), Point(7, 1.0, 0.0), Vector(0, 1, 0))
        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        self.shooting = False
        """Sounds"""
        self.hitmarker = pygame.mixer.Sound("sounds/hitmarker.wav")
        self.heartbeat = pygame.mixer.Sound("sounds/heartbeat.wav")

        self.flashlight_angle = 3 * pi / 2  # To calculate flashlight yaw
        self.player_angle = 0

        """Textures"""
        self.shader.set_diffuse_texture(0)
        self.tex_id_wall_diffuse = self.load_texture("./textures/window_texture.jpeg")
        self.shader.set_specular_texture(1)
        self.tex_id_wall_specular = self.load_texture("./textures/window_texture.jpeg")

        self.tex_id_flashlight_diffuse = self.load_texture("./textures/rifle3.png")
        self.tex_id_flashlight_specular = self.load_texture("./textures/rifle3.png")

        self.tex_id_building_diffuse = self.load_texture("./textures/building.jpg")
        self.tex_id_building_specular = self.load_texture("./textures/building.jpg")

        self.tex_id_building2_diffuse = self.load_texture("./textures/building2.jpg")
        self.tex_id_building2_specular = self.load_texture("./textures/building2.jpg")

        self.tex_id_floorandceiling = self.load_texture("./textures/road.jpg")
        self.tex_id_floorandceiling_specular = self.load_texture("./textures/road.jpg")

        self.tex_id_brick_diff = self.load_texture("./textures/brick.jpg")
        self.tex_id_brick_spec = self.load_texture("./textures/brick.jpg")

        self.tex_id_train_diffuse = self.load_texture("./textures/train.png")
        self.tex_id_train_specular = self.load_texture("./textures/train.png")

        self.tex_id_player_diffuse = self.load_texture("./textures/unwrap.jpg")
        self.tex_id_player_specular = self.load_texture("./textures/unwrap.jpg")

        self.tex_id_roadintersection_dif = self.load_texture("./textures/roadint.png")
        self.tex_id_roadintersection_spec = self.load_texture("./textures/roadint.png")

        self.tex_id_rail_dif = self.load_texture("./textures/rail.jpg")
        self.tex_id_rail_spec = self.load_texture("./textures/rail.jpg")

        self.tex_id_truck_diffuse = self.load_texture("./textures/truck.png")
        self.tex_id_truck_specular = self.load_texture("./textures/truck.png")

        self.tex_id_creambrick_dif = self.load_texture("./textures/creambrick.jpg")
        self.tex_id_creambrick_spec = self.load_texture("./textures/creambrick.jpg")

        self.tex_id_brokenhouse_diff = self.load_texture("./textures/brokenhouse.jpg")
        self.tex_id_brokenhouse_spec = self.load_texture("./textures/brokenhouse.jpg")

        self.tex_id_stop_diffuse = self.load_texture("./textures/stop.png")
        self.tex_id_stop_specular = self.load_texture("./textures/stop.png")

        self.tex_id_car1_dif = self.load_texture("./textures/car1.png")
        self.tex_id_car1_spec = self.load_texture("./textures/car1.png")

        self.tex_id_humvee_dif = self.load_texture("./textures/humvee.png")
        self.tex_id_humvee_spec = self.load_texture("./textures/humvee.png")

        self.tex_id_station_dif = self.load_texture("./textures/gas.png")
        self.tex_id_station_spec = self.load_texture("./textures/gas.png")

        self.tex_id_building3_dif = self.load_texture("./textures/oldbuilding.jpg")
        self.tex_id_building3_spec = self.load_texture("./textures/oldbuilding.jpg")

        self.tex_id_tunnel_dif = self.load_texture("./textures/tunnel1.jpg")
        self.tex_id_tunnel_spec = self.load_texture("./textures/tunnel1.jpg")

        self.tex_id_cape_dif = self.load_texture("./textures/cape.png")
        self.tex_id_cape_spec = self.load_texture("./textures/cape.png")

        self.tex_id_fountain_dif = self.load_texture("./textures/fountain.png")
        self.tex_id_fountain_spec = self.load_texture("./textures/fountain.png")

        self.tex_id_skysphere = self.load_texture("./textures/skysphere.jpeg")

        self.tex_id_hitmarker_color = self.load_texture("./textures/hitmarker_color.png")
        self.tex_id_hitmarker_alpha = self.load_texture("./textures/hitmarker_alpha.png")

        self.tex_id_low_health_color = self.load_texture("./textures/blood.png")
        self.tex_id_low_health_alpha = self.load_texture("./textures/blood.png")

        self.projection_matrix = ProjectionMatrix()
        self.fov = pi / 2
        self.projection_matrix.set_perspective(pi / 2, 800 / 600, 0.5, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())
        self.cube = Cube()
        self.sky_sphere = SkySphere(128, 256)
        self.scale = Point(1, 1, 1)
        self.clock = pygame.time.Clock()

        """Obj models"""
        self.obj_model_gun = objloader.load_obj_file(sys.path[0] + '/objects/', 'gun.obj')
        self.obj_model_stop = objloader.load_obj_file(sys.path[0] + '/objects/', 'stop.obj')
        self.obj_model_truck = objloader.load_obj_file(sys.path[0] + '/objects/', 'truck.obj')
        self.obj_model_car1 = objloader.load_obj_file(sys.path[0] + '/objects/', 'car1.obj')
        self.obj_model_train = objloader.load_obj_file(sys.path[0] + '/objects/', 'train.obj')
        self.obj_model_humvee = objloader.load_obj_file(sys.path[0] + '/objects/', 'humvee.obj')
        self.obj_model_station = objloader.load_obj_file(sys.path[0] + '/objects/', 'station.obj')
        self.obj_model_cape = objloader.load_obj_file(sys.path[0] + '/objects/', 'cape.obj')
        self.obj_model_fountain = objloader.load_obj_file(sys.path[0] + '/objects/', 'fountain.obj')

        """Walls: x, y, z positions, and x, y, z scale"""
        self.wall_list2 = [
            [11.1, 2.0, 1.5, 2, 3, 7.5],
            [5.1, 2.0, 1.5, 2, 3, 7.5],
            [8.0232, 1.0, 4.1309, 0.8, 1.0, 1.0],
            [8.2, 1.0, 1.4405, 0.8, 1.0, 1.2],
            [5.85, 1.0, -3.25, 0.5, 3.0, 2.0],
            [5.85, 1.0, -7.3, 0.5, 3.0, 3.25],
            [4.85, 1.0, -9.0, 2.5, 3.0, 0.5],
            [0.5, 1.0, -3.25, 10.2, 3.0, 0.5],
            [-0.5, 1.0, -6.7, 8.2, 3.0, 0.5],
            [3.7, 1.0, -7.6, 0.5, 3.0, 2.3],
            [-4.6, 1.0, -4.975, 0.5, 3.0, 3.0],
            [14.9, 1.0, -6, 3.0, 3.0, 6.0],
            [9.1, 0.0, -2.0, 40.0, 1.0, 40.0],

        ]

        self.train_station = [
            [5.85, 1.5, -3.25, 0.5, 2.0, 2.0],
            [5.85, 1.5, -7.3, 0.5, 2.0, 3.25],
            [4.85, 1.5, -9.0, 2.5, 2.0, 0.5],
            [0.5, 1.5, -3.25, 10.2, 2.0, 0.5],
            [-0.5, 1.5, -6.7, 8.2, 2.0, 0.5],
            [3.7, 1.5, -7.6, 0.5, 2.0, 2.3],
        ]

        self.close_walls = []

        """A lot of stuff we need"""

        self.collisionLeftWall = False
        self.collisionRightWall = False
        self.collisionTopWall = False
        self.collisionBottomWall = False
        self.collisionUpWall = False
        self.A_key_down = False
        self.D_key_down = False
        self.T_key_down = False
        self.G_key_down = False
        self.UP_key_down = False
        self.DOWN_key_down = False
        self.falling = False
        self.SPACE_key_down = False
        self.p_key_down = False
        self.aiming = False
        self.won = False
        self.jumping = False
        self.lookUP = False
        self.shot_list = []
        self.counter = 0
        self.collision = False
        self.hit_counter = 0
        self.health = 1000

        self.sprite = Sprite()
        #self.enemy = Enemy(Point(7, 0.5, -4))
        self.enemy_list_lvl1 = [
            gameObject(Point(7, 0.5, -4), Point(1, 1, 1), 0, 0.005),
            gameObject(Point(9.1, 0.5, -4.3), Point(1, 1, 1), 0, 0.002),
            gameObject(Point(3.3, 0.5, -4.2), Point(1, 1, 1), 0, 0.009),
            gameObject(Point(7.4, 0.5, -4.1), Point(1, 1, 1), 0, 0.007)
        ]
        #self.enemy1 = Enemy(Point(10, 0.5, -10))


        self.collison_check()
        self.get_walls_closest()

    def get_walls_closest(self):
        for item in self.wall_list2:
            if item[0] - 5.5 <= self.view_matrix.eye.x <= item[0] + 5.5:
                if item[2] - 5.5 <= self.view_matrix.eye.z <= item[2] + 5.5:
                    if item not in self.close_walls:
                        self.close_walls.append(item)
                        continue
                else:
                    if item in self.close_walls:
                        self.close_walls.remove(item)

    def collison_check(self):
        for item in self.wall_list2:
            wall_min_x = item[0] - item[3] / 2
            wall_max_x = item[0] + item[3] / 2
            wall_max_y = item[1] + item[4] / 2
            wall_min_y = item[1] - item[4] / 2
            wall_min_z = item[2] - item[5] / 2
            wall_max_z = item[2] + item[5] / 2

            if wall_max_x + 0.2 >= self.view_matrix.eye.x >= wall_max_x + 0.1:
                if wall_min_z - 0.1 <= self.view_matrix.eye.z <= wall_max_z + 0.1:
                    if wall_max_y-0.1 > self.view_matrix.eye.y:
                        self.collisionRightWall = True
                        return True
            else:
                self.collisionRightWall = False

            if wall_min_x - 0.2 <= self.view_matrix.eye.x <= wall_min_x - 0.1:
                if wall_min_z - 0.2 <= self.view_matrix.eye.z <= wall_max_z + 0.1:
                    if wall_max_y-0.1 > self.view_matrix.eye.y > wall_min_y:
                        self.collisionLeftWall = True
                        return True
            else:
                self.collisionLeftWall = False

            if wall_min_z - 0.2 <= self.view_matrix.eye.z <= wall_min_z - 0.1:
                if wall_min_x - 0.1 <= self.view_matrix.eye.x <= wall_max_x + 0.1:
                    if wall_max_y-0.1 > self.view_matrix.eye.y > wall_min_y:
                        self.collisionTopWall = True
                        return True
            else:
                self.collisionTopWall = False

            if wall_max_z + 0.2 >= self.view_matrix.eye.z >= wall_max_z + 0.1:
                if wall_min_x - 0.1 <= self.view_matrix.eye.x <= wall_max_x + 0.1:
                    if wall_max_y-0.1 > self.view_matrix.eye.y > wall_min_y:
                        self.collisionBottomWall = True
                        return True
            else:
                self.collisionBottomWall = False

            if wall_max_z + 0.2 >= self.view_matrix.eye.z >= wall_min_z - 0.1:
                if wall_min_x - 0.1 <= self.view_matrix.eye.x <= wall_max_x + 0.1:
                    if wall_max_y + 0.5 >= self.view_matrix.eye.y >= wall_max_y-0.1:
                        self.collisionUpWall = True
                        return True
            else:
                self.collisionUpWall = False

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
        gravity = 3 * delta_time
        self.collison_check()
        if self.A_key_down:
            self.view_matrix.yaw(-150 * delta_time)
            self.flashlight_angle += -((5 * pi) / 6) * delta_time
            self.player_angle += -((5 * pi) / 6) * delta_time
        if self.D_key_down:
            self.view_matrix.yaw(150 * delta_time)
            self.flashlight_angle += ((5 * pi) / 6) * delta_time
            self.player_angle += ((5 * pi) / 6) * delta_time
        if self.T_key_down:
            self.fov -= 0.25 * delta_time
        if self.G_key_down:
            self.fov += 0.25 * delta_time
        if self.UP_key_down and not self.collisionLeftWall and not self.collisionRightWall and not self.collisionTopWall and not self.collisionBottomWall:
            self.view_matrix.slide(0, 0, -2.0 * delta_time)
        if self.SPACE_key_down:
            self.aiming = True
            self.fov -= self.fov - 0.75
        if not self.SPACE_key_down:
            self.aiming = False
            self.fov = pi / 2

        player = gameObject(self.view_matrix.eye, Point(0.5, 0.5, 0.5))
        for enemy in self.enemy_list_lvl1:
            enemy.update(self.view_matrix.eye)
            if enemy.check_intersection(player):
                self.health -= 1
                #print(self.health)

        # if self.lookUP:
        # self.view_matrix.pitch(-(pi/2)*delta_time)
        # if self.DOWN_key_down:
        # self.view_matrix.pitch((pi/2)*delta_time)
        if self.jumping:
            self.view_matrix.eye.y += gravity
            if self.view_matrix.eye.y >= 1.8:
                self.jumping = False
        if self.shooting:
            while len(self.shot_list) <= 1:
                shot = gameObject(self.view_matrix.eye, Point(0.01, 0.01, 0.01))
                self.shot_list.append(shot)

        for shot in self.shot_list:
            shot.position += (Point(-self.view_matrix.n.x, 0, -self.view_matrix.n.z))
            updated_shot = gameObject(shot.position, shot.scale)
            for enemy in self.enemy_list_lvl1:
                if updated_shot.check_intersection(enemy):
                    enemy.hit_counter += 1
                    pygame.mixer.Sound.play(self.hitmarker, 0)
                    self.collision = True
                    if enemy.hit_counter > 10:
                        self.enemy_list_lvl1.remove(enemy)
                        self.collision = False

                #print(self.hit_counter)
            if shot.position.x < -20 or shot.position.z < -20 or shot.position.x > 20 or shot.position.z > 20:
                self.shot_list.remove(shot)

        if self.collision:
            self.counter += 1
            #print(self.counter)
        if self.counter > 10:
            self.collision = False
            self.counter = 0

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
        if self.health < 1001:
            self.health += 0.5
            #print(self.health)
        # print(self.view_matrix.eye.x, self.view_matrix.eye.y, self.view_matrix.eye.z)
        if self.health < 200:
            pygame.mixer.Sound.play(self.heartbeat)
        if self.health > 200:
            pygame.mixer.Sound.stop(self.heartbeat)
        #if self.health == 0:

        """If player is falling, the game ends"""
        if self.view_matrix.eye.y <= -4:
            pygame.quit()
            quit()
            print("You died, don't walk away from the area")
            """Our functions must be called here in the update"""
        # print(self.view_matrix.eye.x, self.view_matrix.eye.y, self.view_matrix.eye.z)
        self.collison_check()
        self.get_walls_closest()
        if not self.collisionUpWall and not self.jumping and not self.collisionLeftWall and not self.collisionRightWall\
                and not self.collisionTopWall and not self.collisionBottomWall:
            self.view_matrix.eye.y -= gravity


    def display(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_FRAMEBUFFER_SRGB)
        glShadeModel(GL_SMOOTH)
        glLoadIdentity()
        glMatrixMode(GL_PROJECTION)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glViewport(0, 0, 800, 600)
        self.model_matrix.load_identity()
        self.sprite_shader.use()
        self.sprite_shader.set_projection_matrix(self.projection_matrix.get_matrix())
        self.sprite_shader.set_view_matrix(self.view_matrix.get_matrix())

        glDisable(GL_DEPTH_TEST)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_skysphere)
        self.sprite_shader.set_diffuse_texture(0)
        self.sprite_shader.set_alpha_texture(None)
        self.sprite_shader.set_opacity(1.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(self.view_matrix.eye.x, self.view_matrix.eye.y, self.view_matrix.eye.z - 0.08)
        self.sprite_shader.set_model_matrix(self.model_matrix.matrix)
        self.sky_sphere.draw(self.sprite_shader)
        self.model_matrix.pop_matrix()
        glDisable(GL_TEXTURE_2D)

        glEnable(GL_DEPTH_TEST)
        glClear(GL_DEPTH_BUFFER_BIT)

        self.shader.use()
        self.projection_matrix.set_perspective(self.fov, 800 / 600, 0.01, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        self.cube.set_verticies(self.shader)

        self.shader.set_eye_position(self.view_matrix.eye)
        """"LIGHTS"""
        self.shader.set_normal_light_direction(Point(1.5, 1, -2))
        self.shader.set_normal_light_color(Color(1.0, 1.0, 1.0))
        self.shader.set_other_light_direction(Point(-1.5, -1, -2))

        """Drawing and some more drawing....."""

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_station_dif)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_station_spec)
        self.shader.set_use_texture(1.0)
        self.shader.set_material_diffuse(Color(1.0, 0.65, 0.1))
        self.shader.set_material_shiny(10)
        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_emit(0.0)
        for shot in self.shot_list:
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(shot.position.x, shot.position.y, shot.position.z)
            self.model_matrix.add_scale(shot.scale.x, shot.scale.y, shot.scale.z)
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.cube.draw()
            self.model_matrix.pop_matrix()
        self.shader.set_use_texture(0.0)
        glDisable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, -1)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_tunnel_dif)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_tunnel_spec)
        self.shader.set_use_texture(1.0)
        self.shader.set_material_diffuse(Color(1.0, 0.65, 0.1))
        self.shader.set_material_shiny(10)
        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_emit(0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(-4.6, 1.2, -4.975)
        self.model_matrix.add_rotate_x(3 * pi / 2)
        self.model_matrix.add_scale(0.5, 4.0, 2.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()
        self.shader.set_use_texture(0.0)
        glDisable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, -1)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_floorandceiling)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_floorandceiling_specular)
        self.shader.set_use_texture(1.0)
        self.shader.set_material_diffuse(Color(1.0, 0.65, 0.1))
        self.shader.set_material_shiny(10)
        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_emit(0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(8.1, 0.0, 1.0)
        self.model_matrix.add_scale(4.0, 1.0, 8.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()
        self.shader.set_use_texture(0.0)
        glDisable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, -1)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_brick_diff)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_brick_spec)
        self.shader.set_use_texture(1.0)
        self.shader.set_material_diffuse(Color(1.0, 0.65, 0.1))
        self.shader.set_material_shiny(10)
        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_emit(0.0)
        for item in self.train_station:
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(item[0], item[1], item[2])
            self.model_matrix.add_scale(item[3], item[4], item[5])
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.cube.draw()
            self.model_matrix.pop_matrix()
        self.shader.set_use_texture(0.0)
        glDisable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, -1)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_roadintersection_dif)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_roadintersection_spec)
        self.shader.set_use_texture(1.0)
        self.shader.set_material_diffuse(Color(1.0, 0.65, 0.1))
        self.shader.set_material_shiny(10)
        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_emit(0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(7.9, 0.0, -5.0)
        self.model_matrix.add_scale(8.0, 1.0, 8.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()
        self.shader.set_use_texture(0.0)
        glDisable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, -1)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_rail_dif)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_rail_spec)
        self.shader.set_use_texture(1.0)
        self.shader.set_material_diffuse(Color(1.0, 0.65, 0.1))
        self.shader.set_material_shiny(10)
        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_emit(0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(1.0, 0.0, -5.0)
        self.model_matrix.add_scale(8.0, 1.0, 3.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()
        self.shader.set_use_texture(0.0)
        glDisable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, -1)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_building_diffuse)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_building_specular)
        self.shader.set_use_texture(1.0)
        self.shader.set_material_diffuse(Color(1.0, 0.65, 0.1))
        self.shader.set_material_shiny(10)
        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_emit(0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(11.1, 2.0, 1.5)
        self.model_matrix.add_scale(2, 3, 7.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()
        self.shader.set_use_texture(0.0)
        glDisable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, -1)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_building2_diffuse)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_building2_specular)
        self.shader.set_use_texture(1.0)
        self.shader.set_material_diffuse(Color(1.0, 0.65, 0.1))
        self.shader.set_material_shiny(10)
        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_emit(0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(5.1, 2.0, 1.5)
        self.model_matrix.add_scale(2, 3, 7.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()
        self.shader.set_use_texture(0.0)
        glDisable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, -1)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_creambrick_dif)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_creambrick_spec)
        self.shader.set_use_texture(1.0)
        self.shader.set_material_diffuse(Color(1.0, 0.65, 0.1))
        self.shader.set_material_shiny(10)
        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_emit(0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(13.24, 1.0, -7.1)
        self.model_matrix.add_scale(0.5, 1.1, 1.9)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()
        self.shader.set_use_texture(0.0)
        glDisable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, -1)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_creambrick_dif)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_creambrick_spec)
        self.shader.set_use_texture(1.0)
        self.shader.set_material_diffuse(Color(1.0, 0.65, 0.1))
        self.shader.set_material_shiny(10)
        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_emit(0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(13.5, 1.0, -4.0)
        self.model_matrix.add_scale(0.5, 1.1, 1.9)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()
        self.shader.set_use_texture(0.0)
        glDisable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, -1)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_creambrick_dif)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_creambrick_spec)
        self.shader.set_use_texture(1.0)
        self.shader.set_material_diffuse(Color(1.0, 0.65, 0.1))
        self.shader.set_material_shiny(10)
        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_emit(0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(11.9, 1.0, -2.6)
        self.model_matrix.add_scale(0.3, 1.1, 1.3)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()
        self.shader.set_use_texture(0.0)
        glDisable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, -1)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_creambrick_dif)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_creambrick_spec)
        self.shader.set_use_texture(1.0)
        self.shader.set_material_diffuse(Color(1.0, 0.65, 0.1))
        self.shader.set_material_shiny(10)
        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_emit(0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(12.9, 1.0, -3.0)
        self.model_matrix.add_scale(1.8, 1.1, 0.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()
        self.shader.set_use_texture(0.0)
        glDisable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, -1)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_brokenhouse_diff)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_brokenhouse_spec)
        self.shader.set_use_texture(1.0)
        self.shader.set_material_diffuse(Color(1.0, 0.65, 0.1))
        self.shader.set_material_shiny(10)
        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_emit(0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(10.0, 2.0, -8.6)
        self.model_matrix.add_scale(7.8, 3, 2.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()
        self.shader.set_use_texture(0.0)
        glDisable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, -1)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_cape_dif)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_cape_spec)
        for enemy in self.enemy_list_lvl1:
            self.shader.set_use_texture(1.0)
            self.shader.set_material_diffuse(Color(1.0, 0.65, 0.1))
            self.shader.set_material_shiny(10)
            self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
            self.shader.set_material_emit(0.0)
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(enemy.position.x, enemy.position.y, enemy.position.z)
            self.model_matrix.add_scale(1, 1, 1)
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.obj_model_cape.draw(self.shader)
            self.model_matrix.pop_matrix()
            self.shader.set_use_texture(0.0)
        glDisable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, -1)


        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_fountain_dif)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_fountain_spec)
        self.shader.set_use_texture(1.0)
        self.shader.set_material_diffuse(Color(1.0, 0.65, 0.1))
        self.shader.set_material_shiny(10)
        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_emit(0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(8.5, 0.5, -5.0)
        self.model_matrix.add_scale(0.4, 0.4, 0.4)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.obj_model_fountain.draw(self.shader)
        self.model_matrix.pop_matrix()
        self.shader.set_use_texture(0.0)
        glDisable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, -1)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_flashlight_diffuse)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_flashlight_specular)
        self.shader.set_use_texture(1.0)
        self.shader.set_material_diffuse(Color(1.0, 0.65, 0.1))
        self.shader.set_material_shiny(10)
        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_emit(0.0)
        self.model_matrix.push_matrix()
        if self.aiming == False:
            self.model_matrix.add_translation(self.view_matrix.eye.x + 0.1, self.view_matrix.eye.y - 0.3,
                                              self.view_matrix.eye.z)
        if self.aiming == True:
            self.model_matrix.add_translation(self.view_matrix.eye.x, self.view_matrix.eye.y - 0.2,
                                              self.view_matrix.eye.z)
        self.model_matrix.add_rotate_y(-self.flashlight_angle)
        self.model_matrix.add_scale(0.1, 0.1, 0.15)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.obj_model_gun.draw(self.shader)
        self.model_matrix.pop_matrix()
        self.shader.set_use_texture(0.0)
        glDisable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, -1)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_truck_diffuse)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_truck_specular)
        self.shader.set_use_texture(1.0)
        self.shader.set_material_diffuse(Color(1.0, 0.65, 0.1))
        self.shader.set_material_shiny(10)
        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_emit(0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(8.75, 0.55, 1.5)
        self.model_matrix.add_rotate_y(pi)
        self.model_matrix.add_scale(0.1, 0.1, 0.15)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.obj_model_truck.draw(self.shader)
        self.model_matrix.pop_matrix()
        self.shader.set_use_texture(0.0)
        glDisable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, -1)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_car1_dif)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_car1_spec)
        self.shader.set_use_texture(1.0)
        self.shader.set_material_diffuse(Color(1.0, 0.65, 0.1))
        self.shader.set_material_shiny(10)
        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_emit(0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(3.4, 0.45, -0.7)
        self.model_matrix.add_rotate_y(pi)
        self.model_matrix.add_scale(0.8, 1.0, 1.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.obj_model_car1.draw(self.shader)
        self.model_matrix.pop_matrix()
        self.shader.set_use_texture(0.0)
        glDisable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, -1)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_train_diffuse)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_train_specular)
        self.shader.set_use_texture(1.0)
        self.shader.set_material_diffuse(Color(1.0, 0.65, 0.1))
        self.shader.set_material_shiny(10)
        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_emit(0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(0.5, 0.4, -5.0)
        self.model_matrix.add_rotate_y(pi / 2)
        self.model_matrix.add_scale(0.3, 0.2, 0.1)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.obj_model_train.draw(self.shader)
        self.model_matrix.pop_matrix()
        self.shader.set_use_texture(0.0)
        glDisable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, -1)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_humvee_dif)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_humvee_spec)
        self.shader.set_use_texture(1.0)
        self.shader.set_material_diffuse(Color(1.0, 0.65, 0.1))
        self.shader.set_material_shiny(10)
        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_emit(0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(12.5, 1.0, -7.1)
        self.model_matrix.add_rotate_y(3 * pi / 2)
        self.model_matrix.add_scale(0.35, 0.4, 0.3)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.obj_model_humvee.draw(self.shader)
        self.model_matrix.pop_matrix()
        self.shader.set_use_texture(0.0)
        glDisable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, -1)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_stop_diffuse)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_stop_specular)
        self.shader.set_use_texture(1.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(3.0, 0.4, -3.9)
        self.model_matrix.add_rotate_y(pi / 2)
        self.model_matrix.add_scale(0.0017, 0.0017, 0.0017)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.obj_model_stop.draw(self.shader)
        self.model_matrix.pop_matrix()
        self.shader.set_use_texture(0.0)
        glDisable(GL_TEXTURE_2D)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_stop_diffuse)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_stop_specular)
        self.shader.set_use_texture(1.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(3.0, 0.4, -6.1)
        self.model_matrix.add_rotate_y(pi / 2)
        self.model_matrix.add_scale(0.0017, 0.0017, 0.0017)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.obj_model_stop.draw(self.shader)
        self.model_matrix.pop_matrix()
        self.shader.set_use_texture(0.0)
        glDisable(GL_TEXTURE_2D)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_station_dif)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_station_spec)
        self.shader.set_use_texture(1.0)
        self.shader.set_material_diffuse(Color(1.0, 0.65, 0.1))
        self.shader.set_material_shiny(10)
        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_emit(0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(11.5, 0.5, -4.5)
        self.model_matrix.add_rotate_y(3 * pi / 2)
        self.model_matrix.add_scale(0.15, 0.2, 0.15)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.obj_model_station.draw(self.shader)
        self.model_matrix.pop_matrix()
        self.shader.set_use_texture(0.0)
        glDisable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, -1)


        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        self.sprite_shader.use()
        self.sprite_shader.set_projection_matrix(self.projection_matrix.get_matrix())
        self.sprite_shader.set_view_matrix(self.view_matrix.get_matrix())
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        if self.collision:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.tex_id_hitmarker_color)
            self.sprite_shader.set_diffuse_texture(0)
            glActiveTexture(GL_TEXTURE1)
            glBindTexture(GL_TEXTURE_2D, self.tex_id_hitmarker_alpha)
            self.sprite_shader.set_alpha_texture(1)
            self.sprite_shader.set_opacity(1.0)
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(self.view_matrix.eye.x - self.view_matrix.n.x, self.view_matrix.eye.y-0.01, self.view_matrix.eye.z-self.view_matrix.n.z)
            self.model_matrix.add_rotate_y(-self.player_angle)
            self.model_matrix.add_scale(0.1, 0.1, 0.1)
            self.sprite_shader.set_model_matrix(self.model_matrix.matrix)
            self.sprite.draw(self.sprite_shader)
            self.model_matrix.pop_matrix()
        glDisable(GL_DEPTH_TEST)


        #glClear(GL_COLOR_BUFFER_BIT)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_low_health_color)
        self.sprite_shader.set_diffuse_texture(0)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_low_health_alpha)
        if self.health < 200:
            self.sprite_shader.set_alpha_texture(1)
            self.sprite_shader.set_opacity(1.0)
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(self.view_matrix.eye.x - self.view_matrix.n.x, self.view_matrix.eye.y, self.view_matrix.eye.z - self.view_matrix.n.z)
            self.model_matrix.add_rotate_y(-self.player_angle)
            self.model_matrix.add_scale(3.0, 2.0, 3.0)
            self.sprite_shader.set_model_matrix(self.model_matrix.matrix)
            self.sprite.draw(self.sprite_shader)
            self.model_matrix.pop_matrix()
        glDisable(GL_TEXTURE_2D)
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
                    if event.key == K_UP:
                        self.lookUP = True
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

                    if event.key == K_f:
                        self.jumping = True

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

                    if event.key == K_UP:
                        self.lookUP = False

            self.update()
            self.display()

        # OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()


if __name__ == "__main__":
    GraphicsProgram3D().start()
