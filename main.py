import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platformer")
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

# Player settings
player_size = (50, 50)
player = pygame.Rect(WIDTH // 2, HEIGHT - 130, *player_size)
player_speed_x = 5
player_vel_y = 0
jump_strength = -14
gravity = 0.6
on_ground = False

# Floor
floor = pygame.Rect(0, HEIGHT - 60, WIDTH, 60)

# Platform settings
platforms = []
platform_width = 100
platform_height = 20
min_platform_gap = 80
max_platform_gap = 130
max_horizontal_reach = 180
platform_density_factor = 2.5  # Higher = fewer platforms, lower = more frequent
num_initial_platforms = 20

# Camera offset
camera_offset = 0
last_x = WIDTH // 2 - platform_width // 2
last_y = HEIGHT - 100
highest_platform_y = last_y

# Generate initial platforms
for i in range(num_initial_platforms):
    dx = random.randint(-max_horizontal_reach, max_horizontal_reach)
    dy = random.randint(min_platform_gap, max_platform_gap)
    x = max(0, min(WIDTH - platform_width, last_x + dx))
    y = last_y - dy
    platforms.append(pygame.Rect(x, y, platform_width, platform_height))
    last_x, last_y = x, y
    highest_platform_y = min(highest_platform_y, y)

# Game loop
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:
                player_vel_y = jump_strength
                on_ground = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed_x
    if keys[pygame.K_RIGHT]:
        player.x += player_speed_x

    player.x = max(0, min(WIDTH - player.width, player.x))

    # Predict next position
    next_y = player.y + player_vel_y
    next_bottom = player.bottom + player_vel_y
    on_ground = False

    # Check platform collisions
    for plat in platforms:
        if player_vel_y >= 0 and player.bottom <= plat.top and next_bottom >= plat.top:
            if player.right > plat.left and player.left < plat.right:
                next_y = plat.top - player.height
                player_vel_y = 0
                on_ground = True
                break

    # Check floor collision
    if player_vel_y >= 0 and player.bottom <= floor.top and next_bottom >= floor.top:
        next_y = floor.top - player.height
        player_vel_y = 0
        on_ground = True

    # Apply gravity and move
    player_vel_y += gravity
    player.y = next_y

    # Update camera
    if player.y < HEIGHT // 2:
        camera_scroll = HEIGHT // 2 - player.y
        player.y = HEIGHT // 2
        camera_offset += camera_scroll
        for plat in platforms:
            plat.y += camera_scroll
        floor.y += camera_scroll
        last_y += camera_scroll
        highest_platform_y += camera_scroll

    # Generate new platforms if needed
    buffer_above_screen = 2 * HEIGHT
    skipped_height = 0
    while last_y > -(camera_offset + buffer_above_screen):
        remaining_gap = max_platform_gap - skipped_height

        # Ensure we never exceed the max gap
        if remaining_gap <= min_platform_gap:
            dy = min_platform_gap
        else:
            dy = random.randint(min_platform_gap, remaining_gap)

        y = last_y - dy
        skipped_height += dy

        must_place = skipped_height >= max_platform_gap or random.random() < 1.0 / platform_density_factor

        if must_place or remaining_gap <= min_platform_gap:
            dx = random.randint(-max_horizontal_reach, max_horizontal_reach)
            x = max(0, min(WIDTH - platform_width, last_x + dx))
            platforms.append(pygame.Rect(x, y, platform_width, platform_height))
            last_x, last_y = x, y
            highest_platform_y = min(highest_platform_y, y)
            skipped_height = 0
        else:
            last_y = y
            highest_platform_y = min(highest_platform_y, y)
            skipped_height = 0
        else:
            last_y = y
            highest_platform_y = min(highest_platform_y, y)

    # Draw everything
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, floor)
    for plat in platforms:
        pygame.draw.rect(screen, GREEN, plat)
        pygame.draw.line(screen, RED, (plat.left, plat.top), (plat.right, plat.top), 2)
    pygame.draw.rect(screen, BLUE, player)
    pygame.draw.line(screen, RED, (player.left, player.bottom), (player.right, player.bottom), 2)

    pygame.display.flip()

pygame.quit()
sys.exit()

