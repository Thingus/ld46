import pygame
from random import randint
import math
from enum import Enum
import pdb

object_dict = {obj_id:None for obj_id in range(0, 300)}    # I know globals are bad but this is LD, baby.
volume = 5


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
        
        door = Door(self.screen, 320, 480)
        global object_dict
        object_dict[door.id] = door

    def run(self):
        running = True
        global object_dict
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_d:
                        pdb.set_trace()
            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds /1000.0
            self.draw_text("FPS: {:6.3}  PLAYTIME: {:6.3} SECONDS".format(
                           self.clock.get_fps(), self.playtime))
            for updateable in object_dict.values():
                if "update" in dir(updateable):
                    updateable.update()
            pygame.display.flip()
            self.screen.blit(self.surface, (0,0))
            for drawable in object_dict.values():
                if "draw" in dir(drawable):
                    drawable.draw()
        pygame.quit()

    def draw_text(self, text):
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, (0, 255, 0))
        self.screen.blit(surface, (0, 0)) 


class Door(object):
    """
    Spawns partygoers
    """
    def __init__(self, parent_surface, x, y, spawn_rate=10, max_guests = 20, width=20, height=10):
        self.surface = pygame.Surface((width, height))
        self.x = x
        self.y = y
        self.spawn_rate = spawn_rate
        self.parent_surface = parent_surface
        self.max_guests = max_guests
        self.spawn_ticker = 0
        self.spawned_guests = 0
        self.id = randint(50, 100)
        
    def new_guest(self):
        Partygoer(self.parent_surface, randint(10, 600), randint(400, 480))
        self.spawned_guests += 1

    def draw(self):
        pass
    
    def update(self):
        if self.spawned_guests > self.max_guests:
            return
        self.spawn_ticker += 1
        if self.spawn_ticker % self.spawn_rate == 0:
            self.spawn_ticker = 0
            self.new_guest()
    
    """
    def guest_left(self, guest):
        guest.
    """  

class Mood(Enum):
    DANCING = 1
    TALKING = 2
    LEAVE = 0

class PartyState(Enum):
    ENTERING = 0
    MOVING_TO_DANCE = 1
    MOVING_TO_TALK = 2
    DANCING = 3
    TALKING = 4
    MOVING_TO_LEAVE = 5

class Partygoer(object):
    
    def __init__(self, parent_surface, x, y,  width = 40, height=120, mood=None):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.parent_surface = parent_surface
        self.x = x
        self.y = y
        self.generate_sprite()
        self.id = randint(100, 300)
        global object_dict
        object_dict[self.id] = self
        if not mood:
            self.mood = Mood(randint(1,2))
        self.state = PartyState.ENTERING
        self.fun = 25

    def generate_sprite(self):
        skin_color = gen_random_color()
        tshirt_color = gen_random_color()
        trouser_color = gen_random_color()
        # Background
        pygame.draw.rect(
            self.surface,
            pygame.Color(255,255,255),
            pygame.Rect(0,0, self.width, self.height))
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

    def state_update(self):
        """
        Check for state transitions
        """
        if self.state == PartyState.ENTERING:
            if self.mood == Mood.DANCING:
                self.move_to_dance()
            elif self.mood == Mood.TALKING:
                self.move_to_talk()
        elif self.state == PartyState.MOVING_TO_DANCE:
            if self.reached_target:
                self.state = PartyState.DANCING
        elif self.state == PartyState.MOVING_TO_TALK:
            if self.reached_target:
                self.state = PartyState.TALKING
        elif self.state == PartyState.MOVING_TO_LEAVE:
            if self.reached_target:
                self.destroy()
        elif self.state == PartyState.DANCING:
            if self.mood == Mood.TALKING:
                self.move_to_talk()
            elif mood == Mood.LEAVING:
                self.state = PartyState.MOVING_TO_LEAVE
        elif self.state == PartyState.TALKING:
            if mood == Mood.DANCING:
                self.move_to_dance()
            elif mood == Mood.LEAVING:
                self.state = PartyState.MOVING_TO_LEAVE
    
    def move_to_dance(self):
        # Pick random spot on dancefloor area
        self.set_move_target(
            x = randint(10, 300),
            y = randint(50, 440),
            speed =  4)
        self.state = PartyState.MOVING_TO_DANCE

    def move_to_talk(self):
        # Pick random spot in bar area
        self.set_move_target(
            x = randint(350, 620),
            y = randint(50, 440),
            speed = 2)
        self.state = PartyState.MOVING_TO_TALK

    def move_to_leave(self):
        # Pick a random spot in the doorway
        self.set_move_target(
            x = randint(200, 400),
            y = randint(450, 480),
            speed = 2) 

    def fun_update(self):
        """
        Adjust fun level based on activity and volume
        """
        if self.state == PartyState.DANCING:
            if volume < 7:  # Music not loud enough
                self.fun -= 5
            else:
                self.fun += 1
        elif self.state == PartyState.TALKING:
            if volume > 3: # Music is too loud
                self.fun -= 5
            else:
                self.fun += 1

    def mood_update(self):
        """
        1 in 5 (?) chance that this partygoer wants to do something else
        """
        if randint(0,4) == 0:
            if self.mood == Mood.DANCING:
                self.mood == Mood.TALKING
            elif self.mood == Mood.TALKING:
                self.mood == Mood.DANCING        

    def draw(self):
        self.parent_surface.blit(self.surface, (self.x, self.y))
    
    def set_move_target(self, x, y, speed):
        self.mt_x = x
        self.mt_y = y
        self.move_speed = speed
        self.reached_target = False        

    def update(self):
        """
        Logic for this thing to do on evey clock step
        """
        self.fun_update()
        self.mood_update()
        self.state_update() 
        self.move_towards_target()
    
    def destroy(self):
        global object_dict
        object_dict[self.id] = None
    
    def move_towards_target(self):
        if self.mt_x == self.x and self.mt_y == self.y:
            self.reached_target = True
        loc = pygame.math.Vector2(self.x, self.y)
        target = pygame.math.Vector2(self.mt_x, self.mt_y)
        distance = loc.distance_to(target)
        proportion = self.move_speed/distance
        try:
            new_pos = loc.lerp(target, proportion)
            self.x = new_pos.x
            self.y = new_pos.y
        except ValueError:
            return

def gen_random_color():
    return  pygame.Color(
            randint(0, 255),
            randint(0, 255),
            randint(0, 255)
            )


if __name__ == "__main__":
    PygView().run()
