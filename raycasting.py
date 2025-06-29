import pygame
import math
pygame.init()

screen = pygame.display.set_mode((1200, 720))
clock = pygame.time.Clock()
running = True

player_pos = pygame.Vector2(300, 180)
linecord = player_pos - pygame.Vector2(0, 60)  

dth = 0.087 / 1.2
player_radius = 10
dt = 0
fov = math.radians(60)  
num_rays = 500         
half_fov = fov / 2
ray_step = fov / num_rays
max_depth = 1000
screen_width = 1200
screen_height = 720

walls = [
    (50, 50, 1100, 20), 
    (50, 650, 1100, 20),  
    (50, 50, 20, 600),  
    (1130, 50, 20, 600), 
    (200, 100, 20, 250),
    (200, 100, 300, 20),
    (500, 100, 20, 300),
    (300, 380, 220, 20),
    (300, 200, 20, 180),
    (100, 150, 80, 20),
    (100, 150, 20, 200),
    (100, 350, 150, 20),
    (250, 250, 20, 120),
    (150, 250, 100, 20),
    (700, 100, 20, 300),
    (700, 100, 200, 20),
    (880, 100, 20, 150),
    (880, 250, 120, 20),
    (800, 250, 80, 20),
    (800, 250, 20, 150),
    (800, 400, 100, 20),
    (400, 200, 100, 100),
    (600, 300, 100, 100),
    (350, 450, 100, 100),
    (750, 450, 100, 100),
    (100, 500, 150, 20),
    (100, 500, 20, 130),
    (250, 550, 20, 80),
    (150, 600, 100, 20),    
    (900, 500, 200, 20),
    (900, 500, 20, 130),
    (1000, 500, 20, 130),
    (900, 600, 100, 20),
    (950, 550, 20, 50),    
    (450, 450, 20, 150),
    (550, 400, 20, 200),
    (650, 450, 20, 150),
    (850, 300, 20, 150),    
    # (250, 300, 40, 40),
    (500, 400, 40, 40),
    (750, 200, 40, 40),
    (1000, 400, 40, 40),
    (300, 550, 40, 40),
]

def line_intersect(p1, p2, q1, q2):
    s = p2 - p1
    r = q2 - q1
    denom = s.cross(r)
    if denom == 0:
        return None
    t = (q1 - p1).cross(r) / denom
    u = (q1 - p1).cross(s) / denom
    if 0 <= t <= 1 and 0 <= u <= 1:
        return p1 + s * t
    return None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((100, 100, 255), rect=(0, 0, screen_width, screen_height // 2))
    screen.fill((50, 50, 50), rect=(0, screen_height // 2, screen_width, screen_height // 2))

    old_x = linecord.x - player_pos.x
    old_y = linecord.y - player_pos.y
    direction = player_pos - linecord

    keys = pygame.key.get_pressed()
    move_vec = pygame.Vector2(0, 0)
    speed = 3000

    if keys[pygame.K_w]:
        move_vec -= direction.normalize() * speed * dt
    if keys[pygame.K_s]:
        move_vec += direction.normalize() * speed * dt
    right_vec = pygame.Vector2(direction.y, -direction.x).normalize()
    if keys[pygame.K_e]:
        move_vec += right_vec * speed * dt
    if keys[pygame.K_q]:
        move_vec -= right_vec * speed * dt
    if keys[pygame.K_d]:
        new_x = old_x * math.cos(dth) - old_y * math.sin(dth)
        new_y = old_x * math.sin(dth) + old_y * math.cos(dth)
        linecord.x = player_pos.x + new_x
        linecord.y = player_pos.y + new_y

    if keys[pygame.K_a]:
        new_x = old_x * math.cos(dth) + old_y * math.sin(dth)
        new_y = -old_x * math.sin(dth) + old_y * math.cos(dth)
        linecord.x = player_pos.x + new_x
        linecord.y = player_pos.y + new_y

    next_pos = player_pos + move_vec * dt
    blocked = False
    
    for wx, wy, ww, wh in walls:
        closest_x = max(wx, min(next_pos.x, wx + ww))
        closest_y = max(wy, min(next_pos.y, wy + wh))
        
        distance = math.sqrt((next_pos.x - closest_x)**2 + (next_pos.y - closest_y)**2)
        
        if distance < player_radius:
            blocked = True
            push_x = next_pos.x - closest_x
            push_y = next_pos.y - closest_y
            push_length = math.sqrt(push_x**2 + push_y**2)
            
            if push_length > 0:
                push_x = push_x / push_length * (player_radius - distance)
                push_y = push_y / push_length * (player_radius - distance)
                
                player_pos.x += push_x
                player_pos.y += push_y
                linecord.x += push_x
                linecord.y += push_y
            break
    
    if not blocked:
        player_pos += move_vec * dt
        linecord += move_vec * dt

    line_vec = linecord - player_pos
    base_angle = math.atan2(line_vec.y, line_vec.x)

    rect_lines = []
    for wx, wy, ww, wh in walls:
        rect_lines.extend([
            (pygame.Vector2(wx, wy), pygame.Vector2(wx + ww, wy)),
            (pygame.Vector2(wx + ww, wy), pygame.Vector2(wx + ww, wy + wh)),
            (pygame.Vector2(wx + ww, wy + wh), pygame.Vector2(wx, wy + wh)),
            (pygame.Vector2(wx, wy + wh), pygame.Vector2(wx, wy)),
        ])

    for i in range(num_rays):
        angle = base_angle - half_fov + i * ray_step
        ray_dir = pygame.Vector2(math.cos(angle), math.sin(angle))
        ray_end = player_pos + ray_dir * max_depth
        hit_point = None
        min_dist = float('inf')
        
        for edge_start, edge_end in rect_lines:
            intersect = line_intersect(player_pos, ray_end, edge_start, edge_end)
            if intersect:
                dist_to_intersect = (intersect - player_pos).length()
                if dist_to_intersect < min_dist:
                    min_dist = dist_to_intersect
                    hit_point = intersect
        
        if hit_point:
            corrected_dist = min_dist * math.cos(angle - base_angle)
            height = min(screen_height, screen_height / (corrected_dist + 0.0001) * 100)
            column_x = i * (screen_width / num_rays)  
            stripe_width = (screen_width / num_rays) + 1
            
            shade = max(50, 255 - corrected_dist * 0.5)
            color = (shade * 0.4, shade * 0.4, shade)
            pygame.draw.rect(screen, color, 
                           (column_x, screen_height // 2 - height // 2, 
                            stripe_width, height))

    scale = 0.25
    for wx, wy, ww, wh in walls:
        pygame.draw.rect(screen, "black", pygame.Rect(wx * scale, wy * scale, ww * scale, wh * scale), width=2)
    pygame.draw.circle(screen, "red", player_pos * scale, int(player_radius * scale))
    pygame.draw.line(screen, "black", player_pos * scale, linecord * scale, 2)  
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()