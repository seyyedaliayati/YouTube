import pygame
import math
import sys

def compute_normals(vertices):
    normals = []
    for i in range(3):
        A = vertices[i]
        B = vertices[(i+1)%3]
        C = vertices[(i+2)%3]

        M = ((A[0] + B[0])/2, (A[1] + B[1])/2)
        MC = (C[0] - M[0], C[1] - M[1])

        edge_vec = (B[0] - A[0], B[1] - A[1])
        perp = (-edge_vec[1], edge_vec[0])

        dot = perp[0] * MC[0] + perp[1] * MC[1]
        if dot < 0:
            perp = (-perp[0], -perp[1])

        length = math.hypot(perp[0], perp[1])
        if length == 0:
            normals.append((0, 0))
        else:
            normals.append((perp[0]/length, perp[1]/length))
    return normals

def distance_to_segment(P, A, B):
    ax, ay = A
    bx, by = B
    px, py = P

    abx, aby = bx - ax, by - ay
    apx, apy = px - ax, py - ay

    dot = apx * abx + apy * aby
    ab_len_sq = abx**2 + aby**2

    if ab_len_sq == 0:
        return math.hypot(apx, apy), A

    t = max(0, min(1, dot / ab_len_sq))
    closest_x = ax + t * abx
    closest_y = ay + t * aby

    dx = px - closest_x
    dy = py - closest_y
    return math.hypot(dx, dy), (closest_x, closest_y)

# Initialize Pygame
pygame.init()
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball in Triangle -- DeepSeek R1")

# Triangle vertices
vertices = [(100, 500), (500, 500), (300, 100)]
normals = compute_normals(vertices)

# Ball setup
ball_radius = 20
ball_color = (255, 0, 0)
centroid_x = sum(v[0] for v in vertices) / 3
centroid_y = sum(v[1] for v in vertices) / 3
ball_x, ball_y = centroid_x, centroid_y
ball_dx, ball_dy = 3, 3

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update ball position
    ball_x += ball_dx
    ball_y += ball_dy

    # Collision detection and response
    collision = False
    for i in range(3):
        A = vertices[i]
        B = vertices[(i+1)%3]
        dist, closest = distance_to_segment((ball_x, ball_y), A, B)
        if dist <= ball_radius:
            normal = normals[i]
            dot = ball_dx * normal[0] + ball_dy * normal[1]
            ball_dx -= 2 * dot * normal[0]
            ball_dy -= 2 * dot * normal[1]
            ball_x, ball_y = closest[0] + normal[0] * ball_radius, closest[1] + normal[1] * ball_radius
            collision = True
            break

    # Rendering
    screen.fill((255, 255, 255))
    pygame.draw.polygon(screen, (0, 0, 255), vertices)
    pygame.draw.circle(screen, ball_color, (int(ball_x), int(ball_y)), ball_radius)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()