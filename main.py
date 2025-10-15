# main.py
# Dodge the Falling Blocks - simple pygame game
# Controls: ← and → to move. Space to restart after game over. Esc to quit.

import pygame
import random
import sys

# --- Constants
WIDTH, HEIGHT = 640, 480
FPS = 60
PLAYER_SIZE = 50
PLAYER_SPEED = 6
BLOCK_MIN_SIZE = 20
BLOCK_MAX_SIZE = 60
BLOCK_SPEED_MIN = 3
BLOCK_SPEED_MAX = 8
SPAWN_EVENT = pygame.USEREVENT + 1
SPAWN_INTERVAL_MS = 700  # milliseconds between new blocks

# --- Initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Falling Blocks")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# --- Game objects
class Player:
    def __init__(self):
        self.rect = pygame.Rect((WIDTH - PLAYER_SIZE) // 2,
                                HEIGHT - PLAYER_SIZE - 10,
                                PLAYER_SIZE, PLAYER_SIZE)
        self.speed = PLAYER_SPEED

    def move(self, dx):
        self.rect.x += dx * self.speed
        # keep on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def draw(self, surf):
        pygame.draw.rect(surf, (30, 200, 50), self.rect)

class Block:
    def __init__(self):
        self.w = random.randint(BLOCK_MIN_SIZE, BLOCK_MAX_SIZE)
        self.h = random.randint(BLOCK_MIN_SIZE, BLOCK_MAX_SIZE)
        self.x = random.randint(0, WIDTH - self.w)
        self.y = -self.h
        self.speed = random.randint(BLOCK_SPEED_MIN, BLOCK_SPEED_MAX)
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.color = (200, 30, 30)

    def update(self):
        self.rect.y += self.speed

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)

def draw_text_center(surf, text, y, color=(255,255,255)):
    img = font.render(text, True, color)
    rect = img.get_rect(center=(WIDTH//2, y))
    surf.blit(img, rect)

# --- Game loop / logic
def run_game():
    player = Player()
    blocks = []
    score = 0
    running = True
    game_over = False

    pygame.time.set_timer(SPAWN_EVENT, SPAWN_INTERVAL_MS)

    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == SPAWN_EVENT and not game_over:
                blocks.append(Block())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
                if event.key == pygame.K_SPACE and game_over:
                    # restart
                    return True  # signal restart

        keys = pygame.key.get_pressed()
        if not game_over:
            dx = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx = -1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx = 1
            player.move(dx)

            # update blocks
            for b in blocks:
                b.update()

            # remove off-screen blocks and increase score
            before = len(blocks)
            blocks = [b for b in blocks if b.rect.top <= HEIGHT]
            removed = before - len(blocks)
            if removed:
                score += removed * 10

            # collision check
            for b in blocks:
                if player.rect.colliderect(b.rect):
                    game_over = True
                    break

        # draw
        screen.fill((18, 18, 30))  # background
        player.draw(screen)
        for b in blocks:
            b.draw(screen)

        # HUD
        draw_text_center(screen, f"Score: {score}", 20)
        if game_over:
            draw_text_center(screen, "GAME OVER", HEIGHT//2 - 20, color=(255,200,200))
            draw_text_center(screen, "Press SPACE to restart or ESC to quit", HEIGHT//2 + 20, color=(200,200,200))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

# Main entry - allow restarting
if __name__ == "__main__":
    while True:
        restart = run_game()
        if not restart:
            break
