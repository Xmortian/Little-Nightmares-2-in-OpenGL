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

# Bullet & Ammo System
ammo_count = 10
bullets = [] 
ammo_pickups = []
PICKUP_COUNT = 15
PICKUP_RADIUS = 50 

# Mannequin System
mannequins = []
MANNEQUIN_COUNT = 10
MANNEQUIN_SPEED = 2.5

# Map Settings
MAP_SIZE = 2500 
OBJECT_COUNT = 50
random.seed(423)

obstacles = []
for _ in range(OBJECT_COUNT):
    obstacles.append({
        'pos': (random.uniform(-MAP_SIZE, MAP_SIZE), random.uniform(-MAP_SIZE, MAP_SIZE)),
        'size': random.uniform(30, 80),
        'color': (random.uniform(0.05, 0.1), random.uniform(0.05, 0.1), random.uniform(0.1, 0.15))
    })

for _ in range(PICKUP_COUNT):
    ammo_pickups.append({
        'pos': [random.uniform(-MAP_SIZE, MAP_SIZE), random.uniform(-MAP_SIZE, MAP_SIZE), 10],
        'rotation': 0
    })

# Initialize Mannequins
for _ in range(MANNEQUIN_COUNT):
    mannequins.append({
        'pos': [random.uniform(-MAP_SIZE, MAP_SIZE), random.uniform(-MAP_SIZE, MAP_SIZE), 0],
        'is_frozen': False
    })

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
    
    if dist > 500: return False # Out of light range
    
    # Angle of the mannequin relative to player
    angle_to_m = math.degrees(math.atan2(dy, dx))
    
    # Normalized angle difference
    diff = (angle_to_m - char_rotation + 180) % 360 - 180
    
    return abs(diff) < 25 # Flashlight beam width is ~50 degrees

def update_game_logic():
    global bullets, ammo_count, ammo_pickups, mannequins
    
    # Update Mannequins
    for m in mannequins:
        m['is_frozen'] = is_in_flashlight(m)
        
        if not m['is_frozen']:
            # Move toward player
            dx = char_pos[0] - m['pos'][0]
            dy = char_pos[1] - m['pos'][1]
            dist = math.sqrt(dx*dx + dy*dy)
            if dist > 5:
                m['pos'][0] += (dx/dist) * MANNEQUIN_SPEED
                m['pos'][1] += (dy/dist) * MANNEQUIN_SPEED

    # Update Bullets
    bullet_speed = 30
    new_bullets = []
    for b in bullets:
        rad = math.radians(b['angle'])
        b['pos'][0] += bullet_speed * math.cos(rad)
        b['pos'][1] += bullet_speed * math.sin(rad)
        
        # Bullet vs Mannequin collision
        hit = False
        for m in mannequins:
            mdist = math.sqrt((b['pos'][0]-m['pos'][0])**2 + (b['pos'][1]-m['pos'][1])**2)
            if mdist < 40:
                m['pos'] = [random.uniform(-MAP_SIZE, MAP_SIZE), random.uniform(-MAP_SIZE, MAP_SIZE), 0]
                hit = True
                break
        
        if not hit and abs(b['pos'][0]) < MAP_SIZE and abs(b['pos'][1]) < MAP_SIZE:
            new_bullets.append(b)
    bullets = new_bullets

    # Update Pickups
    remaining_pickups = []
    for p in ammo_pickups:
        p['rotation'] += 2
        dist = math.sqrt((char_pos[0] - p['pos'][0])**2 + (char_pos[1] - p['pos'][1])**2)
        if dist < PICKUP_RADIUS:
            ammo_count += 5
        else:
            remaining_pickups.append(p)
    ammo_pickups = remaining_pickups

def draw_visibility_circle():
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

def draw_character():
    glPushMatrix()
    glTranslatef(char_pos[0], char_pos[1], char_pos[2])
    glRotatef(char_rotation, 0, 0, 1)
    # Legs
    glColor3f(0.15, 0.1, 0.05)
    for side in [-1, 1]:
        glPushMatrix(); glTranslatef(0, side * 8, 15); glScalef(0.4, 0.4, 1.5); glutSolidCube(20); glPopMatrix()
    # Body
    glColor3f(0.25, 0.2, 0.1)
    glPushMatrix(); glTranslatef(0, 0, 50); glScalef(1, 0.8, 1.8); gluSphere(gluNewQuadric(), 25, 12, 12); glPopMatrix()
    # Head
    glPushMatrix(); glTranslatef(0, 0, 95); glColor3f(0.5, 0.4, 0.3); glScalef(1.1, 1, 1.2); glutSolidCube(40); glPopMatrix()
    # Flashlight
    if flashlight_on:
        glPushMatrix(); glTranslatef(25, 15, 55); glRotatef(90, 0, 1, 0); glColor4f(1.0, 1.0, 0.8, 0.4); gluCylinder(gluNewQuadric(), 5, 100, 450, 20, 1); glPopMatrix()
    glPopMatrix()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST); glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    update_game_logic()
    setupCamera()
    
    # Ground & Environment
    glBegin(GL_QUADS)
    for i in range(-MAP_SIZE, MAP_SIZE, 100):
        for j in range(-MAP_SIZE, MAP_SIZE, 100):
            glColor3f(0.02, 0.02, 0.03) if (i+j)%200==0 else glColor3f(0.04, 0.04, 0.06)
            glVertex3f(i, j, 0); glVertex3f(i+100, j, 0); glVertex3f(i+100, j+100, 0); glVertex3f(i, j+100, 0)
    glEnd()

    for m in mannequins: draw_mannequin(m)
    for p in ammo_pickups:
        glPushMatrix(); glTranslatef(p['pos'][0], p['pos'][1], p['pos'][2]); glRotatef(p['rotation'], 0, 0, 1); glColor3f(0.1, 0.6, 0.1); glutSolidCube(20); glPopMatrix()
    for b in bullets:
        glPushMatrix(); glTranslatef(b['pos'][0], b['pos'][1], b['pos'][2]); glColor3f(1, 1, 0.5); gluSphere(gluNewQuadric(), 4, 8, 8); glPopMatrix()

    draw_character()
    draw_visibility_circle()
    draw_text(20, 750, f"AMMO: {ammo_count} | BEAM FREEZES MANNEQUINS")
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
    global char_pos, char_rotation, flashlight_on, ammo_count, bullets
    move_speed = 18
    rad = math.radians(char_rotation)
    if key == b'w': char_pos[0] += move_speed * math.cos(rad); char_pos[1] += move_speed * math.sin(rad)
    if key == b's': char_pos[0] -= move_speed * math.cos(rad); char_pos[1] -= move_speed * math.sin(rad)
    if key == b'a': char_rotation += 7
    if key == b'd': char_rotation -= 7
    if key == b'f': flashlight_on = not flashlight_on
    if key == b' ' and ammo_count > 0:
        ammo_count -= 1
        bullets.append({'pos': [char_pos[0], char_pos[1], 55], 'angle': char_rotation})

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