import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
GRAVITY = 0.5
JUMP_STRENGTH = -8
PIPE_WIDTH = 60
BIRD_X = 50

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)  # Debugging color for hitboxes

# Load assets
bg_img = pygame.image.load("background.png")
bird_img = pygame.image.load("bird.png")
pipe_img = pygame.image.load("pipe.png")

# Resize images
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
bird_img = pygame.transform.scale(bird_img, (40, 30))
pipe_img = pygame.transform.scale(pipe_img, (PIPE_WIDTH, HEIGHT))

# Game window setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Debug mode
DEBUG_MODE = False

# Difficulty settings
DIFFICULTY = "Normal"
DIFFICULTY_SETTINGS = {
    "Easy": {"PIPE_GAP": 200, "PIPE_SPACING": 400, "PIPE_SPEED": 2},
    "Normal": {"PIPE_GAP": 150, "PIPE_SPACING": 350, "PIPE_SPEED": 3},
    "Hard": {"PIPE_GAP": 120, "PIPE_SPACING": 300, "PIPE_SPEED": 4},
}

# Apply chosen difficulty settings
PIPE_GAP = DIFFICULTY_SETTINGS[DIFFICULTY]["PIPE_GAP"]
PIPE_SPACING = DIFFICULTY_SETTINGS[DIFFICULTY]["PIPE_SPACING"]
PIPE_SPEED = DIFFICULTY_SETTINGS[DIFFICULTY]["PIPE_SPEED"]

# Bird class
class Bird:
    def __init__(self):
        self.y = HEIGHT // 2
        self.vel = 0

    def jump(self):
        """Applies an upward force to simulate a jump."""
        self.vel = JUMP_STRENGTH

    def update(self):
        """Applies gravity and updates the bird's position."""
        self.vel += GRAVITY
        self.y += self.vel

    def draw(self):
        """Draws the bird on the screen and optionally the debug hitbox."""
        screen.blit(bird_img, (BIRD_X, self.y))
        if DEBUG_MODE:
            pygame.draw.rect(screen, RED, self.get_hitbox(), 2)

    def get_hitbox(self):
        """Returns the exact rectangular hitbox of the bird."""
        return pygame.Rect(BIRD_X, int(self.y), 40, 30)

# Pipe class
class Pipe:
    def __init__(self, x):
        """Generates a new pipe with a random height while maintaining reasonable variation."""
        self.height = random.randint(100, 400)
        self.x = x

    def move(self):
        """Moves the pipe to the left at a constant speed."""
        self.x -= PIPE_SPEED

    def draw(self):
        """Draws the pipe on the screen and optionally the debug hitbox."""
        top_pipe = pygame.transform.flip(pipe_img, False, True)
        screen.blit(top_pipe, (self.x, self.height - HEIGHT))
        screen.blit(pipe_img, (self.x, self.height + PIPE_GAP))

        if DEBUG_MODE:
            pygame.draw.rect(screen, RED, self.get_top_hitbox(), 2)
            pygame.draw.rect(screen, RED, self.get_bottom_hitbox(), 2)

    def get_top_hitbox(self):
        """Returns the exact rectangular hitbox for the top pipe."""
        return pygame.Rect(self.x, self.height - HEIGHT + PIPE_GAP, PIPE_WIDTH, HEIGHT - PIPE_GAP)

    def get_bottom_hitbox(self):
        """Returns the exact rectangular hitbox for the bottom pipe."""
        return pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP)

    def collide(self, bird_hitbox):
        """Checks if the bird collides with either the top or bottom pipe."""
        return bird_hitbox.colliderect(self.get_top_hitbox()) or bird_hitbox.colliderect(self.get_bottom_hitbox())

# Main game loop
def main():
    """Runs the main game loop, handling events, updates, and rendering."""
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe(WIDTH + i * PIPE_SPACING) for i in range(3)]
    running = True
    score = 0

    while running:
        screen.blit(bg_img, (0, 0))  # Draw background
        bird.update()
        bird.draw()

        # Handle user input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()

        # Update and draw pipes
        for pipe in pipes:
            pipe.move()
            pipe.draw()
            if pipe.collide(bird.get_hitbox()):
                print("Collision detected!")  # Debugging output
                running = False  # End game when collision occurs

            # Remove off-screen pipes and generate new ones
            if pipe.x + PIPE_WIDTH < 0:
                pipes.remove(pipe)
                pipes.append(Pipe(WIDTH))
                score += 1

        # End the game if the bird falls below the screen
        if bird.y > HEIGHT:
            running = False

        pygame.display.update()  # Refresh the screen
        clock.tick(30)  # Limit the frame rate

    pygame.quit()

# Run the game
if __name__ == "__main__":
    main()
