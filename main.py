import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 800
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
GREEN = (0, 200, 0)

class Player:
    WIDTH = 50
    HEIGHT = 50
    SPEED_X = 5
    JUMP_STRENGTH = -14
    GRAVITY = 0.6

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)
        self.vel_y = 0
        self.on_ground = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.SPEED_X
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.SPEED_X
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))

    def jump(self):
        if self.on_ground:
            self.vel_y = self.JUMP_STRENGTH
            self.on_ground = False

    def apply_gravity(self, floor):
        self.vel_y += self.GRAVITY
        self.rect.y += self.vel_y
        self.on_ground = False

        if self.rect.bottom >= floor.top:
            self.rect.bottom = floor.top
            self.vel_y = 0
            self.on_ground = True

    def update_camera(self, floor, camera_offset):
        if self.rect.y < HEIGHT // 2:
            scroll = HEIGHT // 2 - self.rect.y
            camera_offset += scroll
            self.rect.y = HEIGHT // 2
            floor.y += scroll
        return camera_offset

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Endless Platformer")
        self.clock = pygame.time.Clock()
        self.running = True
        self.camera_offset = 0

        self.player = Player(WIDTH // 2, HEIGHT - 130)
        self.floor = pygame.Rect(0, HEIGHT - 60, WIDTH, 60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

    def update(self):
        self.player.handle_input()
        self.player.apply_gravity(self.floor)
        self.camera_offset = self.player.update_camera(self.floor, self.camera_offset)

    def draw(self):
        self.screen.fill(WHITE)
        pygame.draw.rect(self.screen, GREEN, self.floor)
        pygame.draw.rect(self.screen, BLUE, self.player.rect)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Game().run()

