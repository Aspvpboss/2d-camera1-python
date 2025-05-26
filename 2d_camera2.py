import pygame
from sys import exit
import time

class Game:
    def __init__(self):
        #this is test3-branch
        pygame.init()
        # general 
        self.FPS_DICTIONARY = {"60" : 60, "144" : 144, "240" : 240, "Unlimited" : 1000}
        FPS_STRING = "240"
        self.FPS = self.FPS_DICTIONARY[FPS_STRING]
        RESOLUTIONS = {"720p" : [1280, 720], "1080p" : [1920, 1080], "1440p" : [2560, 1440]}
        RESOLUTION = "1080p"
        self.DISPLAY_WIDTH = RESOLUTIONS[RESOLUTION][0]
        self.DISPLAY_HEIGHT = RESOLUTIONS[RESOLUTION][1]
        self.SCREEN = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT - 80))
        self.CLOCK = pygame.time.Clock()
        self.FONT = pygame.font.Font(None, 30)
        self.dt = 0
        self.current_time = 0
        self.previous_time = time.time()

        # world 
        self.TILE_SIZE = self.DISPLAY_HEIGHT // 21
        self.WORLD_WIDTH = 100
        self.WORLD_HEIGHT = 100
        # self.WORLD_WIDTH = self.DISPLAY_WIDTH // self.TILE_SIZE
        # self.WORLD_HEIGHT = self.DISPLAY_HEIGHT // self.TILE_SIZE
        self.create_surfaces()

        # camera
        self.camera_world_x = 0
        self.camera_world_y = 0        
        self.CAMERA_WORLD_WIDTH = self.DISPLAY_WIDTH // self.TILE_SIZE 
        self.CAMERA_WORLD_HEIGHT = self.DISPLAY_HEIGHT // self.TILE_SIZE 

        self.camera_display_x = self.camera_world_x * self.TILE_SIZE
        self.camera_display_y = self.camera_world_y * self.TILE_SIZE
        self.camera_offset_x = 0
        self.camera_offset_y = 0
        self.CAMERA_DISPLAY_WIDTH = self.CAMERA_WORLD_WIDTH * self.TILE_SIZE
        self.CAMERA_DISPLAY_HEIGHT = self.CAMERA_WORLD_HEIGHT * self.TILE_SIZE

        

        self.grid = [[0 for _ in range(self.WORLD_WIDTH)] for _ in range(self.WORLD_HEIGHT)]
        for grid_y in range(0, self.WORLD_HEIGHT):

            for grid_x in range(0, self.WORLD_WIDTH):

                if grid_x % 2 == 0:

                    if grid_y % 2 == 0:

                        self.grid[grid_y][grid_x] = 1
                    else:

                            self.grid[grid_y][grid_x] = 0

                else:

                    if grid_y % 2 == 0:

                        self.grid[grid_y][grid_x] = 0
                    else:

                        self.grid[grid_y][grid_x] = 1

    def create_surfaces(self):
        self.surface1 = pygame.Surface((self.TILE_SIZE, self.TILE_SIZE))
        self.surface1.fill((0, 255, 0))
        self.surface2 = pygame.Surface((self.TILE_SIZE, self.TILE_SIZE))
        self.surface2.fill((0, 200 , 0))
        self.camera_surface = pygame.Surface((self.TILE_SIZE, self.TILE_SIZE))
        self.camera_surface.fill((255, 255, 255))

    def calculate_dt(self):
        self.current_time = time.time()
        self.dt = self.current_time - self.previous_time
        self.previous_time = self.current_time        

    def quit_game(self):
        pygame.quit()
        exit()



    def inside_camera(self, screen_x, screen_y):
        if screen_x < self.camera_world_x + self.CAMERA_WORLD_WIDTH and screen_x > self.camera_world_x - self.CAMERA_WORLD_WIDTH:
            if screen_x >= 0 and screen_x < self.WORLD_WIDTH:
                if screen_y < self.camera_world_y + self.CAMERA_WORLD_HEIGHT and screen_y > self.camera_world_y - self.CAMERA_WORLD_HEIGHT:
                    if screen_y >= 0 and screen_y < self.WORLD_HEIGHT:
                        return True
        return False


    def handle_event(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.quit_game()

            # toggle fullscreen / windowed
        just_pressed = pygame.key.get_just_pressed()
        pressed = pygame.key.get_pressed()

        if just_pressed[pygame.K_F11]:

            if pygame.display.is_fullscreen():

                self.SCREEN = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT - 80))
                
            else:

                self.SCREEN = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT), pygame.FULLSCREEN)

        if just_pressed[pygame.K_ESCAPE]:

            self.quit_game()

        # scroll wheel
        mouse_just_pressed = pygame.mouse.get_just_pressed()

        if mouse_just_pressed[3]:
            self.TILE_SIZE -= 4
            self.create_surfaces()

        if mouse_just_pressed[4]:
            self.TILE_SIZE += 4
            self.create_surfaces()

        if self.TILE_SIZE < 8:
            self.TILE_SIZE = 8

        if self.TILE_SIZE > 60:
            self.TILE_SIZE = 60
        
        # wasd
        movement_speed = self.dt * 500
        camera_movement_x = 0
        camera_movement_y = 0
        camera_movement_x += (pressed[pygame.K_d] - pressed[pygame.K_a]) * movement_speed
        camera_movement_y += (pressed[pygame.K_s] - pressed[pygame.K_w]) * movement_speed

        self.camera_display_x = round(self.camera_display_x + camera_movement_x)
        self.camera_display_y = round(self.camera_display_y + camera_movement_y)
        
        # limit inputs
        if self.camera_display_x < 0:
            self.camera_display_x = 0

        if self.camera_display_x >= (self.WORLD_WIDTH - 1) * self.TILE_SIZE:
            self.camera_display_x = (self.WORLD_WIDTH - 1) * self.TILE_SIZE

        if self.camera_display_y < 0:
            self.camera_display_y = 0

        if self.camera_display_y >= (self.WORLD_HEIGHT - 1) * self.TILE_SIZE:
            self.camera_display_y = (self.WORLD_HEIGHT - 1) * self.TILE_SIZE


        # get offset values
        self.camera_world_x = self.camera_display_x // self.TILE_SIZE
        self.camera_offset_x = self.camera_display_x - (self.camera_world_x * self.TILE_SIZE)

        self.camera_world_y = self.camera_display_y // self.TILE_SIZE
        self.camera_offset_y = self.camera_display_y - (self.camera_world_y * self.TILE_SIZE)

        
      
    def handle_render(self):
        self.SCREEN.fill((0, 0, 0))
        for screen_y in range(self.camera_world_y - self.CAMERA_WORLD_HEIGHT, self.camera_world_y + self.CAMERA_WORLD_HEIGHT):
            for screen_x in range(self.camera_world_x - self.CAMERA_WORLD_WIDTH, self.camera_world_x + self.CAMERA_WORLD_WIDTH):

                if self.inside_camera(screen_x, screen_y):

                    temp_camera_x = (self.DISPLAY_WIDTH // 2) + ((screen_x - self.camera_world_x) * self.TILE_SIZE) - self.camera_offset_x
                    temp_camera_y = (self.DISPLAY_HEIGHT // 2) + ((screen_y - self.camera_world_y) * self.TILE_SIZE) - self.camera_offset_y


                    if self.grid[screen_y][screen_x] == 1:

                        self.SCREEN.blit(self.surface1, (temp_camera_x, temp_camera_y))
                    
                    if self.grid[screen_y][screen_x] == 0:

                        self.SCREEN.blit(self.surface2, (temp_camera_x, temp_camera_y))

        
                   
    def handle_gui(self):
        fps = int(self.CLOCK.get_fps())
        fps_surface = self.FONT.render(f"{fps}", True, (255, 255, 255))
        self.SCREEN.blit(fps_surface, (10, 10))

    #dooky dook 

    def main(self):
        
        while True:

            self.calculate_dt()
            self.handle_event()
            self.handle_render()
            self.handle_gui()
            self.CLOCK.tick(self.FPS)
            pygame.display.update()

        
if __name__ == "__main__":
    game = Game()
    game.main()