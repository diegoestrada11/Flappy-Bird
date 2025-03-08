import pygame
import random

# Initialize Pygame
pygame.init()

# Constants 
WIDTH, HEIGHT = 400, 600  # Game window dimensions
GRAVITY = 0.5  # Gravity applied to the bird
JUMP_STRENGTH = -8  # Upward velocity when jumping
PIPE_GAP = 300  # Vertical gap between pipes
PIPE_WIDTH = 60  # Width of the pipes
PIPE_SPACING = 1000 # Horizontal distance between pipes
PIPE_SPEED = 3  # Speed at which pipes move left 
BIRD_X = 50  # Fixed horizontal position of the bird

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)  # Debugging color for hitboxes

# Load assets
bg_img = pygame.image.load("background.png")  
bird_img = pygame.image.load("bird.png")  
pipe_img = pygame.image.load("pipe.png")  

# Resize images to fit the game window
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
bird_img = pygame.transform.scale(bird_img, (40, 30))
pipe_img = pygame.transform.scale(pipe_img, (PIPE_WIDTH, HEIGHT))

# Game window setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Enable debug mode to visualize hitboxes
DEBUG_MODE = True  # Set to False to disable red hitbox visualization

# Bird class
class Bird:
    def __init__(self):
        self.y = HEIGHT // 2  # Start position in the middle of the screen
        self.vel = 0  # Initial velocity
        self.radius = 15  # Radius for debugging hitbox (circular)

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
            # Draw a red circle around the bird for debugging collision
            pygame.draw.circle(screen, RED, (BIRD_X + 20, int(self.y) + 15), self.radius, 2)

    def get_hitbox(self):
        """Returns the exact rectangular hitbox of the bird."""
        return pygame.Rect(BIRD_X, self.y, 40, 30)

# Pipe class
class Pipe:
    def __init__(self, x, previous_height=None):
        """Generates a new pipe with a random height while maintaining reasonable variation."""
        while True:
            self.height = random.randint(120, 380)
            if previous_height is None or abs(self.height - previous_height) > 120:
                break
        self.x = x  # Set the pipe's initial horizontal position

    def move(self):
        """Moves the pipe to the left at a constant speed."""
        self.x -= PIPE_SPEED

    def draw(self):
        """Draws the pipe on the screen and optionally the debug hitbox."""
        # Draw the top pipe (flipped upside down)
        top_pipe = pygame.transform.flip(pipe_img, False, True)
        screen.blit(top_pipe, (self.x, self.height - HEIGHT))
        # Draw the bottom pipe
        screen.blit(pipe_img, (self.x, self.height + PIPE_GAP))

        if DEBUG_MODE:
            # Draw hitboxes around the pipes for collision debugging
            pygame.draw.rect(screen, RED, self.get_top_hitbox(), 2)
            pygame.draw.rect(screen, RED, self.get_bottom_hitbox(), 2)

    def get_top_hitbox(self):
        """Returns the exact rectangular hitbox for the top pipe."""
        return pygame.Rect(self.x, self.height - HEIGHT, PIPE_WIDTH, HEIGHT)

    def get_bottom_hitbox(self):
        """Returns the exact rectangular hitbox for the bottom pipe."""
        return pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT)

    def collide(self, bird_hitbox):
        """Checks if the bird collides with either the top or bottom pipe."""
        if bird_hitbox.colliderect(self.get_top_hitbox()) or bird_hitbox.colliderect(self.get_bottom_hitbox()):
            print("Collision detected!")  # Debugging message
            return True
        return False

# Main game loop
def main():
    """Runs the main game loop, handling events, updates, and rendering."""
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe(WIDTH + i * PIPE_SPACING) for i in range(3)]  # Generate initial pipes
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
                running = False  # End game when collision occurs

            # Remove off-screen pipes and generate new ones
            if pipe.x + PIPE_WIDTH < 0:
                pipes.remove(pipe)
                new_pipe = Pipe(WIDTH, pipes[-1].height if pipes else None)
                pipes.append(new_pipe)
                score += 1  # Increment score when passing a pipe

        # End the game if the bird falls below the screen
        if bird.y > HEIGHT:
            running = False

        pygame.display.update()  # Refresh the screen
        clock.tick(30)  # Limit the frame rate to 30 FPS

    pygame.quit()

# Run the game
if __name__ == "__main__":
    main()
