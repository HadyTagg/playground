import pygame
import math
import sys

# --- Config ---
WIDTH, HEIGHT = 800, 600
HEART_DURATION = 10  # seconds
TEXT_DURATION = 5    # seconds
FPS = 60

# --- Initialize ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Love Message")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 60)

# --- Generate heart points ---
def generate_heart_points(scale=10, step=0.01):
    points = []
    t = 0
    while t < 2 * math.pi:
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        points.append((WIDTH // 2 + int(scale * x), HEIGHT // 2 - int(scale * y)))
        t += step
    return points

heart_points = generate_heart_points()
total_points = len(heart_points)
points_per_frame = total_points / (HEART_DURATION * FPS)

# --- Main Loop ---
frame_count = 0
text_shown = False
running = True

while running:
    dt = clock.tick(FPS)
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw heart gradually
    if frame_count < HEART_DURATION * FPS:
        current_index = int(frame_count * points_per_frame)
        for pt in heart_points[:current_index]:
            pygame.draw.circle(screen, (255, 0, 0), pt, 2)
    else:
        # Draw full heart
        for pt in heart_points:
            pygame.draw.circle(screen, (255, 0, 0), pt, 2)
        if not text_shown:
            text_start_frame = frame_count
            text_shown = True

    # Show text after heart is complete
    if text_shown:
        text_surface = font.render("Rosie, I love you", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surface, text_rect)

        # Close after holding text
        if frame_count - text_start_frame >= TEXT_DURATION * FPS:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    frame_count += 1

