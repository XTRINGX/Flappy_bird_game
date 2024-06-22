import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 200
GRAVITY = 0.5
FLAP_STRENGTH = -10

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load images
bird_image = pygame.image.load("images/bird.png")
bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))
background_image = pygame.image.load("images/background.png")
pipe_image = pygame.image.load("images/pipe.png")
pipe_image = pygame.transform.scale(pipe_image, (PIPE_WIDTH, PIPE_HEIGHT))

# Load sounds
flap_sound = pygame.mixer.Sound("sounds/flap.mp3")
hit_sound = pygame.mixer.Sound("sounds/hit.mp3")

# Bird class
class Bird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def draw(self, screen):
        screen.blit(bird_image, (self.x, self.y))

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, 400)
        self.top_pipe = pygame.transform.flip(pipe_image, False, True)
        self.bottom_pipe = pipe_image

    def update(self):
        self.x -= 5

    def draw(self, screen):
        screen.blit(self.top_pipe, (self.x, self.height - PIPE_HEIGHT))
        screen.blit(self.bottom_pipe, (self.x, self.height + PIPE_GAP))

    def collide(self, bird):
        if bird.y < self.height or bird.y + BIRD_HEIGHT > self.height + PIPE_GAP:
            if bird.x + BIRD_WIDTH > self.x and bird.x < self.x + PIPE_WIDTH:
                return True
        return False
    
    # Function to restart the game
def restart_game():
    global score
    bird.x = 100
    bird.y = SCREEN_HEIGHT // 2
    bird.velocity = 0
    pipes.clear()
    pipes.extend([Pipe(SCREEN_WIDTH + i * 300) for i in range(3)])
    score = 0

# Main game loop
def main():
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + i * 300) for i in range(3)]
    clock = pygame.time.Clock()
    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()
                    flap_sound.play()

        bird.update()

        for pipe in pipes:
            pipe.update()
            if pipe.x + PIPE_WIDTH < 0:
                pipes.remove(pipe)
                pipes.append(Pipe(SCREEN_WIDTH + 300))
                score += 1

        for pipe in pipes:
            if pipe.collide(bird):
                hit_sound.play()
                running = False

        if bird.y > SCREEN_HEIGHT or bird.y < 0:
            running = False

        screen.blit(background_image, (0, 0))
        bird.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)

        score_text = pygame.font.SysFont("Arial", 36).render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Game over screen
    game_over_text = pygame.font.SysFont("Arial", 48).render("Game Over", True, (255, 0, 0))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
    restart_text = pygame.font.SysFont("Arial", 24).render("Press R to restart", True, (255, 255, 255))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50))
    pygame.display.flip()

    # Wait for user input to restart or quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game()
                    main()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

if __name__ == "__main__":
    main()
