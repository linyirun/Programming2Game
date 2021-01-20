import pygame

# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (95, 165, 228)
WIDTH = 800
HEIGHT = 600
TITLE = "Game"

all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
projectiles = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("./images/Galaga_ship.png")
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.center = (100, 100)

        self.x_vel = 3
        self.y_vel = 3

    def update(self):
        # Update the position
        # self.rect.x += self.x_vel
        # self.rect.y += self.y_vel

        # If the position is out of bounds, put it back in bounds
        if self.rect.top + self.y_vel <= 0:
            self.rect.top = 0

        if self.rect.bottom + self.y_vel >= HEIGHT:
            self.rect.bottom = HEIGHT

        if self.rect.right + self.x_vel >= WIDTH:
            self.rect.right = WIDTH

        if self.rect.left + self.x_vel <= 0:
            self.rect.left = 0

    # Player-controlled movement

    def move_up(self):
        # Change the player's y velocity
        self.rect.y += self.y_vel

    def move_down(self):
        self.rect.y -= self.y_vel

    def move_right(self):
        # Change the player's x vel
        self.rect.x += self.x_vel

    def move_left(self):
        self.rect.x -= self.x_vel

    # Some functions to stop the x and y vels
    def stop_x(self):
        self.x_vel = 0

    def stop_y(self):
        self.y_vel = 0

    def shoot(self):
        # Shoots a projectile
        pass


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()


def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()

    player = Player()
    all_sprites.add(player)
    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True



        # ----- LOGIC

        # ----- DRAW
        screen.fill(BLACK)
        all_sprites.update()
        all_sprites.draw(screen)

        # ----- UPDATE
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
