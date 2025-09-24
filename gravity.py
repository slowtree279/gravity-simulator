import pygame
import math
import sys

pygame.init()

WIDTH, HEIGHT = 1200, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Simulator: Center on Heaviest Body")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
RED = (255, 69, 0)
GRAY = (180, 180, 180)
YELLOW = (255, 255, 102)
ORANGE = (255, 165, 0)

font = pygame.font.SysFont("Arial", 18)

G = 0.1  

planets = {
    "Earth": {"radius": 30, "mass": 1000, "color": BLUE},
    "Mars": {"radius": 20, "mass": 338, "color": RED},
    "Moon": {"radius": 15, "mass": 73, "color": GRAY},
    "Sun": {"radius": 50, "mass": 1989000, "color": ORANGE},
}

obj_radius = 12

clock = pygame.time.Clock()
FPS = 60
dt = 0.5

mode = "choose_central_planet"

bodies = []  # list of dicts: pos, vel, mass, radius, color, type, name(optional)

obj_mass_str = ""
obj_mass = None
placing_planet_type = None  # if user chooses to place planet object

def draw_text(text, x, y, color=WHITE):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def compute_forces():
    # Reset forces
    forces = [ [0, 0] for _ in bodies ]
    
    # Calculate gravitational force between every pair
    for i, body_i in enumerate(bodies):
        for j, body_j in enumerate(bodies):
            if i == j:
                continue
            dx = body_j['pos'][0] - body_i['pos'][0]
            dy = body_j['pos'][1] - body_i['pos'][1]
            dist_sq = dx * dx + dy * dy
            dist = math.sqrt(dist_sq)
            if dist < 1:
                dist = 1  # avoid too large forces
            
            force_mag = G * body_i['mass'] * body_j['mass'] / dist_sq
            force_x = force_mag * dx / dist
            force_y = force_mag * dy / dist
            
            forces[i][0] += force_x
            forces[i][1] += force_y
    return forces

def update_bodies(forces):
    for i, body in enumerate(bodies):
        
        ax = forces[i][0] / body['mass']
        ay = forces[i][1] / body['mass']

      
        body['vel'][0] += ax * dt
        body['vel'][1] += ay * dt

        max_vel = 100
        body['vel'][0] = max(-max_vel, min(max_vel, body['vel'][0]))
        body['vel'][1] = max(-max_vel, min(max_vel, body['vel'][1]))

      
        body['pos'][0] += body['vel'][0] * dt
        body['pos'][1] += body['vel'][1] * dt

def reset_sim():
    global mode, bodies, obj_mass_str, obj_mass, placing_planet_type
    mode = "choose_central_planet"
    bodies = []
    obj_mass_str = ""
    obj_mass = None
    placing_planet_type = None

def main():
    global mode, bodies, obj_mass_str, obj_mass, placing_planet_type

    reset_sim()

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if mode == "choose_central_planet":
                    if event.key == pygame.K_1:
                        pdata = planets["Earth"]
                        # Place central planet in center with zero velocity
                        bodies = [{
                            'pos': [WIDTH // 2, HEIGHT // 2],
                            'vel': [0, 0],
                            'mass': pdata['mass'],
                            'radius': pdata['radius'],
                            'color': pdata['color'],
                            'type': 'planet',
                            'name': 'Earth (central)'
                        }]
                        mode = "choose_object_type"
                    elif event.key == pygame.K_2:
                        pdata = planets["Mars"]
                        bodies = [{
                            'pos': [WIDTH // 2, HEIGHT // 2],
                            'vel': [0, 0],
                            'mass': pdata['mass'],
                            'radius': pdata['radius'],
                            'color': pdata['color'],
                            'type': 'planet',
                            'name': 'Mars (central)'
                        }]
                        mode = "choose_object_type"
                    elif event.key == pygame.K_3:
                        pdata = planets["Moon"]
                        bodies = [{
                            'pos': [WIDTH // 2, HEIGHT // 2],
                            'vel': [0, 0],
                            'mass': pdata['mass'],
                            'radius': pdata['radius'],
                            'color': pdata['color'],
                            'type': 'planet',
                            'name': 'Moon (central)'
                        }]
                        mode = "choose_object_type"
                    elif event.key == pygame.K_4:
                        pdata = planets["Sun"]
                        bodies = [{
                            'pos': [WIDTH // 2, HEIGHT // 2],
                            'vel': [0, 0],
                            'mass': pdata['mass'],
                            'radius': pdata['radius'],
                            'color': pdata['color'],
                            'type': 'planet',
                            'name': 'Sun (central)'
                        }]
                        mode = "choose_object_type"

                elif mode == "choose_object_type":
                    if event.key == pygame.K_1:
                        mode = "enter_object_mass"
                        obj_mass_str = ""
                        obj_mass = None
                        placing_planet_type = None
                    elif event.key == pygame.K_2:
                        mode = "choose_planet_object_type"
                        placing_planet_type = None
                    elif event.key == pygame.K_ESCAPE:
                        reset_sim()

                elif mode == "enter_object_mass":
                    if event.key == pygame.K_RETURN:
                        try:
                            val = float(obj_mass_str)
                            if val > 0:
                                obj_mass = val
                                mode = "place_objects"
                            else:
                                obj_mass_str = ""
                        except:
                            obj_mass_str = ""
                    elif event.key == pygame.K_BACKSPACE:
                        obj_mass_str = obj_mass_str[:-1]
                    else:
                        if event.unicode.isdigit() or event.unicode == '.':
                            obj_mass_str += event.unicode
                    if event.key == pygame.K_ESCAPE:
                        mode = "choose_object_type"

                elif mode == "choose_planet_object_type":
                    if event.key == pygame.K_1:
                        placing_planet_type = "Earth"
                        mode = "place_objects"
                    elif event.key == pygame.K_2:
                        placing_planet_type = "Mars"
                        mode = "place_objects"
                    elif event.key == pygame.K_3:
                        placing_planet_type = "Moon"
                        mode = "place_objects"
                    elif event.key == pygame.K_4:
                        placing_planet_type = "Sun"
                        mode = "place_objects"
                    elif event.key == pygame.K_ESCAPE:
                        mode = "choose_object_type"

                elif mode == "place_objects":
                    if event.key == pygame.K_ESCAPE:
                        if len(bodies) > 1:
                            mode = "simulate"
                        else:
                            print("Place at least one object before starting simulation.")

                elif mode == "simulate":
                    if event.key == pygame.K_ESCAPE:
                        reset_sim()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mode == "place_objects":
                    pos = list(event.pos)
                    # Find heaviest body and its position
                    heaviest_body = max(bodies, key=lambda b: b['mass'])
                    hx, hy = heaviest_body['pos']

                    # Calculate relative position to heaviest body
                    rel_x = pos[0] - hx
                    rel_y = pos[1] - hy

                    r = math.hypot(rel_x, rel_y)
                    if r == 0:
                        r = 0.1

                    # Velocity perpendicular to radius vector, magnitude for circular orbit
                    v = math.sqrt(G * heaviest_body['mass'] / r)
                    vel_x = rel_y / r * v
                    vel_y = -rel_x / r * v

                    if placing_planet_type:
                        pdata = planets[placing_planet_type]
                        bodies.append({
                            'pos': [pos[0], pos[1]],
                            'vel': [vel_x, vel_y],
                            'mass': pdata['mass'],
                            'radius': pdata['radius'],
                            'color': pdata['color'],
                            'type': 'planet',
                            'name': placing_planet_type
                        })
                    else:
                        bodies.append({
                            'pos': [pos[0], pos[1]],
                            'vel': [vel_x, vel_y],
                            'mass': obj_mass,
                            'radius': obj_radius,
                            'color': YELLOW,
                            'type': 'mass_object',
                            'name': 'Custom mass object'
                        })

       
        if mode == "choose_central_planet":
            draw_text("Choose Central Planet:", 10, 10)
            draw_text("1. Earth", 10, 40, BLUE)
            draw_text("2. Mars", 10, 70, RED)
            draw_text("3. Moon", 10, 100, GRAY)
            draw_text("4. Sun", 10, 130, ORANGE)

        elif mode == "choose_object_type":
            draw_text("Place Objects Around Central Planet:", 10, 10)
            draw_text("1. Place your own mass object", 10, 40)
            draw_text("2. Place another planet as object", 10, 70)
            draw_text("ESC to reset simulation", 10, 100)

        elif mode == "enter_object_mass":
            draw_text("Enter mass of your object:", 10, 10)
            draw_text(obj_mass_str, 10, 40)
            draw_text("Press Enter to confirm, ESC to go back", 10, 70)

        elif mode == "choose_planet_object_type":
            draw_text("Choose Planet to place as object:", 10, 10)
            draw_text("1. Earth", 10, 40, BLUE)
            draw_text("2. Mars", 10, 70, RED)
            draw_text("3. Moon", 10, 100, GRAY)
            draw_text("4. Sun", 10, 130, ORANGE)
            draw_text("ESC to go back", 10, 170)

        elif mode == "place_objects":
            draw_text("Click to place objects orbiting central planet", 10, 10)
            draw_text("ESC to start simulation (must place >=1 object)", 10, 40)
            if placing_planet_type:
                draw_text(f"Placing planet: {placing_planet_type}", 10, 70, planets[placing_planet_type]['color'])
            else:
                draw_text(f"Placing custom mass object: mass = {obj_mass}", 10, 70, YELLOW)

        elif mode == "simulate":
            draw_text("Simulation running. Press ESC to reset simulation.", 10, 10)

        if mode == "simulate":
            forces = compute_forces()
            update_bodies(forces)

        # Find the heaviest body to center the view on it
        if len(bodies) > 0:
            heaviest_body = max(bodies, key=lambda b: b['mass'])
            center_x, center_y = heaviest_body['pos']
        else:
            center_x, center_y = WIDTH // 2, HEIGHT // 2

        # Draw bodies relative to heaviest body's position (center screen)
        for body in bodies:
            draw_x = int(WIDTH // 2 + (body['pos'][0] - center_x))
            draw_y = int(HEIGHT // 2 + (body['pos'][1] - center_y))
            pygame.draw.circle(screen, body['color'], (draw_x, draw_y), body['radius'])

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

