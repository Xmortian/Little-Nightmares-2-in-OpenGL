
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
import math
import random

is_first_person = False
# --- Camera Intro Variables ---

game_started = False
intro_finished = False
intro_factor = 0.0 
intro_speed = 0.0009  
blink_timer = 0

reveal_mode = False
reveal_timer = 0
REVEAL_DURATION = 360  


# Starting position (Far to the right)
camera_start_pos = [1500, 0, 400]
game_time = 0
SAFE_ZONES = [
    {'pos': [0, 0], 'radius': 170},
    {'pos': [-2200, -1000], 'radius': 170},
    {'pos': [1800, -1800], 'radius': 170},
]

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
MANNEQUIN_COUNT = 5
MANNEQUIN_SPEED = 0.8 
MAP_SIZE = 2400

level = 1
MAX_LEVEL = 3

def init_game():
    global camera_pos, char_pos, char_rotation, ammo_count, bullets, ammo_pickups, game_started
    global mannequins, mannequins_killed, door_visible, game_won, furniture
    global mannequins_spawned, spawn_timer, game_over, lives, damage_flash_timer, camera_pan, flashlight_on, walls, level, MANNEQUIN_SPEED, reveal_mode, reveal_timer
    
    random.seed(423)
    camera_pos = [0, -450, 350]
    camera_pan = 0
    flashlight_on = True
    char_pos = [0, 0, 0]
    char_rotation = -90 
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
    mannequins = [] 
    level = 1
    MANNEQUIN_SPEED = 0.8
    reveal_mode = False  
    reveal_timer = 0    

    
    furniture = []
    # Room 1: North-East Corner
    furniture.append({'type': 'almirah', 'pos': [MAP_SIZE-100, MAP_SIZE-500, 0], 'rot': 90, 'size': [120, 80, 250]})
    
    # Room 2: North-West Corner
    furniture.append({'type': 'sofa', 'pos': [-MAP_SIZE+300, MAP_SIZE-150, 0], 'rot': 0, 'size': [250, 100, 60]})
    furniture.append({'type': 'almirah', 'pos': [-MAP_SIZE+100, MAP_SIZE-500, 0], 'rot': -90, 'size': [120, 80, 250]})
    furniture.append({'type': 'vase', 'pos': [MAP_SIZE-150, MAP_SIZE-800, 0], 'size': [40, 40, 60]})    # Room 3: South-West Corner
    furniture.append({'type': 'bed', 'pos': [-MAP_SIZE+250, -MAP_SIZE+250, 0], 'rot': 90, 'size': [200, 120, 50]})
    furniture.append({'type': 'vase', 'pos': [-MAP_SIZE+500, -MAP_SIZE+100, 0], 'size': [40, 40, 60]})    # Dining Area (South-East Corner)
    table_pos = [MAP_SIZE-600, -MAP_SIZE+600, 0]
    furniture.append({'type': 'dining_table', 'pos': table_pos, 'rot': 0, 'size': [250, 150, 75]})
    furniture.append({'type': 'dining_chandelier', 'pos': [table_pos[0], table_pos[1], 250], 'rot': 0, 'size': [100, 100, 100]})


    walls = []
    wall_thickness = 20
    # Central North Wall
    walls.append({'x1': -wall_thickness/2, 'y1': 600, 'x2': wall_thickness/2, 'y2': MAP_SIZE})
    # Central South Wall
    walls.append({'x1': -wall_thickness/2, 'y1': -MAP_SIZE, 'x2': wall_thickness/2, 'y2': -600})

    # Init Pickups
    ammo_pickups = []
    for _ in range(PICKUP_COUNT):
        ammo_pickups.append({
            'pos': [random.uniform(-MAP_SIZE+200, MAP_SIZE-200), random.uniform(-MAP_SIZE+200, MAP_SIZE-200), 10],
            'rotation': 0
        })

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
    
    glColor3f(0.4, 0.5, 0.6)    
    # Upper Chest
    glPushMatrix()
    glTranslatef(0, 0, 85)
    glScalef(0.7, 0.45, 1.0)
    glutSolidCube(30)
    glPopMatrix()
    # Spine/Waist (Thin connect)
    glPushMatrix()
    glTranslatef(0, 0, 60)
    glScalef(0.3, 0.3, 1.2)
    glutSolidCube(30)
    glPopMatrix()
    
    # 2. The Head (Unnerving and Tilted)
    glPushMatrix()
    glTranslatef(2, 0, 115)
    if m['is_frozen']:
        # Snap-tilts randomly when light hits to look broken
        glRotatef(35, 1, 0, 1) 
    else:
        # Creepy twitching while moving
        glRotatef(math.sin(game_time * 0.008) * 15, 0, 1, 0)
    
    # Head Sphere
    gluSphere(gluNewQuadric(), 13, 12, 12)
    # Detached neck look
    glTranslatef(0, 0, -12)
    glColor3f(0.3, 0.28, 0.25) # Darker interior for the joint
    gluCylinder(gluNewQuadric(), 6, 6, 12, 10, 1)
    glPopMatrix()

    # 3. Arms (Articulated at the elbow)
    glColor3f(0.55, 0.52, 0.48) 
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(0, side * 18, 95)
        
        # Shoulder Joint
        gluSphere(gluNewQuadric(), 5, 8, 8)
        
        # Upper Arm
        if m['is_frozen']:
            glRotatef(side * 115, 0, 1, 0) 
            glRotatef(random.uniform(-5, 5), 1, 1, 1) 
        else:
            glRotatef(side * 40, 1, 0, 0)
            
        glPushMatrix()
        glScalef(0.15, 0.15, 1.6)
        glutSolidCube(25)
        glPopMatrix()
        
        # Elbow Joint
        glTranslatef(0, 0, 40)
        gluSphere(gluNewQuadric(), 4, 8, 8)
        
        # Lower Arm (Tilted at a "broken" angle)
        glRotatef(80 if m['is_frozen'] else 30, 0, 1, 0)
        glPushMatrix()
        glScalef(0.12, 0.12, 1.8)
        glutSolidCube(25)
        glPopMatrix()
        
        # Claw-like Hand
        glTranslatef(0, 0, 45)
        glScalef(0.5, 0.5, 0.5)
        glutSolidCube(10)
        glPopMatrix()

    # 4. Legs 
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(0, side * 10, 40)
        
        # Hip Joint
        gluSphere(gluNewQuadric(), 6, 8, 8)
        
        # Thigh
        glRotatef(side * 5, 0, 1, 0)
        glPushMatrix()
        glScalef(0.2, 0.2, 2.0)
        glutSolidCube(30)
        glPopMatrix()
        
        # Knee Joint
        glTranslatef(0, 0, 55)
        glRotatef(-15 if not m['is_frozen'] else 0, 0, 1, 0)
        # Calf
        glPushMatrix()
        glScalef(0.15, 0.15, 2.2)
        glutSolidCube(30)
        glPopMatrix()
        glPopMatrix()
    
    glPopMatrix()


def player_in_safe_zone():
    for z in SAFE_ZONES:
        dx = char_pos[0] - z['pos'][0]
        dy = char_pos[1] - z['pos'][1]
        if math.sqrt(dx*dx + dy*dy) <= z['radius']:
            return True
    return False
def is_in_flashlight(m):
    if not flashlight_on: return False
    
    # Vector from character to mannequin
    dx = m['pos'][0] - char_pos[0]
    dy = m['pos'][1] - char_pos[1]
    dist = math.sqrt(dx*dx + dy*dy)
    
    if dist > 450: return False 
    
    angle_to_m = math.degrees(math.atan2(dy, dx))
    
    diff = (angle_to_m - char_rotation + 180) % 360 - 180
    
    return abs(diff) < 13 

def check_collision(x, y, radius):
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
        f_rad = (f['size'][0] + f['size'][1]) / 2 * 0.6 
        dist = math.sqrt((x-fx)**2 + (y-fy)**2)
        if dist < (radius + f_rad):
            return True
            
    return False

def update_game_logic():
    global bullets, ammo_count, ammo_pickups, mannequins, mannequins_killed, door_visible, door_pos
    global mannequins_spawned, spawn_timer, lives, game_over, damage_flash_timer
    global player_hidden, level, reveal_mode, reveal_timer

    if game_won or game_over:
        return

    # Check if player is currently in a safe zone
    player_hidden = player_in_safe_zone()
    if reveal_timer > 0:
        reveal_timer -= 1
        if reveal_timer == 0:
            reveal_mode = False


    # ------------------ Update Mannequins ------------------
    active_mannequins = []
    for m in mannequins:
        # Initialize wander angle if not present
        if 'wander_angle' not in m:
            m['wander_angle'] = random.uniform(0, 360)

        # Flashlight Check
        m['is_frozen'] = is_in_flashlight(m)

        if not m['is_frozen']:
            step = MANNEQUIN_SPEED
            
            if player_hidden:
                # --- STRROLLING LOGIC ---
                if random.random() < 0.05:
                    m['wander_angle'] += random.uniform(-40, 40)

                radw = math.radians(m['wander_angle'])
                dx = math.cos(radw)
                dy = math.sin(radw)

                nx = m['pos'][0] + dx * step
                ny = m['pos'][1] + dy * step

                # Stop mannequins from entering safe zones while wandering
                blocked_by_zone = False
                for z in SAFE_ZONES:
                    ddx = nx - z['pos'][0]
                    ddy = ny - z['pos'][1]
                    if math.sqrt(ddx*ddx + ddy*ddy) < (z['radius'] + 80):
                        blocked_by_zone = True
                        break
                
                if blocked_by_zone:
                    m['wander_angle'] += random.uniform(150, 210)
                    nx, ny = m['pos'][0], m['pos'][1]
            else:
                # --- CHASE LOGIC ---
                dx = char_pos[0] - m['pos'][0]
                dy = char_pos[1] - m['pos'][1]
                dist = math.sqrt(dx*dx + dy*dy)

                if dist > 5:
                    nx = m['pos'][0] + (dx/dist) * step
                    ny = m['pos'][1] + (dy/dist) * step
                else:
                    nx, ny = m['pos'][0], m['pos'][1]

            # Wall collision check
            wall_collision = False
            for wall in walls:
                if (nx + 20 > wall['x1'] and nx - 20 < wall['x2'] and
                    ny + 20 > wall['y1'] and ny - 20 < wall['y2']):
                    wall_collision = True
                    break

            if not wall_collision:
                m['pos'][0] = nx
                m['pos'][1] = ny

        dist_to_player = math.sqrt((char_pos[0]-m['pos'][0])**2 + (char_pos[1]-m['pos'][1])**2)
        if dist_to_player < 30:
            if not player_hidden:
                lives -= 1
                damage_flash_timer = 5
                m['pos'] = [random.uniform(-MAP_SIZE, MAP_SIZE), random.uniform(-MAP_SIZE, MAP_SIZE), 0]
                if lives <= 0:
                    game_over = True
            else:
                m['pos'] = [random.uniform(-MAP_SIZE, MAP_SIZE), random.uniform(-MAP_SIZE, MAP_SIZE), 0]

        active_mannequins.append(m)
    mannequins = active_mannequins

    # ------------------ Update Bullets ------------------
    bullet_speed = 30
    new_bullets = []
    for b in bullets:
        rad = math.radians(b['angle'])
        b['pos'][0] += bullet_speed * math.cos(rad)
        b['pos'][1] += bullet_speed * math.sin(rad)

        hit = False
        current_mannequins = []
        
        for m in mannequins:
            mdist = math.sqrt((b['pos'][0]-m['pos'][0])**2 + (b['pos'][1]-m['pos'][1])**2)
            
            if not hit and mdist < 40:
                hit = True # Bullet is consumed regardless
                
                if player_hidden:
                    current_mannequins.append(m)
                else:
                    mannequins_killed += 1
                    if mannequins_killed >= MANNEQUIN_COUNT:
                        if level < MAX_LEVEL:
                            start_next_level()
                        else:
                            door_visible = True
                            door_pos[0], door_pos[1], door_pos[2] = MAP_SIZE - 300, MAP_SIZE - 100, 0
            else:
                current_mannequins.append(m)

        mannequins = current_mannequins

        # Respawn Logic
        if mannequins_killed < MANNEQUIN_COUNT and len(mannequins) < 3 and mannequins_spawned < MANNEQUIN_COUNT:
            spawn_pos = [0, 0, 0]
            valid = False
            for _ in range(10):
                spawn_pos = [random.uniform(-MAP_SIZE, MAP_SIZE), random.uniform(-MAP_SIZE, MAP_SIZE), 0]
                if not check_collision(spawn_pos[0], spawn_pos[1], 30) and \
                   math.sqrt((spawn_pos[0]-char_pos[0])**2 + (spawn_pos[1]-char_pos[1])**2) > 400 and \
                   not any(math.sqrt((spawn_pos[0]-z['pos'][0])**2 + (spawn_pos[1]-z['pos'][1])**2) < (z['radius'] + 120) for z in SAFE_ZONES):
                    valid = True
                    break
            if valid:
                mannequins.append({
                    'pos': spawn_pos,
                    'is_frozen': False,
                    'wander_angle': random.uniform(0, 360)
                })
                mannequins_spawned += 1

        if not hit and abs(b['pos'][0]) < MAP_SIZE and abs(b['pos'][1]) < MAP_SIZE:
            new_bullets.append(b)

    bullets = new_bullets

    # ------------------ Update Pickups ------------------
    remaining_pickups = []
    for p in ammo_pickups:
        p['rotation'] += 2
        dist = math.sqrt((char_pos[0] - p['pos'][0])**2 + (char_pos[1] - p['pos'][1])**2)

        if dist < PICKUP_RADIUS and (ammo_count < 10 or lives < 5):
            if ammo_count < 10: ammo_count += 5
            if lives < 5: lives += 1
        else:
            remaining_pickups.append(p)
    ammo_pickups = remaining_pickups

def start_next_level():
    global level, mannequins_killed, mannequins_spawned, mannequins, door_visible
    global MANNEQUIN_SPEED, door_pos

    level += 1
    mannequins_killed = 0
    mannequins_spawned = 0
    
    # Increase difficulty
    MANNEQUIN_SPEED += 0.35

    # Re-spawn mannequins for the new level
    mannequins = []
    for _ in range(MANNEQUIN_COUNT):
        mannequins.append({
            'pos': [random.uniform(-MAP_SIZE+200, MAP_SIZE-200), 
                    random.uniform(-MAP_SIZE+200, MAP_SIZE-200), 0],
            'is_frozen': False,
            'is_active': False,
            'is_attacker': True,
            'alive': True
        })

    if level > MAX_LEVEL:
        door_visible = True
        door_pos = [MAP_SIZE - 300, MAP_SIZE - 100, 0]
        
def draw_safe_zones():
    glColor3f(0.0, 0.6, 1.0)  # Bright Cyan/Blue (solid)
    glLineWidth(3.0)

    for z in SAFE_ZONES:
        glPushMatrix()
        glTranslatef(z['pos'][0], z['pos'][1], 0.5)
        
        glBegin(GL_LINE_LOOP)
        segments = 32
        for i in range(segments):
            angle = 2.0 * math.pi * i / segments
            glVertex3f(math.cos(angle) * z['radius'], math.sin(angle) * z['radius'], 0)
        glEnd()
        
        glBegin(GL_LINE_LOOP)
        for i in range(segments):
            angle = 2.0 * math.pi * i / segments
            glVertex3f(math.cos(angle) * z['radius'] * 0.7, math.sin(angle) * z['radius'] * 0.7, 0)
        glEnd()
        
        glPopMatrix()

    glLineWidth(1.0) 





def draw_door():
    if not door_visible: return
    glPushMatrix()
    glTranslatef(door_pos[0], door_pos[1], door_pos[2])
    glRotatef(180, 0, 0, 1)

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
    glColor3f(0.25, 0.15, 0.05)
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
    glBegin(GL_POLYGON)
    for i in range(16):
        angle = (2 * math.pi * i) / 16
        glVertex3f(15 * math.cos(angle), 15 * math.sin(angle), 0)
    glEnd()
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
    glColor3f(1, 1, 0)
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
    glColor3f(1.0, 1.0, 0.3)  # Bright yellow
    glPushMatrix()
    glRotatef(180, 1, 0, 0)  # Point down
    # Draw just the outline
    glBegin(GL_LINES)
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        x_top = 10 * math.cos(rad)
        y_top = 10 * math.sin(rad)
        x_bottom = 150 * math.cos(rad)
        y_bottom = 150 * math.sin(rad)
        glVertex3f(x_top, y_top, 0)
        glVertex3f(x_bottom, y_bottom, 250)
    glEnd()
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
    glTranslatef(0, 0, 325)  
    
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
    glPushMatrix(); glTranslatef(0, 0, 30); glRotatef(-90, 1, 0, 0);gluCylinder(gluNewQuadric(), 20, 5, 45, 20, 20) 
    glPopMatrix()
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
        glColor3f(0.5, 0.7, 0.9)
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
    if reveal_mode:
        return
    glPushMatrix()
    glTranslatef(char_pos[0], char_pos[1], 0.1) 
    
    glColor3f(0.0, 0.0, 0.0) 
    
    view_r = 500    # How far the ground is visible around Mono
    map_limit = 4000 
    
    glBegin(GL_QUADS)
    # North Quad (Top)
    glVertex3f(-map_limit, map_limit, 0)
    glVertex3f(map_limit, map_limit, 0)
    glVertex3f(map_limit, view_r, 0)
    glVertex3f(-map_limit, view_r, 0)
    
    # South Quad (Bottom)
    glVertex3f(-map_limit, -view_r, 0)
    glVertex3f(map_limit, -view_r, 0)
    glVertex3f(map_limit, -map_limit, 0)
    glVertex3f(-map_limit, -map_limit, 0)
    
    # West Quad (Left)
    glVertex3f(-map_limit, view_r, 0)
    glVertex3f(-view_r, view_r, 0)
    glVertex3f(-view_r, -view_r, 0)
    glVertex3f(-map_limit, -view_r, 0)
    
    # East Quad (Right)
    glVertex3f(view_r, view_r, 0)
    glVertex3f(map_limit, view_r, 0)
    glVertex3f(map_limit, -view_r, 0)
    glVertex3f(view_r, -view_r, 0)
    glEnd()
    
    glPopMatrix()

def draw_character():
    glPushMatrix()
    glTranslatef(char_pos[0], char_pos[1], char_pos[2])
    glRotatef(char_rotation, 0, 0, 1)

    if player_in_safe_zone():
        body_color = (0.28, 0.27, 0.22)
        head_color = (0.52, 0.50, 0.46)

    else:
        body_color = (0.25, 0.2, 0.1)  # Normal body
        head_color = (0.5, 0.4, 0.3)   # Normal head

    glColor3f(*body_color)
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(0, side * 8, 15)
        glScalef(0.4, 0.4, 1.5)
        glutSolidCube(20)
        glPopMatrix()

    glColor3f(*body_color)
    glPushMatrix()
    glTranslatef(0, 0, 50)
    glScalef(1, 0.8, 1.8)
    gluSphere(gluNewQuadric(), 25, 12, 12) 
    glPopMatrix()

    # HEAD
    if not is_first_person:
        glColor3f(*head_color)
        glPushMatrix()
        glTranslatef(0, 0, 95)
        glScalef(1.1, 1, 1.2)
        glutSolidCube(40)
        glPopMatrix()
    if flashlight_on:
        glPushMatrix()
        glTranslatef(20, 10, 50)  # X=forward, Y=right, Z=up in local space
        
        
        glColor3f(1.0, 1.0, 0.6)
        glLineWidth(2.0)
        
        glBegin(GL_LINES)
        num_rays = 16
        for i in range(num_rays):
            angle = (2 * math.pi * i) / num_rays
            # Circle on YZ plane
            y_base = 5 * math.cos(angle)
            z_base = 5 * math.sin(angle)
            y_top = 100 * math.cos(angle)
            z_top = 100 * math.sin(angle)
            
            glVertex3f(0, y_base, z_base)
            glVertex3f(450, y_top, z_top)
        glEnd()
        
        for distance in [150, 300, 450]:
            radius = 5 + (distance / 450) * 95
            glBegin(GL_LINE_LOOP)
            for i in range(32):
                angle = (2 * math.pi * i) / 32
                y = radius * math.cos(angle)
                z = radius * math.sin(angle)
                glVertex3f(distance, y, z)
            glEnd()
        
        glLineWidth(1.0)
        glPopMatrix()        
    glPopMatrix()


def draw_crosshair():
    if not is_first_person or not game_started or game_won or game_over:
        return

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_DEPTH_TEST)
    glColor3f(1.0, 1, 1) # Bright Red
    glLineWidth(2.0)

    # Draw Crosshair
    glBegin(GL_LINES)
    # Horizontal line
    glVertex2f(490, 400); glVertex2f(510, 400)
    # Vertical line
    glVertex2f(500, 390); glVertex2f(500, 410)
    glEnd()

    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_damage_overlay():
    global damage_flash_timer
    if damage_flash_timer > 0:
        damage_flash_timer -= 1
        glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity()
        gluOrtho2D(0, 1000, 0, 800)
        glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity()
        
        glDisable(GL_DEPTH_TEST)
        glColor3f(1.0, 0.0, 0.0)  # Solid red
        glLineWidth(10.0)
        
        # Draw thick red border frame
        glBegin(GL_LINE_LOOP)
        glVertex2f(10, 10)
        glVertex2f(990, 10)
        glVertex2f(990, 790)
        glVertex2f(10, 790)
        glEnd()
        
        draw_text(420, 400, "!!! DAMAGE !!!")

        
        
        glLineWidth(1.0)
        glEnable(GL_DEPTH_TEST)
        
        glPopMatrix(); glMatrixMode(GL_PROJECTION); glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    
    glEnable(GL_DEPTH_TEST)
    setupCamera()
    if game_started and not game_won and not game_over:
        update_game_logic()
    
    # 3. Draw 3D Environment
    draw_house()
    draw_safe_zones()
    
    # Draw interactive entities
    for m in mannequins: 
        draw_mannequin(m)
        
    for p in ammo_pickups:
        glPushMatrix()
        glTranslatef(p['pos'][0], p['pos'][1], p['pos'][2])
        glRotatef(p['rotation'], 0, 0, 1)
        glColor3f(0.1, 0.6, 0.1)
        glutSolidCube(20)
        glPopMatrix()
        
    for b in bullets:
        glPushMatrix()
        glTranslatef(b['pos'][0], b['pos'][1], b['pos'][2])
        glColor3f(1, 1, 0.5)
        gluSphere(gluNewQuadric(), 4, 8, 8)
        glPopMatrix()

    # Draw Main Characters
    draw_character() # Mono
    draw_door()
    draw_girl()
    
    draw_visibility_circle()
    
    draw_damage_overlay()
    draw_crosshair()
    
    if not intro_finished:
        pass
        
    elif intro_finished and not game_started:
        draw_text(350, 550, "--- MONO: Little Nightmare ---")
        draw_text(380, 500, "CONTROLS:")
        draw_text(380, 470, "[SPACE] - Start Game / Shoot")
        draw_text(380, 440, "[V]     - Reload Ammo")
        draw_text(380, 410, "[F]     - Toggle Flashlight")
        draw_text(380, 380, "[WASD]  - Move Mono")
        draw_text(380, 350, "[ARROWS]- Adjust Camera")
        draw_text(380, 320, "[E]     - Toggle Camera")
        draw_text(380, 290, "[K]     - Reveal Entire Map")  # ADD THIS


        
        if (blink_timer // 30) % 2 == 0:  # Blink every 30 frames
            draw_text(360, 250, "PRESS E TO START THE GAME")
            
    elif game_won:
        draw_text(350, 400, "RESCUED, YOU WIN")
        draw_text(380, 370, "Press 'R' to Play Again")
        
    elif game_over:
        draw_text(300, 400, "YOU COULDN'T RESCUE HER, YOU LOSE")
        draw_text(380, 370, "Press 'R' to Play Again")
        
    else:
        # ACTIVE GAMEPLAY UI
        draw_text(20, 750, f"LEVEL: {level}/{MAX_LEVEL} | LIVES: {lives} | KILLED: {mannequins_killed}/{MANNEQUIN_COUNT} | AMMO: {ammo_count}")        
        if reveal_mode:
            glColor3f(0.0, 1.0, 1.0)  # Cyan color for active ability
            draw_text(350, 50, f"MAP REVEALED: {reveal_timer // 60 + 1}s")
        else:
            draw_text(380, 50, "Press [K] to Reveal Map")

        if ammo_count <= 0:
            glColor3f(1.0, 0.0, 0.0) # Red text for warning
            draw_text(350, 450, "!!! OUT OF AMMO !!!")
            draw_text(385, 420, "Press 'V' to Reload")

    # Final Buffer Swap
    glutSwapBuffers()

def setupCamera():
    global intro_factor, intro_finished, is_first_person
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    # Use a wider Field of View for First Person to see more around you
    fov = 95 if is_first_person else 65
    gluPerspective(fov, 1.25, 1.0, 5000)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    rad = math.radians(char_rotation)

    if is_first_person:
        # --- FIRST PERSON LOGIC ---
        cx = char_pos[0] + 25 * math.cos(rad) # Offset forward slightly
        cy = char_pos[1] + 25 * math.sin(rad)
        cz = 90 # Head height
        
        # Look forward based on rotation
        tx = cx + 100 * math.cos(rad)
        ty = cy + 100 * math.sin(rad)
        tz = cz
        gluLookAt(cx, cy, cz, tx, ty, tz, 0, 0, 1)
    
    else:
        # --- THIRD PERSON LOGIC ---
        ideal_cam_dist = 450
        target_x = (char_pos[0] - ideal_cam_dist * math.cos(rad)) + (camera_pan * math.sin(rad))
        target_y = (char_pos[1] - ideal_cam_dist * math.sin(rad)) - (camera_pan * math.cos(rad))
        target_z = camera_pos[2]

        actual_dist = ideal_cam_dist
        if abs(target_x) > MAP_SIZE - 30 or abs(target_y) > MAP_SIZE - 30:
            actual_dist = 150 

        target_x = (char_pos[0] - actual_dist * math.cos(rad)) + (camera_pan * math.sin(rad))
        target_y = (char_pos[1] - actual_dist * math.sin(rad)) - (camera_pan * math.cos(rad))

        if not intro_finished:
            current_x = camera_start_pos[0] + (target_x - camera_start_pos[0]) * intro_factor
            current_y = camera_start_pos[1] + (target_y - camera_start_pos[1]) * intro_factor
            current_z = camera_start_pos[2] + (target_z - camera_start_pos[2]) * intro_factor
            intro_factor += intro_speed
            if intro_factor >= 1.0:
                intro_factor = 1.0
                intro_finished = True
            cx, cy, cz = current_x, current_y, current_z
        else:
            cx, cy, cz = target_x, target_y, target_z
        tx, ty, tz = char_pos[0], char_pos[1], char_pos[2] + 50
        
        gluLookAt(cx, cy, cz, tx, ty, tz, 0, 0, 1)

def keyboardListener(key, x, y):
    global char_pos, char_rotation, flashlight_on, ammo_count, bullets, game_won, game_started, is_first_person, reveal_timer, reveal_mode
    
    if not intro_finished:
        return
        
    key = key.lower()
    
    if key == b'e':
        if not game_started:
            game_started = True
            is_first_person = True
        else:
            is_first_person = not is_first_person
        return

    if not game_started:
        if key == b' ':
            game_started = True
        return 
    if key == b'r':
        init_game()
        return
        
    if key == b'v' and ammo_count <= 0:
        ammo_count = 10
    if key == b'k':
        if not reveal_mode and not game_won and not game_over:
            reveal_mode = True
            reveal_timer = REVEAL_DURATION
        return


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
        char_pos[0], char_pos[1] = nx, ny
        
    if key == b'a': char_rotation += 7
    if key == b'd': char_rotation -= 7
    if key == b'f': flashlight_on = not flashlight_on
    if key == b' ' and ammo_count > 0:
        ammo_count -= 1
        bx = char_pos[0] + 30 * math.cos(rad)
        by = char_pos[1] + 30 * math.sin(rad)
        bullets.append({'pos': [bx, by, 55], 'angle': char_rotation})
            
    if key == b'p' and door_visible:
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
    glutInitWindowSize(1000, 800); glutCreateWindow(b"MONO: Little Nightmare ")
    glutDisplayFunc(showScreen); glutIdleFunc(lambda: glutPostRedisplay())
    glutKeyboardFunc(keyboardListener); glutSpecialFunc(specialKeyListener)
    glutMainLoop()

if __name__ == "__main__": main()
