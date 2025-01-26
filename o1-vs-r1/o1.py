import pygame
import pymunk
import pymunk.pygame_util
from pygame.locals import *

# Window dimensions
WIDTH, HEIGHT = 800, 600

def create_triangle(space):
    triangle_points = [(100, 500), (400, 100), (700, 500)]
    static_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Poly(static_body, triangle_points)
    shape.elasticity = 0.9
    shape.friction = 0.5
    # Add both the body and shape to the space
    space.add(static_body, shape)

def create_ball(space, pos, radius=20):
    """
    Create a ball (circle) in the physics space at position 'pos'.
    """
    mass = 1
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.9
    shape.friction = 0.5
    space.add(body, shape)
    return shape

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Triangle with Ball Simulation")

    # Clock to manage frame rate
    clock = pygame.time.Clock()

    # Create pymunk Space
    space = pymunk.Space()
    space.gravity = (0, 900)  # Gravity pulling down (in px/s^2)

    # Draw options for pymunk (to visualize shapes)
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    # Create the triangle boundary
    create_triangle(space)
    
    # Create a single ball inside the triangle
    ball_shape = create_ball(space, pos=(400, 200), radius=20)

    # Main loop
    running = True
    while running:
        clock.tick(60)  # Limit to 60 FPS
        
        for event in pygame.event.get():
            if event.type == QUIT or (
                event.type == KEYDOWN and event.key == K_ESCAPE
            ):
                running = False
                
        # Update the physics simulation
        # (The smaller the dt, the more accurate but the more CPU usage)
        space.step(1/60)
        
        # Clear screen
        screen.fill((255, 255, 255))
        
        # Draw objects
        space.debug_draw(draw_options)
        
        # Flip the screen buffer
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
