from math import *


class gameObject:
    def __init__(self, position, scale):
        self.position = position
        self.scale = scale
        self.max_x = position.x + (scale.x/2)
        self.min_x = position.x - (scale.x/2)
        self.max_z = position.z + (scale.z / 2)
        self.min_z = position.z - (scale.z / 2)
        self.max_y = position.y + (scale.y / 2)
        self.min_y = position.y - (scale.y / 2)
#(self.min_y <= other.max_y and self.max_y >= other.min_y) and \
    def check_intersection(self, other):
        if (self.min_x <= other.max_x+0.2 and self.max_x >= other.min_x-0.2) and \
                (self.min_z <= other.max_z+0.4 and self.max_z >= other.min_z-0.4):
            return True
        else:
            return False

class Enemy:
    def __init__(self, position):
        self.position = position
        self.distance_x = 0
        self.distance_z = 0

    def update(self, player_pos):
        self.distance_x = sqrt(pow(player_pos.x - self.position.x, 2))
        self.distance_z = sqrt(pow(player_pos.z - self.position.z, 2))
        distance_x_inc = sqrt(pow(player_pos.x - self.position.x+0.1, 2))
        distance_z_inc = sqrt(pow(player_pos.z - self.position.z+0.1, 2))
        distance_x_dec = sqrt(pow(player_pos.x - self.position.x-0.1, 2))
        distance_z_dec = sqrt(pow(player_pos.z - self.position.z-0.1, 2))
        if self.distance_x < distance_x_inc:
            #print("Poop")
            self.position.x += 0.005
        if self.distance_z < distance_z_inc:
            #print("Poop")
            self.position.z += 0.005
        if self.distance_x < distance_x_dec:
            #print("Poop")
            self.position.x -= 0.005
        if self.distance_z < distance_z_dec:
            #print("Poop")
            self.position.z -= 0.005











