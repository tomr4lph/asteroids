from circleshape import CircleShape
from constants import (
     PLAYER_RADIUS,
     LINE_WIDTH,
     PLAYER_TURN_SPEED,
     PLAYER_SPEED,
     PLAYER_SHOOT_SPEED,
     PLAYER_SHOOT_COOLDOWN_SECONDS
     )
import pygame
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cooldown = 0

    # in the Player class
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
            pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt) -> None:
         self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        
        #Left
        if keys[pygame.K_a]:
            self.rotate(-dt)

        #Right
        if keys[pygame.K_d]:
            self.rotate(dt)

        #Forward
        if keys[pygame.K_w]:
            self.move(dt)

        #Backwards
        if keys[pygame.K_s]:
            self.move(-dt)

        #Shoot
        if keys[pygame.K_SPACE]:
            if self.shoot_cooldown <= 0:
                self.shoot()
                self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

        #Reduce the shoot cooldown
        self.shoot_cooldown = max(0, self.shoot_cooldown - dt)

    def move(self, dt: float) -> None:
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self) -> None:
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        print("Shot")

        