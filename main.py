import pygame
import time
import random

# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (95, 165, 228)
CYAN = (0, 100, 100)
WIDTH = 800
HEIGHT = 800
TPS = 60
TITLE = "Game"

# GLOBAL VARIABLES

all_sprites = pygame.sprite.Group()
obstacle_sprites = pygame.sprite.Group()
lazer_sprites = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

# ----- SCREEN PROPERTIES
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption(TITLE)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("./images/Galaga_ship.png")
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect()

        # Set the initial position of the ship to the center of the screen
        self.rect.center = screen.get_rect().center

        self.x_vel = 7
        self.y_vel = 7

        self.dir = 'u'

    def update(self):
        # If the position is out of bounds, put it back in bounds
        if self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH

        if self.rect.left <= 0:
            self.rect.left = 0

        # Rotate the image in the direction of the last key pressed
        self.image = pygame.image.load("./images/Galaga_ship.png")

        # Rotate the image to the right
        if self.dir == 'r':
            self.image = pygame.transform.rotate(self.image, 270)
        elif self.dir == 'd':
            self.image = pygame.transform.rotate(self.image, 180)
        elif self.dir == 'l':
            self.image = pygame.transform.rotate(self.image, 90)

        # Since the image is still 128x128, scale it down again
        self.image = pygame.transform.scale(self.image, (48, 48))

    # Player-controlled movement
    def move_up(self):
        # Change the player's y velocity
        self.rect.y -= self.y_vel

        # Update self.dir so the update() function can rotate the sprite
        self.dir = 'u'

    def move_down(self):
        self.rect.y += self.y_vel
        self.dir = 'd'

    def move_right(self):
        # Change the player's x vel
        self.rect.x += self.x_vel
        self.dir = 'r'

    def move_left(self):
        self.rect.x -= self.x_vel
        self.dir = 'l'


class Obstacle(pygame.sprite.Sprite):
    # spawn_dir is the border on which the obstacle spawns
    # '1' - spawns on the top, moves towards the bottom
    # '2' - spawns on the bottom, moves towards the top
    # '3' - spawns on the left, moves towards the right
    # '4' - spawns on the right, moves towards the right
    # max_vel is the maximum velocity that the obstacle can have
    def __init__(self, spawn_dir, max_vel):
        super().__init__()

        # Obstacle is a square of size 20x20
        self.image = pygame.Surface((20, 20))
        # Make the rectangle green
        self.image.fill((0, 255, 0))
        
        self.dir = spawn_dir
        
        self.rect = self.image.get_rect()
        self.x_vel = 0
        self.y_vel = 0
        
        # Gets a random velocity from [2, max_vel] (inclusive)
        random_vel = random.randrange(2, max_vel + 1)
        if spawn_dir == 1:
            # Spawns the block somewhere on the top, off the screen
            self.rect.x = random.randrange(0, WIDTH)
            self.rect.y = -30
            
            self.y_vel = random_vel
        elif spawn_dir == 2:
            # Spawns the block somewhere on the bottom
            self.rect.x = random.randrange(0, WIDTH)
            self.rect.y = HEIGHT + 30
            
            self.y_vel = -random_vel
        elif spawn_dir == 3:
            # Spawns the block somewhere on the right
            self.rect.x = -30
            self.rect.y = random.randrange(0, HEIGHT)
            
            self.x_vel = random_vel
        elif spawn_dir == 4:
            # Spawns the block somewhere on the left
            self.rect.x = WIDTH + 30
            self.rect.y = random.randrange(0, HEIGHT)
            
            self.x_vel = -random_vel
            
    def update(self):
        # Update the position of the obstacle
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel
            
            
class Lazer(pygame.sprite.Sprite):
    # Direction: 1 - vertical, 2 - horizontal
    def __init__(self, direction):
        super().__init__()
        self.image = pygame.Surface((0, 0))
        if direction == 1:
            # Make this a horizontal line
            self.image = pygame.Surface((20, HEIGHT))
            self.rect = self.image.get_rect()
            
            # Set a random x-pos
            self.rect.x = random.randrange(0, WIDTH)
        else:
            # Make this a vertical line
            self.image = pygame.Surface((WIDTH, 20))
            self.rect = self.image.get_rect()
            
            # Set a random y-pos
            self.rect.y = random.randrange(0, HEIGHT)
            
        self.image.fill(CYAN)
        self.image.set_alpha(128)
            
        # A variable to check how much time has passed since the lazer was created
        self.tick = 0
        
    def update(self):
        self.tick += 1
        
        # If this object has existed for 2 seconds,
        # Color the object green and add itself to obstacle list
        if self.tick == 2 * TPS:
            self.image.fill((0, 255, 0))
            lazer_sprites.add(self)
            
            # Make the image not transparent
            self.image.set_alpha(255)
        elif self.tick == 3 * TPS:
            # If the object existed for 3 seconds, kill it
            self.kill()
            
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        
        
# A function to write text on the screen
def write_text(text, x, y, font_size):
    font = pygame.font.Font(pygame.font.get_default_font(), font_size)
    text_surface = font.render(text, False, WHITE)
    screen.blit(text_surface, (x, y))


def main():
    pygame.init()

    # ----- LOCAL VARIABLES
    # Player's current score
    score = 0
    done = False
    clock = pygame.time.Clock()

    player = Player()
    all_sprites.add(player)

    # Amount of ticks since the game has started
    ticks = 40 * TPS

    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.move_right()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.move_up()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.move_down()
            
        # Check to see if the user skips the intro
        if keys[pygame.K_ESCAPE] and ticks <= 5 * TPS:
            ticks = 5 * TPS

        # ----- LOGIC

        collided = False
        # Iterate through the list of obstacles
        for obstacle in obstacle_sprites:
            # Check the direction of the obstacle, and kill it if it's off the screen
            if obstacle.dir == 1 and obstacle.rect.top > HEIGHT:
                obstacle.kill()
                score += 1
            elif obstacle.dir == 2 and obstacle.rect.bottom < 0:
                obstacle.kill()
                score += 1
            elif obstacle.dir == 3 and obstacle.rect.left > WIDTH:
                obstacle.kill()
                score += 1
            elif obstacle.dir == 4 and obstacle.rect.right < 0:
                obstacle.kill()
                score += 1

            # Check if any of the obstacles have collided the player's center
            if obstacle.rect.collidepoint(player.rect.center):
                collided = True
                
        # Iterate through the list of lazers to see if any of them have collided w/ plaer
        for lazer in lazer_sprites:
            if lazer.rect.collidepoint(player.rect.center):
                collided = True

        # TODO: when it has collided
        if collided:
            done = True

        # If game has been going on for less than 5 seconds, don't do anything as it is showing the intro
        if ticks < 5 * TPS:
            pass
        # Stage 1: Pretty easy, 2-3 obstacles per wave, waves every 50 ticks, obstacles are the same speed
        # Stage lasts until 20 seconds
        # TPS is ticks per second
        elif ticks < 20 * TPS:
            # Check if ticks is a multiple of 50, so it only does it once every 20 ticks
            if ticks % 50 == 0:
                # Spawn 5 - 7 obstacles
                for i in range(random.randrange(5, 8)):
                    # Create an obstacle Class and add it to the list
                    obstacle = Obstacle(random.randrange(1, 5), 2)
                    all_sprites.add(obstacle)
                    obstacle_sprites.add(obstacle)

        # Stage 2: Normal - 5 - 7 obstacles per wave, waves every 40 ticks, each obstacle varies in speed, from 2 - 4
        # Start spawning lazers at a rate of 1 every 2 seconds
        # Stage lasts until 40 seconds
        elif ticks < 40 * TPS:
            if ticks % 40 == 0:
                # Spawn 5 - 7 obstacles
                for i in range(random.randrange(5, 8)):
                    obstacle = Obstacle(random.randrange(1, 5), 4)
                    all_sprites.add(obstacle)
                    obstacle_sprites.add(obstacle)
            # Spawn the lazers (every 2 seconds)
            if ticks % (2 * TPS) == 0:
                lazer = Lazer(random.randrange(1, 3))
                all_sprites.add(lazer)
            
        # Stage 3: Hard - 6 - 8 obstacles per wave, waves every 30 ticks, each obstacle varies in speed from 2 - 6
        # Spawn a lazer every second
        elif ticks < 70 * TPS:
            if ticks % 30 == 0:
                # Spawns 6 - 8 obstacles
                for i in range(random.randrange(6, 9)):
                    obstacle = Obstacle(random.randrange(1, 5), 6)
                    all_sprites.add(obstacle)
                    obstacle_sprites.add(obstacle)
                    
            # Spawn lazers every second
            if ticks % TPS == 0:
                lazer = Lazer(random.randrange(1, 3))
                all_sprites.add(lazer)

        # Stage 4: Insane - 7-10 obstacles per wave, wave every 25 ticks, obstacles varies in speed from 2 - 10
        else:
            if ticks % 25 == 0:
                # Spawns 7 - 10 obstacles
                for i in range(random.randrange(7, 11)):
                    obstacle = Obstacle(random.randrange(1, 5), 10)
                    all_sprites.add(obstacle)
                    obstacle_sprites.add(obstacle)
                    
            # Spawn 2 lazers every half a second
            if ticks % 30 == 0:
                lazer = Lazer(random.randrange(1, 3))
                all_sprites.add(lazer)
                lazer = Lazer(random.randrange(1, 3))
                all_sprites.add(lazer)

        # ----- DRAW
        screen.fill(BLACK)

        # If less than 300 ticks (5 seconds) have passed, show the intro
        if ticks < 5 * TPS:
            write_text("Use the arrow keys or WASD to move", 50, 50, 30)
            write_text("Try to avoid the obstacles for as long as possible", 50, 100, 30)
            write_text("Your hit-box is the center of the ship -", 50, 150, 30)
            write_text("it is only 1 pixel wide!", 50, 200, 30)
            
            write_text("You get +1 point for every obstacle that goes", 50, 250, 30)
            write_text("off the screen.", 50, 300, 30)
            
            write_text("Press esc to skip this screen...", 50, 500, 30)
        

        # Draw the score
        write_text(f"Score: {score}", 10, 10, 20)
        
        # Display which stage it's on
        stage = ""
        if ticks <= 20 * TPS:
            stage = "Easy"
        elif ticks <= 40 * TPS:
            stage = "Normal"
        elif ticks <= 70 * TPS:
            stage = "Hard"
        else:
            stage = "Insane"
        
        # Draw time passed, rounded to 3, only if time passed >= 5
        if ticks >= 5 * TPS:
            write_text(f"Time survived: {round(ticks / TPS - 5, 2)}", 200, 10, 20)
            write_text("Stage: " + stage, 450, 10, 20)

        all_sprites.update()
        all_sprites.draw(screen)

        # ----- UPDATE
        pygame.display.flip()
        clock.tick(60)
        ticks += 1

    # After the game ended, print the score
    tick = 0
    while True:
        screen.fill(BLACK)
        write_text(f"Your final score is {score}.", 50, 50, 30)
        write_text(f"You survived for {round(ticks / TPS - 5, 2)} seconds.", 50, 100, 30)
        pygame.display.flip()
        tick += 1
        if tick == 5 * TPS:
            break
    pygame.quit()


if __name__ == "__main__":
    main()

