import pygame
import sys
import math

def main():
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Ball inside Triangle Simulation -- O3 Mini High")
    clock = pygame.time.Clock()

    # Define the triangle vertices (in a clockwise or counterclockwise order)
    triangle = [(100, 500), (700, 500), (400, 100)]
    
    # Compute the centroid of the triangle (used to determine the inward normals)
    centroid = (sum(x for x, y in triangle) / 3, sum(y for x, y in triangle) / 3)

    # Precompute the triangle edges and their inward normals.
    # For each edge (from P1 to P2) we compute two candidate normals.
    # We choose the one that points toward the interior (i.e. toward the centroid).
    edges = []
    for i in range(len(triangle)):
        P1 = triangle[i]
        P2 = triangle[(i + 1) % len(triangle)]
        dx = P2[0] - P1[0]
        dy = P2[1] - P1[1]
        # Two candidates: rotate the edge vector 90° clockwise and counterclockwise.
        candidate1 = (dy, -dx)
        candidate2 = (-dy, dx)
        # Choose the candidate that points toward the centroid.
        mid = ((P1[0] + P2[0]) / 2, (P1[1] + P2[1]) / 2)
        vec_to_centroid = (centroid[0] - mid[0], centroid[1] - mid[1])
        dot1 = candidate1[0] * vec_to_centroid[0] + candidate1[1] * vec_to_centroid[1]
        dot2 = candidate2[0] * vec_to_centroid[0] + candidate2[1] * vec_to_centroid[1]
        n = candidate1 if dot1 > dot2 else candidate2
        # Normalize the chosen normal
        norm = math.hypot(n[0], n[1])
        if norm != 0:
            n = (n[0] / norm, n[1] / norm)
        else:
            n = (0, 0)
        edges.append((P1, P2, n))
    
    # Define the ball properties.
    ball_radius = 15
    ball_pos = [400, 300]  # starting at the center of the window
    ball_vel = [200, 150]  # pixels per second

    running = True
    while running:
        # Limit the frame rate and compute the elapsed time in seconds.
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update ball position based on its velocity.
        ball_pos[0] += ball_vel[0] * dt
        ball_pos[1] += ball_vel[1] * dt

        # Check for collisions with each edge of the triangle.
        for P1, P2, n in edges:
            # Compute the (signed) distance from the ball center to the edge,
            # along the inward normal direction.
            d = (ball_pos[0] - P1[0]) * n[0] + (ball_pos[1] - P1[1]) * n[1]
            # If the ball is closer to the edge than its radius, it has collided.
            if d < ball_radius:
                # Only reflect if the ball is moving toward the edge.
                vel_dot_n = ball_vel[0] * n[0] + ball_vel[1] * n[1]
                if vel_dot_n < 0:
                    # Reflect the velocity: v' = v - 2*(v·n)*n.
                    ball_vel[0] = ball_vel[0] - 2 * vel_dot_n * n[0]
                    ball_vel[1] = ball_vel[1] - 2 * vel_dot_n * n[1]
                    # Push the ball out of the wall so it no longer overlaps.
                    overlap = ball_radius - d
                    ball_pos[0] += overlap * n[0]
                    ball_pos[1] += overlap * n[1]

        # Drawing section:
        screen.fill((30, 30, 30))  # dark background
        
        # Draw the filled triangle.
        pygame.draw.polygon(screen, (0, 128, 255), triangle)
        
        # Draw the ball.
        pygame.draw.circle(screen, (255, 100, 0), (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
