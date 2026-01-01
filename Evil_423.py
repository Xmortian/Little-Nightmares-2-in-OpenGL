from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
import math
import random

# --- Global Variables ---
camera_pos = [0, -450, 350]
camera_pan = 0 
char_pos = [0, 0, 0]
char_rotation = 0
flashlight_on = True
gun_visible = False

# Game State
ammo_count = 10
bullets = [] 
ammo_pickups = []
mannequins = []
furniture = [] 
walls = []  
mannequins_killed = 0
mannequins_spawned = 0
spawn_timer = 0
door_visible = False
door_pos = [0, 0, 0]
game_won = False
game_over = False
lives = 5
damage_flash_timer = 0
girl_pos = [0, 0, 0]

PICKUP_COUNT = 5
PICKUP_RADIUS = 50 
MANNEQUIN_COUNT = 10
MANNEQUIN_SPEED = 0.8 # Slower speed
MAP_SIZE = 1200

def init_game():
    global camera_pos, char_pos, char_rotation, ammo_count, bullets, ammo_pickups
    global mannequins, mannequins_killed, door_visible, game_won, furniture
    global mannequins_spawned, spawn_timer, game_over, lives, damage_flash_timer, camera_pan, flashlight_on, walls
    
    random.seed(423)
    camera_pos = [0, -450, 350]
    camera_pan = 0
    flashlight_on = True
    char_pos = [0, 0, 0]
    char_rotation = -90  # Facing South/Camera at start
    ammo_count = 10
    mannequins_killed = 0
    mannequins_spawned = 0
    spawn_timer = 0
    door_visible = False
    game_won = False
    game_over = False
    lives = 5
    damage_flash_timer = 0
    bullets = []
    mannequins = [] # Start empty, spawn sequentially
    
    # Init House Furniture 
    furniture = []

    # Room 1: Top Right area
    furniture.append({'type': 'sofa', 'pos': [500, 500, 0], 'rot': 0, 'size': [250, 100, 60]})
    furniture.append({'type': 'almirah', 'pos': [1000, 1000, 0], 'rot': 45, 'size': [120, 80, 250]})
    # Room 2: Top Left area
    furniture.append({'type': 'sofa', 'pos': [-500, 500, 0], 'rot': 90, 'size': [250, 100, 60]})
    furniture.append({'type': 'almirah', 'pos': [-1000, 200, 0], 'rot': 0, 'size': [120, 80, 250]})
    # Room 3: Bottom Left area
    furniture.append({'type': 'sofa', 'pos': [-600, -600, 0], 'rot': 180, 'size': [250, 100, 60]})
    furniture.append({'type': 'almirah', 'pos': [-200, -1000, 0], 'rot': 90, 'size': [120, 80, 250]})
    # Room 4: Bottom Right area
    furniture.append({'type': 'sofa', 'pos': [600, -600, 0], 'rot': -90, 'size': [250, 100, 60]})
    furniture.append({'type': 'almirah', 'pos': [1000, -200, 0], 'rot': 180, 'size': [120, 80, 250]})
    
    #Furniture for density
    furniture.append({'type': 'sofa', 'pos': [0, 800, 0], 'rot': 0, 'size': [250, 100, 60]})
    furniture.append({'type': 'sofa', 'pos': [0, -800, 0], 'rot': 180, 'size': [250, 100, 60]})
    furniture.append({'type': 'almirah', 'pos': [-800, 0, 0], 'rot': 90, 'size': [120, 80, 250]})
    furniture.append({'type': 'almirah', 'pos': [800, 0, 0], 'rot': -90, 'size': [120, 80, 250]})
    
    # East Side
    furniture.append({'type': 'bed', 'pos': [1100, 450, 0], 'rot': 180, 'size': [200, 120, 50]})
    furniture.append({'type': 'sofa', 'pos': [1100, 150, 0], 'rot': 90, 'size': [200, 100, 60]})
    
    # West Side
    furniture.append({'type': 'bed', 'pos': [-1100, -450, 0], 'rot': 0, 'size': [200, 120, 50]})
    furniture.append({'type': 'sofa', 'pos': [-1100, -150, 0], 'rot': -90, 'size': [200, 100, 60]})
    
    # Add Flower Vases
    furniture.append({'type': 'vase', 'pos': [1000, -1000, 0], 'rot': 0, 'size': [40, 40, 100]})
    furniture.append({'type': 'vase', 'pos': [-1000, 1000, 0], 'rot': 0, 'size': [40, 40, 100]})
    furniture.append({'type': 'vase', 'pos': [1000, 1000, 0], 'rot': 0, 'size': [40, 40, 100]})
    furniture.append({'type': 'vase', 'pos': [-1000, -1000, 0], 'rot': 0, 'size': [40, 40, 100]})
    furniture.append({'type': 'vase', 'pos': [0, 1050, 0], 'rot': 0, 'size': [40, 40, 100]})
    
    # Add Staircase 
    furniture.append({'type': 'staircase', 'pos': [-1150, 800, 0], 'rot': 90, 'size': [300, 200, 200]})
    
    # Dining Table
    table_pos = [800, -700, 0]
    furniture.append({'type': 'dining_table', 'pos': table_pos, 'rot': 90, 'size': [250, 150, 75]})
    # Chairs around table
    furniture.append({'type': 'chair', 'pos': [table_pos[0]-100, table_pos[1], 0], 'rot': 90, 'size': [40, 40, 90]})
    furniture.append({'type': 'chair', 'pos': [table_pos[0]+100, table_pos[1], 0], 'rot': -90, 'size': [40, 40, 90]})
    furniture.append({'type': 'chair', 'pos': [table_pos[0], table_pos[1]-60, 0], 'rot': 0, 'size': [40, 40, 90]})
    furniture.append({'type': 'chair', 'pos': [table_pos[0], table_pos[1]+60, 0], 'rot': 180, 'size': [40, 40, 90]})
    
    # Dining Chandelier (Above table)
    furniture.append({'type': 'dining_chandelier', 'pos': [800, -700, 250], 'rot': 0, 'size': [100, 100, 100]})

    # Init Internal Walls 
    walls = []
    door_width = 200  # Wider doors for easier passage
    wall_thickness = 20
    door_spacing = 400  # Distance from center to each door

    # Top section (above both doors)
    walls.append({
        'x1': -wall_thickness/2, 'y1': door_spacing + door_width/2, 'x2': wall_thickness/2, 'y2': MAP_SIZE,
        'is_door': False
    })
    # Middle section (between the two doors)
    walls.append({
        'x1': -wall_thickness/2, 'y1': -door_spacing - door_width/2, 'x2': wall_thickness/2, 'y2': -door_spacing + door_width/2,
        'is_door': False
    })
    walls.append({
        'x1': -wall_thickness/2, 'y1': door_spacing - door_width/2, 'x2': wall_thickness/2, 'y2': door_spacing + door_width/2,
        'is_door': False
    })
    # Bottom section (below both doors)
    walls.append({
        'x1': -wall_thickness/2, 'y1': -MAP_SIZE, 'x2': wall_thickness/2, 'y2': -door_spacing - door_width/2,
        'is_door': False
    })
    
    # Horizontal wall (East-West) with 2 doors
    # Right section (beyond both doors)
    walls.append({
        'x1': door_spacing + door_width/2, 'y1': -wall_thickness/2, 'x2': MAP_SIZE, 'y2': wall_thickness/2,
        'is_door': False
    })
    # Middle section (between the two doors)
    walls.append({
        'x1': -door_spacing - door_width/2, 'y1': -wall_thickness/2, 'x2': -door_spacing + door_width/2, 'y2': wall_thickness/2,
        'is_door': False
    })
    walls.append({
        'x1': door_spacing - door_width/2, 'y1': -wall_thickness/2, 'x2': door_spacing + door_width/2, 'y2': wall_thickness/2,
        'is_door': False
    })
    # Left section (beyond both doors)
    walls.append({
        'x1': -MAP_SIZE, 'y1': -wall_thickness/2, 'x2': -door_spacing - door_width/2, 'y2': wall_thickness/2,
        'is_door': False
    })

    # Init Pickups
    ammo_pickups = []
    for _ in range(PICKUP_COUNT):
        ammo_pickups.append({
            'pos': [random.uniform(-MAP_SIZE, MAP_SIZE), random.uniform(-MAP_SIZE, MAP_SIZE), 10],
            'rotation': 0
        })

# Call init once at start
init_game()

def draw_text(x, y, text):
    glColor3f(0.7, 0.7, 0.7)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_mannequin(m):
    glPushMatrix()
    glTranslatef(m['pos'][0], m['pos'][1], m['pos'][2])
    
    # Body (Creepy pale white)
    glColor3f(0.8, 0.8, 0.8)
    glPushMatrix()
    glTranslatef(0, 0, 60)
    glScalef(1, 0.6, 2.0)
    glutSolidCube(30)
    glPopMatrix()
    
    # Head (Featureless)
    glPushMatrix()
    glTranslatef(0, 0, 105)
    gluSphere(gluNewQuadric(), 12, 10, 10)
    glPopMatrix()

    # Twisted Arms
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(0, side * 20, 80)
        glRotatef(45 if m['is_frozen'] else 0, 1, 0, 0)
        glScalef(0.3, 0.3, 2.0)
        glutSolidCube(25)
        glPopMatrix()
    
    glPopMatrix()

def is_in_flashlight(m):
    if not flashlight_on: return False
    
    # Vector from character to mannequin
    dx = m['pos'][0] - char_pos[0]
    dy = m['pos'][1] - char_pos[1]
    dist = math.sqrt(dx*dx + dy*dy)
    
    if dist > 450: return False # Character light range is 450
    
    # Angle of the mannequin relative to player
    angle_to_m = math.degrees(math.atan2(dy, dx))
    
    # Normalized angle difference (character looks towards char_rotation)
    diff = (angle_to_m - char_rotation + 180) % 360 - 180
    
    # beam is half-angle ~12.5 degrees (tan inverse of 100/450)
    return abs(diff) < 13 

def check_collision(x, y, radius):
    # Check map boundaries
    if x < -MAP_SIZE or x > MAP_SIZE or y < -MAP_SIZE or y > MAP_SIZE:
        return True
    
    # Check Internal Walls (AABB collision)
    for wall in walls:
        # Expand wall bounds by radius
        if (x + radius > wall['x1'] and x - radius < wall['x2'] and
            y + radius > wall['y1'] and y - radius < wall['y2']):
            return True
    
    # Check Furniture
    for f in furniture:
        fx, fy = f['pos'][0], f['pos'][1]
        # Radius ~ average of width/depth * 0.6 for rough circle
        f_rad = (f['size'][0] + f['size'][1]) / 2 * 0.6 
        dist = math.sqrt((x-fx)**2 + (y-fy)**2)
        if dist < (radius + f_rad):
            return True
            
    return False

def update_game_logic():
    global bullets, ammo_count, ammo_pickups, mannequins, mannequins_killed, door_visible, door_pos
    global mannequins_spawned, spawn_timer, lives, game_over, damage_flash_timer
    
    if game_won or game_over: return


    # Update Mannequins
    active_mannequins = []
    for m in mannequins:
        m['is_frozen'] = is_in_flashlight(m)
        
        if not m['is_frozen']:
            # Move toward player
            dx = char_pos[0] - m['pos'][0]
            dy = char_pos[1] - m['pos'][1]
            dist = math.sqrt(dx*dx + dy*dy)
            if dist > 5:
                step = MANNEQUIN_SPEED
                nx = m['pos'][0] + (dx/dist) * step
                ny = m['pos'][1] + (dy/dist) * step
                
                # Check collision with walls only (not furniture)
                wall_collision = False
                for wall in walls:
                    if (nx + 20 > wall['x1'] and nx - 20 < wall['x2'] and
                        ny + 20 > wall['y1'] and ny - 20 < wall['y2']):
                        wall_collision = True
                        break
                
                if wall_collision:
                    # Try moving along the wall - attempt perpendicular directions
                    # Try moving in X direction only
                    nx_alt = m['pos'][0] + (dx/dist) * step
                    ny_alt = m['pos'][1]
                    wall_collision_x = False
                    for wall in walls:
                        if (nx_alt + 20 > wall['x1'] and nx_alt - 20 < wall['x2'] and
                            ny_alt + 20 > wall['y1'] and ny_alt - 20 < wall['y2']):
                            wall_collision_x = True
                            break
                    
                    if not wall_collision_x:
                        nx, ny = nx_alt, ny_alt
                    else:
                        # Try moving in Y direction only
                        nx_alt = m['pos'][0]
                        ny_alt = m['pos'][1] + (dy/dist) * step
                        wall_collision_y = False
                        for wall in walls:
                            if (nx_alt + 20 > wall['x1'] and nx_alt - 20 < wall['x2'] and
                                ny_alt + 20 > wall['y1'] and ny_alt - 20 < wall['y2']):
                                wall_collision_y = True
                                break
                        
                        if not wall_collision_y:
                            nx, ny = nx_alt, ny_alt
                        else:
                            # Both blocked, stay in place
                            nx, ny = m['pos'][0], m['pos'][1]
                
                m['pos'][0] = nx
                m['pos'][1] = ny
            
            # Check collision with player (Damage)
            if math.sqrt((char_pos[0]-m['pos'][0])**2 + (char_pos[1]-m['pos'][1])**2) < 30:
                lives -= 1
                damage_flash_timer = 5 # Flash red
                # Teleport mannequin away to avoid instant kill
                m['pos'] = [random.uniform(-MAP_SIZE, MAP_SIZE), random.uniform(-MAP_SIZE, MAP_SIZE), 0]
                if lives <= 0:
                    game_over = True
                    
        active_mannequins.append(m)
    mannequins = active_mannequins

    # Update Bullets
    bullet_speed = 30
    new_bullets = []
    for b in bullets:
        rad = math.radians(b['angle'])
        b['pos'][0] += bullet_speed * math.cos(rad)
        b['pos'][1] += bullet_speed * math.sin(rad)
        
        # Bullet vs Mannequin collision
        hit = False
        remaining_mannequins = []
        for m in mannequins:
            mdist = math.sqrt((b['pos'][0]-m['pos'][0])**2 + (b['pos'][1]-m['pos'][1])**2)
            if not hit and mdist < 40:
                # Mannequin Killed
                hit = True
                mannequins_killed += 1
                if mannequins_killed >= MANNEQUIN_COUNT:
                    door_visible = True
                    door_pos = [MAP_SIZE - 300, MAP_SIZE - 100, 0] 
            else:
                remaining_mannequins.append(m)
        mannequins = remaining_mannequins

        # Respawn Logic (Maintain 3 active)
        if mannequins_killed < MANNEQUIN_COUNT and len(mannequins) < 3 and mannequins_spawned < MANNEQUIN_COUNT:
             spawn_pos = [0,0,0]
             valid = False
             for _ in range(10):
                spawn_pos = [random.uniform(-MAP_SIZE, MAP_SIZE), random.uniform(-MAP_SIZE, MAP_SIZE), 0]
                if not check_collision(spawn_pos[0], spawn_pos[1], 30) and \
                   math.sqrt((spawn_pos[0]-char_pos[0])**2 + (spawn_pos[1]-char_pos[1])**2) > 400:
                    valid = True
                    break
             if valid:
                mannequins.append({'pos': spawn_pos, 'is_frozen': False})
                mannequins_spawned += 1
        
        if not hit and abs(b['pos'][0]) < MAP_SIZE and abs(b['pos'][1]) < MAP_SIZE:
            new_bullets.append(b)
    bullets = new_bullets

    # Update Pickups
    remaining_pickups = []
    for p in ammo_pickups:
        p['rotation'] += 2
        dist = math.sqrt((char_pos[0] - p['pos'][0])**2 + (char_pos[1] - p['pos'][1])**2)
        
        # Pickup Condition: Low Ammo OR Low Health
        if dist < PICKUP_RADIUS and (ammo_count < 10 or lives < 5): 
            if ammo_count < 10:
                ammo_count += 5
            if lives < 5:
                lives += 1
        else:
            remaining_pickups.append(p)
    ammo_pickups = remaining_pickups

def draw_door():
    if not door_visible: return
    glPushMatrix()
    glTranslatef(door_pos[0], door_pos[1], door_pos[2])
    glRotatef(180, 0, 0, 1) # Rotate to face inward 

    # Door Frame (Dark Wood)
    glColor3f(0.5, 0.05, 0.05)
    glPushMatrix(); glTranslatef(0, 0, 150); glScalef(240/30, 20/30, 300/30); glutSolidCube(30); glPopMatrix() # Frame outline logic is complex with cubes.

    # Top
    glPushMatrix(); glTranslatef(0, -5, 290); glScalef(220/30, 20/30, 20/30); glutSolidCube(30); glPopMatrix()
    # Left
    glPushMatrix(); glTranslatef(-100, -5, 140); glScalef(20/30, 20/30, 300/30); glutSolidCube(30); glPopMatrix()
    # Right
    glPushMatrix(); glTranslatef(100, -5, 140); glScalef(20/30, 20/30, 300/30); glutSolidCube(30); glPopMatrix()

    # The Door Itself 
    glColor3f(0.6, 0.05, 0.05) # Deep Red
    glPushMatrix(); glTranslatef(0, 0, 140); glScalef(180/30, 10/30, 280/30); glutSolidCube(30); glPopMatrix()
    
    # Panels
    glColor3f(0.4, 0.0, 0.0)
    # Top Panel
    glPushMatrix(); glTranslatef(0, 6, 220); glScalef(120/30, 2/30, 80/30); glutSolidCube(30); glPopMatrix()
    # Bottom Panel
    glPushMatrix(); glTranslatef(0, 6, 80); glScalef(120/30, 2/30, 100/30); glutSolidCube(30); glPopMatrix()
    
    # Doorknob (Gold)
    glColor3f(0.8, 0.7, 0.2)
    glPushMatrix(); glTranslatef(70, 8, 130); gluSphere(gluNewQuadric(), 8, 10, 10); glPopMatrix()

    glPopMatrix()

def draw_sofa(x, y, z, rot, sx, sy, sz):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(rot, 0, 0, 1)
    
    # Base
    glColor3f(0.3, 0.1, 0.1) 
    glPushMatrix(); glTranslatef(0, 0, sz*0.3); glScalef(sx/30, sy/30, sz*0.6/30); glutSolidCube(30); glPopMatrix()
    # Back
    glPushMatrix(); glTranslatef(-sx*0.3, 0, sz*0.8); glScalef(sx*0.2/30, sy/30, sz/30); glutSolidCube(30); glPopMatrix()
    # Arms
    glPushMatrix(); glTranslatef(0, sy*0.4, sz*0.6); glScalef(sx/30, sy*0.2/30, sz*0.5/30); glutSolidCube(30); glPopMatrix()
    glPushMatrix(); glTranslatef(0, -sy*0.4, sz*0.6); glScalef(sx/30, sy*0.2/30, sz*0.5/30); glutSolidCube(30); glPopMatrix()
    
    glPopMatrix()

def draw_almirah(x, y, z, rot, sx, sy, sz):
    glPushMatrix()
    glTranslatef(x, y, z + sz/2)
    glRotatef(rot, 0, 0, 1)
    glColor3f(0.25, 0.15, 0.05) # Dark wood
    glScalef(sx/30, sy/30, sz/30)
    glutSolidCube(30)

    glColor3f(0.05, 0.0, 0.0)
    glPushMatrix(); glTranslatef(sx*0.51, 0, 0); glScalef(0.05, sy/30*0.05, sz/30); glutSolidCube(30); glPopMatrix()
    glPopMatrix()

def draw_flower_vase(x, y, z):
    """Draw a large decorative flower vase with flowers"""
    glPushMatrix()
    glTranslatef(x, y, z)
    
    # Vase Body (Ceramic Teal)
    glColor3f(0.6, 0.5, 0.18)
    # Bottom sphere
    glPushMatrix()
    glTranslatef(0, 0, 20)
    gluSphere(gluNewQuadric(), 20, 16, 16)
    glPopMatrix()
    # Neck
    glPushMatrix()
    glTranslatef(0, 0, 30)
    gluCylinder(gluNewQuadric(), 15, 10, 30, 16, 1)
    glPopMatrix()
    # Rim
    glPushMatrix()
    glTranslatef(0, 0, 60)
    gluDisk(gluNewQuadric(), 0, 15, 16, 1)
    glPopMatrix()
    
    # Flowers and Stems
    glPushMatrix()
    glTranslatef(0, 0, 60)
    
    # Stem 1
    glColor3f(0.1, 0.4, 0.1)
    glPushMatrix(); glRotatef(10, 1, 0, 0); gluCylinder(gluNewQuadric(), 1.5, 1.5, 40, 8, 1); glPopMatrix()
    # Flower 1
    glColor3f(1, 0, 0) # Red
    glPushMatrix(); glTranslatef(0, -7, 40); gluSphere(gluNewQuadric(), 6, 8, 8); glPopMatrix()
    
    # Stem 2
    glColor3f(0.1, 0.4, 0.1)
    glPushMatrix(); glRotatef(-15, 0, 1, 0); gluCylinder(gluNewQuadric(), 1.5, 1.5, 35, 8, 1); glPopMatrix()
    # Flower 2
    glColor3f(1, 1, 0) # Yellow
    glPushMatrix(); glTranslatef(9, 0, 35); gluSphere(gluNewQuadric(), 6, 8, 8); glPopMatrix()
    
    # Stem 3
    glColor3f(0.1, 0.4, 0.1)
    glPushMatrix(); glRotatef(15, 1, 1, 0); gluCylinder(gluNewQuadric(), 1.5, 1.5, 38, 8, 1); glPopMatrix()
    # Flower 3
    glColor3f(1, 0.5, 0) # Orange
    glPushMatrix(); glTranslatef(-8, -8, 38); gluSphere(gluNewQuadric(), 6, 8, 8); glPopMatrix()
    
    glPopMatrix()
    glPopMatrix()

def draw_staircase(x, y, z, rot, width, height, steps):
    """Draw a wooden staircase with accurate shading for visible steps"""
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(rot, 0, 0, 1)
    
    step_depth = width / steps
    step_height = height / steps
    
    for i in range(steps):
        # 1. Main Block / Riser (Medium-Dark shade)
        glColor3f(0.12, 0.08, 0.04) 
        glPushMatrix()
        glTranslatef(i * step_depth, 0, (i + 0.5) * step_height)
        glScalef(step_depth/30, 200/30, (i + 1) * step_height / 30)
        glutSolidCube(30)
        glPopMatrix()
        
        # 2. Tread 
        glColor3f(0.25, 0.2, 0.15)
        glPushMatrix()
        glTranslatef(i * step_depth, 0, (i + 1) * step_height)
        glScalef(step_depth/30, 200/30, 4/30) # Thin top plate
        glutSolidCube(30)
        glPopMatrix()
        
        # 3. Deep Shadow 
        glColor3f(0.01, 0.01, 0.01) # Near black
        glPushMatrix()
        glTranslatef((i + 0.48) * step_depth, 0, (i + 1) * step_height + 2)
        glScalef(0.05, 200/30, 8/30)
        glutSolidCube(30)
        glPopMatrix()
        
    glPopMatrix()

def draw_dining_table(x, y, z, rot, sx, sy, sz):
    """Draw a rectangular dining table with legs"""
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(rot, 0, 0, 1)
    
    # Top (Dark Wood)
    glColor3f(0.15, 0.1, 0.05)
    glPushMatrix()
    glTranslatef(0, 0, sz)
    glScalef(sx/30, sy/30, 8/30)
    glutSolidCube(30)
    glPopMatrix()
    
    # Legs
    glPushMatrix()
    for dx in [-sx*0.4, sx*0.4]:
        for dy in [-sy*0.4, sy*0.4]:
            glPushMatrix()
            glTranslatef(dx, dy, sz/2)
            glScalef(8/30, 8/30, sz/30)
            glutSolidCube(30)
            glPopMatrix()
    glPopMatrix()
    
    glPopMatrix()

def draw_chair(x, y, z, rot, sx, sy, sz):
    """Draw a chair with seat, backrest and 4 legs"""
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(rot, 0, 0, 1)
    
    # Seat
    glColor3f(0.2, 0.1, 0.05)
    glPushMatrix()
    glTranslatef(0, 0, 40)
    glScalef(sx/30, sy/30, 6/30)
    glutSolidCube(30)
    glPopMatrix()
    
    # Backrest
    glPushMatrix()
    glTranslatef(-sx*0.45, 0, 70)
    glScalef(4/30, sy/30, 60/30)
    glutSolidCube(30)
    glPopMatrix()
    
    # Legs
    glPushMatrix()
    for dx in [-sx*0.4, sx*0.4]:
        for dy in [-sy*0.4, sy*0.4]:
            glPushMatrix()
            glTranslatef(dx, dy, 20)
            glScalef(4/30, 4/30, 40/30)
            glutSolidCube(30)
            glPopMatrix()
    glPopMatrix()
    
    glPopMatrix()

def draw_dining_chandelier(x, y, z):
    """Draw a chandelier that throws light onto the dining table"""
    glPushMatrix()
    glTranslatef(x, y, z)
    
    # Chain from ceiling
    glColor3f(0.2, 0.2, 0.2)
    glPushMatrix()
    glTranslatef(0, 0, 25)
    glScalef(2/30, 2/30, 50/30)
    glutSolidCube(30)
    glPopMatrix()
    
    # Ornate Body
    glColor3f(0.8, 0.7, 0.2) # Golden
    gluSphere(gluNewQuadric(), 15, 12, 12)
    
    # Arms and Candles
    for i in range(4):
        glPushMatrix()
        glRotatef(i * 90, 0, 0, 1)
        glTranslatef(20, 0, 5)
        # Arm
        glColor3f(0.7, 0.6, 0.1)
        glPushMatrix(); glScalef(20/30, 4/30, 4/30); glutSolidCube(30); glPopMatrix()
        # Candle
        glTranslatef(8, 0, 10)
        glColor3f(0.9, 0.9, 0.8)
        glPushMatrix(); glScalef(4/30, 4/30, 15/30); glutSolidCube(30); glPopMatrix()
        # Flame
        glColor3f(1, 0.6, 0.1)
        glTranslatef(0, 0, 10)
        gluSphere(gluNewQuadric(), 4, 8, 8)
        glPopMatrix()
        
    # Light Beam 
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1.0, 1.0, 0.5, 0.2) # Dim yellow light
    glPushMatrix()
    glRotatef(180, 1, 0, 0) # Point down
    gluCylinder(gluNewQuadric(), 10, 150, 250, 20, 1)
    glPopMatrix()
  
    
    glPopMatrix()

def draw_bed(x, y, z, rot, sx, sy, sz):
    """Draw a bed with frame, mattress, headboard, and pillow"""
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(rot, 0, 0, 1)
    
    # Bed Frame (Dark Wood)
    glColor3f(0.10, 0.07, 0.03)
    glPushMatrix()
    glScalef(sx/30, sy/30, 10/30) # Low base
    glTranslatef(0, 0, 15)
    glutSolidCube(30)
    glPopMatrix()
    
    # Mattress (Off-white)
    glColor3f(0.5, 0.05, 0.05)
    glPushMatrix()
    glTranslatef(0, 0, 15)
    glScalef(sx*0.95/30, sy*0.95/30, 10/30)
    glutSolidCube(30)
    glPopMatrix()
    
    # Headboard
    glColor3f(0.12, 0.08, 0.04)
    glPushMatrix()
    glTranslatef(-sx*0.45, 0, 25)
    glScalef(5/30, sy/30, 40/30)
    glutSolidCube(30)
    glPopMatrix()
    
    # Pillow
    glColor3f(0.96, 0.94, 0.90)
    glPushMatrix()
    glTranslatef(-sx*0.35, 0, 22)
    glScalef(sx*0.2/30, sy*0.6/30, 5/30)
    glutSolidCube(30)
    glPopMatrix()
    
    glPopMatrix()

def draw_picture_frame(x, y, z, width, height, orientation='north'):
    """Draw a picture frame on a wall
    orientation: 'north', 'south', 'east', 'west'
    """
    glPushMatrix()
    glTranslatef(x, y, z)
    
    # Rotate based on wall orientation
    if orientation == 'north':
        glRotatef(0, 0, 0, 1)
    elif orientation == 'south':
        glRotatef(180, 0, 0, 1)
    elif orientation == 'east':
        glRotatef(-90, 0, 0, 1)
    elif orientation == 'west':
        glRotatef(90, 0, 0, 1)
    
    # Frame (Dark wood)
    glColor3f(0.2, 0.12, 0.05)
    frame_thickness = 8
    # Top
    glPushMatrix(); glTranslatef(0, -2, height/2 + frame_thickness/2); glScalef(width/30, 4/30, frame_thickness/30); glutSolidCube(30); glPopMatrix()
    # Bottom
    glPushMatrix(); glTranslatef(0, -2, -height/2 - frame_thickness/2); glScalef(width/30, 4/30, frame_thickness/30); glutSolidCube(30); glPopMatrix()
    # Left
    glPushMatrix(); glTranslatef(-width/2 - frame_thickness/2, -2, 0); glScalef(frame_thickness/30, 4/30, height/30); glutSolidCube(30); glPopMatrix()
    # Right
    glPushMatrix(); glTranslatef(width/2 + frame_thickness/2, -2, 0); glScalef(frame_thickness/30, 4/30, height/30); glutSolidCube(30); glPopMatrix()
    
    # Picture interior (Dark/mysterious)
    glColor3f(0.1, 0.08, 0.06)
    glPushMatrix(); glTranslatef(0, 0, 0); glScalef(width/30, 2/30, height/30); glutSolidCube(30); glPopMatrix()
    
    glPopMatrix()

def draw_chandelier():
    """Draw a large chandelier in the center of the house"""
    glPushMatrix()
    glTranslatef(0, 0, 250)  
    
    # Central chain/rod (Dark metal) - extends upward
    glColor3f(0.2, 0.2, 0.2)
    glPushMatrix()
    glTranslatef(0, 0, 0) 
    gluCylinder(gluNewQuadric(), 4, 4, 80, 10, 1)  # Extends upward in +Z
    glPopMatrix()
    
    # Main body (ornate sphere) 
    glColor3f(0.3, 0.25, 0.15) 
    gluSphere(gluNewQuadric(), 30, 16, 16)
    
    #rings around center
    glColor3f(0.4, 0.35, 0.2)
    glPushMatrix()
    glRotatef(90, 1, 0, 0)
    glutSolidTorus(3, 35, 8, 16)
    glPopMatrix()
    
    # Arms extending outward (6 arms)
    num_arms = 6
    for i in range(num_arms):
        angle = (360.0 / num_arms) * i
        glPushMatrix()
        glRotatef(angle, 0, 0, 1)
        glTranslatef(40, 0, -15)
        glRotatef(25, 0, 1, 0)  # Angle downward
        
        # Arm (Ornate metal)
        glColor3f(0.25, 0.2, 0.12)
        glPushMatrix()
        glRotatef(90, 0, 1, 0)
        gluCylinder(gluNewQuadric(), 3, 2, 35, 8, 1)
        glPopMatrix()
        
        # Candle holder at end
        glTranslatef(35, 0, 0)
        glColor3f(0.3, 0.25, 0.15)
        # Base plate
        glPushMatrix()
        glRotatef(90, 1, 0, 0)
        glutSolidTorus(2, 6, 6, 12)
        glPopMatrix()
        
        # Candle stick holder
        gluCylinder(gluNewQuadric(), 5, 4, 8, 10, 1)
        
        # Wax candle
        glTranslatef(0, 0, 8)
        glColor3f(0.9, 0.85, 0.7)  # Cream/ivory wax
        gluCylinder(gluNewQuadric(), 3.5, 3.5, 20, 10, 1)
        
        # Wax drips
        glColor3f(0.85, 0.8, 0.65)
        glPushMatrix()
        glTranslatef(3, 0, 5)
        glScalef(0.3, 0.3, 1.5)
        gluSphere(gluNewQuadric(), 3, 6, 6)
        glPopMatrix()
        
        # Flame (bright and visible)
        glTranslatef(0, 0, 20)
        # Outer glow (orange)
        glColor3f(1.0, 0.5, 0.1)
        glPushMatrix()
        glScalef(1, 1, 1.5)
        gluSphere(gluNewQuadric(), 6, 8, 8)
        glPopMatrix()
        
        # Inner flame (bright yellow)
        glColor3f(1.0, 0.9, 0.3)
        glPushMatrix()
        glScalef(0.7, 0.7, 1.3)
        gluSphere(gluNewQuadric(), 5, 8, 8)
        glPopMatrix()
        
        # Core (white-hot)
        glColor3f(1.0, 1.0, 0.8)
        glPushMatrix()
        glScalef(0.5, 0.5, 1.0)
        gluSphere(gluNewQuadric(), 4, 6, 6)
        glPopMatrix()
        
        glPopMatrix()
    
    glPopMatrix()

def draw_player():
    glPushMatrix()
    glTranslatef(char_pos[0], char_pos[1], 0)
    glRotatef(char_rotation, 0, 0, 1)
    
    # Legs
    glColor3f(0.2, 0.2, 0.3) 
    # Left leg
    glPushMatrix()
    glTranslatef(-8, 0, 15)
    glScalef(6/30, 6/30, 30/30)
    glutSolidCube(30)
    glPopMatrix()
    # Right leg
    glPushMatrix()
    glTranslatef(8, 0, 15)
    glScalef(6/30, 6/30, 30/30)
    glutSolidCube(30)
    glPopMatrix()
    
    # Torso
    glColor3f(0.4, 0.3, 0.25) 
    glPushMatrix()
    glTranslatef(0, 0, 45)
    glScalef(20/30, 12/30, 35/30)
    glutSolidCube(30)
    glPopMatrix()
    
    # Arms
    glColor3f(0.6, 0.45, 0.35)  # Skin tone
    # Left arm
    glPushMatrix()
    glTranslatef(-15, 0, 50)
    glScalef(5/30, 5/30, 25/30)
    glutSolidCube(30)
    glPopMatrix()
    # Right arm
    glPushMatrix()
    glTranslatef(15, 0, 50)
    glScalef(5/30, 5/30, 25/30)
    glutSolidCube(30)
    glPopMatrix()
    
    # Neck
    glColor3f(0.6, 0.45, 0.35)  # Skin tone
    glPushMatrix()
    glTranslatef(0, 0, 65)
    glScalef(6/30, 6/30, 8/30)
    glutSolidCube(30)
    glPopMatrix()
    
    # Head
    glColor3f(0.65, 0.5, 0.4)  # Skin tone
    glPushMatrix()
    glTranslatef(0, 0, 75)
    gluSphere(gluNewQuadric(), 10, 12, 12)
    glPopMatrix()
    
    # Hair (black)
    glColor3f(0.05, 0.05, 0.05)
    glPushMatrix()
    glTranslatef(0, 0, 78)
    glScalef(1.0, 1.0, 0.8)
    gluSphere(gluNewQuadric(), 10.5, 12, 12)
    glPopMatrix()
    
    glPopMatrix()

def draw_girl():
    if not game_won: return
    glPushMatrix()
    girl_x = door_pos[0]
    girl_y = door_pos[1] - 100 
    glTranslatef(girl_x, girl_y, 0)
    glRotatef(180, 0, 0, 1) # Face the player

    # Legs
    glColor3f(0.85, 0.75, 0.65) # Skin tone
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(0, side * 6, 15)
        glScalef(6/30, 6/30, 30/30)
        glutSolidCube(30)
        glPopMatrix()
    
    # Body / Dress 
    glColor3f(1.0, 0.8, 0.9) 
    # Skirt part
    glPushMatrix(); glTranslatef(0, 0, 30); glRotatef(-90, 1, 0, 0); glutSolidCone(20, 45, 20, 20); glPopMatrix()
    # Torso
    glPushMatrix(); glTranslatef(0, 0, 60); glScalef(10/30, 18/30, 25/30); glutSolidCube(30); glPopMatrix() 
    
    # Arms
    glColor3f(0.85, 0.75, 0.65) # Skin tone
    for side in [-1, 1]:
        glPushMatrix(); glTranslatef(0, side * 12, 60); glScalef(4/30, 4/30, 18/30); glutSolidCube(30); glPopMatrix()
    
    # Head
    glColor3f(0.85, 0.75, 0.65) # Skin tone
    glPushMatrix(); glTranslatef(0, 0, 85); gluSphere(gluNewQuadric(), 10, 12, 12); glPopMatrix() 
    
    # Long Deep Red Hair
    glColor3f(0.4, 0.0, 0.0) # Dark red
    glPushMatrix()
    glTranslatef(-2, 0, 85) # Back of head
    # Hair draped down
    glPushMatrix(); glTranslatef(-4, 0, -20); glScalef(10/30, 18/30, 40/30); glutSolidCube(30); glPopMatrix()
    # Hair on top
    glPushMatrix(); glTranslatef(2, 0, 8); glScalef(12/30, 20/30, 8/30); glutSolidCube(30); glPopMatrix()
    glPopMatrix()

    glPopMatrix()

def draw_house():
    # Floor
    plank_width = 80
    gap = 5
    
    glBegin(GL_QUADS)
    for x in range(-MAP_SIZE, MAP_SIZE, plank_width):
        # Plank (Dark Wood)
        glColor3f(0.15, 0.1, 0.05) 
        glVertex3f(x, -MAP_SIZE, 0)
        glVertex3f(x + plank_width - gap, -MAP_SIZE, 0)
        glVertex3f(x + plank_width - gap, MAP_SIZE, 0)
        glVertex3f(x, MAP_SIZE, 0)
        
        # Black Line (Gap)
        glColor3f(0.0, 0.0, 0.0)
        glVertex3f(x + plank_width - gap, -MAP_SIZE, 0)
        glVertex3f(x + plank_width, -MAP_SIZE, 0)
        glVertex3f(x + plank_width, MAP_SIZE, 0)
        glVertex3f(x + plank_width - gap, MAP_SIZE, 0)
    glEnd()
    
    # Walls - Grungy Olive/Beige
    glColor3f(0.25, 0.23, 0.17)
    wall_height = 300
    
    # Draw 4 walls
    glBegin(GL_QUADS)
    # Wall 1
    glVertex3f(-MAP_SIZE, -MAP_SIZE, 0); glVertex3f(MAP_SIZE, -MAP_SIZE, 0); glVertex3f(MAP_SIZE, -MAP_SIZE, wall_height); glVertex3f(-MAP_SIZE, -MAP_SIZE, wall_height)
    # Wall 2
    glVertex3f(-MAP_SIZE, MAP_SIZE, 0); glVertex3f(MAP_SIZE, MAP_SIZE, 0); glVertex3f(MAP_SIZE, MAP_SIZE, wall_height); glVertex3f(-MAP_SIZE, MAP_SIZE, wall_height)
    # Wall 3
    glVertex3f(-MAP_SIZE, -MAP_SIZE, 0); glVertex3f(-MAP_SIZE, MAP_SIZE, 0); glVertex3f(-MAP_SIZE, MAP_SIZE, wall_height); glVertex3f(-MAP_SIZE, -MAP_SIZE, wall_height)
    # Wall 4
    glVertex3f(MAP_SIZE, -MAP_SIZE, 0); glVertex3f(MAP_SIZE, MAP_SIZE, 0); glVertex3f(MAP_SIZE, MAP_SIZE, wall_height); glVertex3f(MAP_SIZE, -MAP_SIZE, wall_height)
    glEnd()
    
    # Internal Walls (Room partitions)
    glBegin(GL_QUADS)
    for wall in walls:
        x1, y1 = wall['x1'], wall['y1']
        x2, y2 = wall['x2'], wall['y2']
        # Front face
        glVertex3f(x1, y1, 0); glVertex3f(x2, y1, 0); glVertex3f(x2, y1, wall_height); glVertex3f(x1, y1, wall_height)
        # Back face
        glVertex3f(x1, y2, 0); glVertex3f(x2, y2, 0); glVertex3f(x2, y2, wall_height); glVertex3f(x1, y2, wall_height)
        # Left face
        glVertex3f(x1, y1, 0); glVertex3f(x1, y2, 0); glVertex3f(x1, y2, wall_height); glVertex3f(x1, y1, wall_height)
        # Right face
        glVertex3f(x2, y1, 0); glVertex3f(x2, y2, 0); glVertex3f(x2, y2, wall_height); glVertex3f(x2, y1, wall_height)
    glEnd()

    # Window positions
    for i in range(-MAP_SIZE + 200, MAP_SIZE, 400):
        # Top Wall
        x, y, z_bot, z_top, w_width = i, MAP_SIZE-5, 120, 220, 150
        
        # Glass
        glColor4f(0.5, 0.7, 0.9, 0.6)
        glBegin(GL_QUADS)
        glVertex3f(x, y, z_bot); glVertex3f(x+w_width, y, z_bot); glVertex3f(x+w_width, y, z_top); glVertex3f(x, y, z_top)
        glEnd()
        
        # Grid (using thin quads)
        glColor3f(0.1, 0.1, 0.2)
        # Vertical bar
        glBegin(GL_QUADS)
        mid_x = x + w_width/2
        glVertex3f(mid_x-2, y+1, z_bot); glVertex3f(mid_x+2, y+1, z_bot); glVertex3f(mid_x+2, y+1, z_top); glVertex3f(mid_x-2, y+1, z_top)
        # Horizontal bar
        mid_z = (z_bot + z_top) / 2
        glVertex3f(x, y+1, mid_z-2); glVertex3f(x+w_width, y+1, mid_z-2); glVertex3f(x+w_width, y+1, mid_z+2); glVertex3f(x, y+1, mid_z+2)
        glEnd()



    # Furniture
    for f in furniture:
        if f['type'] == 'sofa':
            draw_sofa(f['pos'][0], f['pos'][1], f['pos'][2], f['rot'], f['size'][0], f['size'][1], f['size'][2])
        elif f['type'] == 'almirah':
            draw_almirah(f['pos'][0], f['pos'][1], f['pos'][2], f['rot'], f['size'][0], f['size'][1], f['size'][2])
        elif f['type'] == 'bed':
            draw_bed(f['pos'][0], f['pos'][1], f['pos'][2], f['rot'], f['size'][0], f['size'][1], f['size'][2])
        elif f['type'] == 'vase':
            draw_flower_vase(f['pos'][0], f['pos'][1], f['pos'][2])
        elif f['type'] == 'staircase':
            # f['size'] = [width, length, total_height]
            draw_staircase(f['pos'][0], f['pos'][1], f['pos'][2], f['rot'], f['size'][0], f['size'][2], 10)
        elif f['type'] == 'dining_table':
            draw_dining_table(f['pos'][0], f['pos'][1], f['pos'][2], f['rot'], f['size'][0], f['size'][1], f['size'][2])
        elif f['type'] == 'chair':
            draw_chair(f['pos'][0], f['pos'][1], f['pos'][2], f['rot'], f['size'][0], f['size'][1], f['size'][2])
        elif f['type'] == 'dining_chandelier':
            draw_dining_chandelier(f['pos'][0], f['pos'][1], f['pos'][2])

    # North Wall
    draw_picture_frame(0, MAP_SIZE - 5, 150, 80, 100, 'north')
    draw_picture_frame(400, MAP_SIZE - 5, 180, 60, 80, 'north')
    draw_picture_frame(-500, MAP_SIZE - 5, 160, 70, 90, 'north')
    # South Wall
    draw_picture_frame(0, -MAP_SIZE + 5, 140, 90, 110, 'south')
    draw_picture_frame(-400, -MAP_SIZE + 5, 170, 65, 85, 'south')
    # East Wall
    draw_picture_frame(MAP_SIZE - 5, 300, 150, 75, 95, 'east')
    draw_picture_frame(MAP_SIZE - 5, -400, 160, 80, 100, 'east')
    # West Wall
    draw_picture_frame(-MAP_SIZE + 5, 200, 145, 70, 90, 'west')
    draw_picture_frame(-MAP_SIZE + 5, -300, 155, 75, 95, 'west')
    
    # Chandelier in center
    draw_chandelier()

def draw_visibility_circle():
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDisable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslatef(char_pos[0], char_pos[1], 0)
    inner_radius, outer_radius, segments = 180, 1200, 32
    glBegin(GL_QUAD_STRIP)
    for i in range(segments + 1):
        angle = 2.0 * math.pi * i / segments
        glColor4f(0.0, 0.0, 0.01, 0.0); glVertex3f(math.cos(angle) * inner_radius, math.sin(angle) * inner_radius, 150)
        glColor4f(0.0, 0.0, 0.01, 0.95); glVertex3f(math.cos(angle) * outer_radius, math.sin(angle) * outer_radius, 150)
    glEnd()
    glPopMatrix()
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_BLEND)

def draw_character():
    glPushMatrix()
    glTranslatef(char_pos[0], char_pos[1], char_pos[2])
    glRotatef(char_rotation, 0, 0, 1) # No offset, +X is front
    
    glColor3f(0.2, 0.2, 0.3)
    # Left leg
    glPushMatrix()
    glTranslatef(0, -8, 15)
    glScalef(6/30, 6/30, 30/30)
    glutSolidCube(30)
    glPopMatrix()
    # Right leg
    glPushMatrix()
    glTranslatef(0, 8, 15)
    glScalef(6/30, 6/30, 30/30)
    glutSolidCube(30)
    glPopMatrix()
    
    # Torso (Brown shirt)
    glColor3f(0.4, 0.3, 0.25)
    glPushMatrix()
    glTranslatef(0, 0, 45)
    glScalef(12/30, 20/30, 35/30)
    glutSolidCube(30)
    glPopMatrix()
    
    # Arms (Skin tone) 
    glColor3f(0.6, 0.45, 0.35)
    # Left arm
    glPushMatrix()
    glTranslatef(0, -15, 50)
    glScalef(5/30, 5/30, 25/30)
    glutSolidCube(30)
    glPopMatrix()
    # Right arm 
    glPushMatrix()
    glTranslatef(0, 15, 50)
    glScalef(5/30, 5/30, 25/30)
    glutSolidCube(30)
    glPopMatrix()
    
    # Neck
    glColor3f(0.6, 0.45, 0.35)
    glPushMatrix()
    glTranslatef(0, 0, 65)
    glScalef(6/30, 6/30, 8/30)
    glutSolidCube(30)
    glPopMatrix()
    
    # Head 
    glColor3f(0.65, 0.5, 0.4)
    glPushMatrix()
    glTranslatef(0, 0, 75)
    gluSphere(gluNewQuadric(), 10, 12, 12)
    glPopMatrix()
    
    # Hair 
    glColor3f(0.05, 0.05, 0.05)
    glPushMatrix()
    glTranslatef(-2, 0, 78)
    glScalef(1.0, 1.0, 0.8)
    gluSphere(gluNewQuadric(), 10.5, 12, 12)
    glPopMatrix()
    
    # Flashlight
    if flashlight_on:
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glPushMatrix()
        glTranslatef(12, 15, 50) 
        glRotatef(90, 0, 1, 0)   
        glColor4f(1.0, 1.0, 0.8, 0.4)
        gluCylinder(gluNewQuadric(), 5, 100, 450, 20, 1)
        glPopMatrix()
        glDisable(GL_BLEND)
    
    glPopMatrix()

def draw_damage_overlay():
    global damage_flash_timer
    if damage_flash_timer > 0:
        damage_flash_timer -= 1
        glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity(); gluOrtho2D(0, 1000, 0, 800); glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity()
        
        glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1.0, 0.0, 0.0, 0.5)
        glBegin(GL_QUADS)
        glVertex2f(0, 0); glVertex2f(1000, 0); glVertex2f(1000, 800); glVertex2f(0, 800)
        glEnd()
        glDisable(GL_BLEND)
        
        glPopMatrix(); glMatrixMode(GL_PROJECTION); glPopMatrix(); glMatrixMode(GL_MODELVIEW)

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800) # Fix white screen
    
    glEnable(GL_DEPTH_TEST); glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    update_game_logic()
    setupCamera()
    
    draw_house()

    for m in mannequins: draw_mannequin(m)
    for p in ammo_pickups:
        glPushMatrix(); glTranslatef(p['pos'][0], p['pos'][1], p['pos'][2]); glRotatef(p['rotation'], 0, 0, 1); glColor3f(0.1, 0.6, 0.1); glutSolidCube(20); glPopMatrix()
    for b in bullets:
        glPushMatrix(); glTranslatef(b['pos'][0], b['pos'][1], b['pos'][2]); glColor3f(1, 1, 0.5); gluSphere(gluNewQuadric(), 4, 8, 8); glPopMatrix()

    draw_character()
    draw_door()
    draw_girl()
    draw_visibility_circle()
    

    draw_damage_overlay()
    
    if game_won:
        draw_text(350, 400, "RESCUED, YOU WIN")
        draw_text(380, 370, "Press 'R' to Play Again")
    elif game_over:
        draw_text(300, 400, "YOU COULDN'T RESCUE HER, YOU LOSE")
        draw_text(380, 370, "Press 'R' to Play Again")
    else:
        draw_text(20, 750, f"LIVES: {lives} | AMMO: {ammo_count} | KILLED: {mannequins_killed}/{MANNEQUIN_COUNT}")
        
        if ammo_count <= 0:
            draw_text(350, 400, "OUT OF AMMO, RELOAD IT")
    
    glutSwapBuffers()

def setupCamera():
    glMatrixMode(GL_PROJECTION); glLoadIdentity(); gluPerspective(65, 1.25, 1.0, 3000)
    glMatrixMode(GL_MODELVIEW); glLoadIdentity()
    cam_dist = 450
    rad = math.radians(char_rotation)
    cam_x = (char_pos[0] - cam_dist * math.cos(rad)) + (camera_pan * math.sin(rad))
    cam_y = (char_pos[1] - cam_dist * math.sin(rad)) - (camera_pan * math.cos(rad))
    gluLookAt(cam_x, cam_y, camera_pos[2], char_pos[0], char_pos[1], char_pos[2] + 50, 0, 0, 1)

def keyboardListener(key, x, y):
    global char_pos, char_rotation, flashlight_on, ammo_count, bullets, game_won
    
    # Handle both cases
    key = key.lower()
    
    if key == b'r':
        init_game()
        return
        
    if key == b'v' and ammo_count <= 0:
        ammo_count = 10

    if game_won or game_over: return

    move_speed = 18
    nx, ny = char_pos[0], char_pos[1]
    rad = math.radians(char_rotation)
    
    if key == b'w': 
        nx += move_speed * math.cos(rad)
        ny += move_speed * math.sin(rad)
    if key == b's': 
        nx -= move_speed * math.cos(rad)
        ny -= move_speed * math.sin(rad)
        
    if not check_collision(nx, ny, 25):
        char_pos[0] = nx
        char_pos[1] = ny
    if key == b'a': char_rotation += 7
    if key == b'd': char_rotation -= 7
    if key == b'f': flashlight_on = not flashlight_on
    if key == b' ' and ammo_count > 0:
        ammo_count -= 1
        # Start bullet from front of player (offset from center)
        b_rad = math.radians(char_rotation)
        bx = char_pos[0] + 30 * math.cos(b_rad)
        by = char_pos[1] + 30 * math.sin(b_rad)
        bullets.append({'pos': [bx, by, 55], 'angle': char_rotation})
    
    if key == b'p' and door_visible:
        # Check distance to door
        dist = math.sqrt((char_pos[0] - door_pos[0])**2 + (char_pos[1] - door_pos[1])**2)
        if dist < 150:
            game_won = True

def specialKeyListener(key, x, y):
    global camera_pos, camera_pan
    if key == GLUT_KEY_UP: camera_pos[2] += 20
    if key == GLUT_KEY_DOWN: camera_pos[2] -= 20
    if key == GLUT_KEY_LEFT: camera_pan -= 20
    if key == GLUT_KEY_RIGHT: camera_pan += 20

def main():
    glutInit(); glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800); glutCreateWindow(b"Mono: The Pale City")
    glutDisplayFunc(showScreen); glutIdleFunc(lambda: glutPostRedisplay())
    glutKeyboardFunc(keyboardListener); glutSpecialFunc(specialKeyListener)
    glutMainLoop()

if __name__ == "__main__": main()