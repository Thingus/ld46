import pygame
from random import randint
import math

import pdb

class PygView(object):
    """
    From https://raw.githubusercontent.com/horstjens/ThePythonGameBook/master/pygame/002_display_fps_pretty.py
    """
    
    def __init__(self, width=640, height=480, fps=30):
        pygame.init()
        pygame.display.set_caption("ESC to quit")
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.surface = pygame.Surface(self.screen.get_size()).convert()
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.font = pygame.font.SysFont("mono", 20, bold=True)

        self.object_list = []

    def run(self):
        running = True
        self.object_list.append(Partygoer(parent_object = self, x = 320, y=240))
        self.object_list[0].set_move_target(0, 0, 2)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds /1000.0
            self.draw_text("FPS: {:6.3}\nPLAYTIME: {:6.3} SECONDS".format(
                           self.clock.get_fps(), self.playtime))
            for updateable in self.object_list:
                updateable.update()
            pygame.display.flip()
            self.screen.blit(self.surface, (0,0))
            for drawable in self.object_list:
                drawable.draw()
        pygame.quit()

    def draw_text(self, text):
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, (0, 255, 0))
        self.screen.blit(surface, (0, 0)) 


class Partygoer(object):
    
    def __init__(self, parent_object, x, y,  width = 40, height=120):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.parent_surface = parent_object.surface
        self.x = x
        self.y = y
        self.generate_sprite()
        
    def generate_sprite(self):
        skin_color = gen_random_color()
        tshirt_color = gen_random_color()
        trouser_color = gen_random_color()
        # Tshirt rect
        pygame.draw.rect(
            self.surface,
            tshirt_color,
            pygame.Rect(10, 10, 20, 55))
        # Head
        pygame.draw.rect(
            self.surface,
            skin_color,
            pygame.Rect(12, 0, 16, 16))
        # Left arm
        pygame.draw.rect(
            self.surface,
            skin_color,
            pygame.Rect(0, 10, 10, 50))
        # Right arm
        pygame.draw.rect(
            self.surface,
            skin_color,
            pygame.Rect(30, 10, 10, 50))
        # Left leg
        pygame.draw.rect(
            self.surface,
            trouser_color,
            pygame.Rect(10, 65, 10, 55))
        # Right leg
        pygame.draw.rect(
            self.surface,
            trouser_color,
            pygame.Rect(20, 65, 10, 55))
        
        self.surface.set_colorkey((255, 255, 255))
        self.surface.convert()

    def draw(self):
        self.parent_surface.blit(self.surface, (self.x, self.y))
    
    def set_move_target(self, x, y, speed):
        self.mt_x = x
        self.mt_y = y
        self.move_speed = speed

    def update(self):
        """
        Logic for this thing to do on evey clock step
        """ 
        self.move_towards_target()
    
    def move_towards_target(self):
        loc = pygame.math.Vector2(self.x, self.y)
        target = pygame.math.Vector2(self.mt_x, self.mt_y)
        angle = loc.angle_to(target)
        x_dist = self.move_speed * math.cos(math.radians(angle))
        y_dist = self.move_speed * math.sin(math.radians(angle))
        if self.mt_x > self.x:
            self.x += x_dist
        elif self.mt_x < self.x:
            self.x -= x_dist
        if self.mt_y > self.y:
            self.y += y_dist
        elif self.mt_y < y_dist:
            self.y -= y_dist
        

def gen_random_color():
    return  pygame.Color(
            randint(0, 255),
            randint(0, 255),
            randint(0, 255)
            )


if __name__ == "__main__":
    PygView().run()
