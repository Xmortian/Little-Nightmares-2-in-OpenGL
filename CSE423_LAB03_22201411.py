from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
import random
import math


# Camera-related variables
camera_pos = (0,500,500)

fovY = 90  # Field of view
GRID_LENGTH = 800  # Length of grid lines
rand_var = 423

player_x = 0
player_y = 0
player_speed = 10

enemies = [[random.randint(-500, 500), random.randint(-500, 500), 1.0, True] for _ in range(5)]
bullets = []
player_angle = 0

cam_angle = math.radians(90)
cam_height = 600
cam_radius = 800
first_person = False

is_game_over = False
player_lives = 5
game_score =0
total_bullet_missed =0

cheat_mode = False
auto_cam_follow = False
player_angle = 0 
player_movement_angle=0 


def draw_text(x,y,text,font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(0,1,0)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_shapes():
    glPushMatrix()  # Save the current matrix state
    glTranslatef(0,0,40)
    if is_game_over:
        glRotatef(90,1,0, 0) # lie flat on the ground to simulate death
        glTranslatef(0,0,-30)
    # Body
    glColor3f(0.33,0.42, 0.18)
    glPushMatrix()
    glScalef(0.6,0.3, 1.0)
    glutSolidCube(60)
    glPopMatrix()
    # head
    glColor3f(0,0,0)
    glPushMatrix()
    glTranslatef(0,0,50)
    gluSphere(gluNewQuadric(),15,20,20)
    glPopMatrix()
    #3 legs
    glColor3f(0,0,1) # Blue
    glPushMatrix()
    glTranslatef(-12, 0, -30)
    gluCylinder(gluNewQuadric(),8, 5,30,10, 10) 
    glPopMatrix()
    glPushMatrix()
    glTranslatef(12, 0, -30)
    gluCylinder(gluNewQuadric(), 8,5,30,10,10)
    glPopMatrix()
    #4 arms
    glColor3f(0.8,0.7,0.6)
    # Left Arm
    glPushMatrix()
    glTranslatef(-25, 0, 20)
    glScalef(0.2, 0.2, 0.5)
    glutSolidCube(40)
    glPopMatrix()
    # Right Arm
    glPushMatrix()
    glTranslatef(25,0, 20)
    glScalef(0.2, 0.2, 0.5)
    glutSolidCube(40)
    glPopMatrix()
    #5 gun
    glColor3f(0.7,0.7,0.7)
    glPushMatrix()
    glTranslatef(0,50,20)
    glScalef(.8,1.1,0.4)  
    glutSolidCube(40)
    glPopMatrix()
    glPopMatrix()  # Restore the previous matrix state

def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    global player_x, player_y, player_angle, player_movement_angle, is_game_over, player_lives, game_score, total_bullet_missed, cheat_mode, auto_cam_follow
    if key == b'r' or key == b'R':
        player_lives =5
        game_score = 0
        total_bullet_missed = 0
        is_game_over = False
        player_x, player_y = 0, 0
        player_angle =0
        player_movement_angle = 0
        print("Game Restarted!")
    if not is_game_over:
        if not cheat_mode:
            if key == b'a': 
                player_angle +=7
                player_movement_angle = player_angle
            if key == b'd': 
                player_angle -=7
                player_movement_angle=player_angle
        else:
            if key == b'a':
                player_movement_angle+=7
            if key == b'd':
                player_movement_angle-=7
        
        rad = math.radians(player_movement_angle)
        new_x, new_y=player_x, player_y
        
        if key == b'w':
            new_x += player_speed*math.sin(rad)
            new_y += player_speed * math.cos(rad)
        if key == b's':
            new_x -= player_speed * math.sin(rad)
            new_y -= player_speed * math.cos(rad)
            
        if key == b'c' or key == b'C':
            cheat_mode = not cheat_mode
            if not cheat_mode:
                auto_cam_follow = False
                player_movement_angle = player_angle
            print(f"Cheat Mode: {'ON' if cheat_mode else 'OFF'}")
            
        if key == b'v' or key == b'V':
            if cheat_mode:
                auto_cam_follow = not auto_cam_follow
                print(f"Auto Camera Follow: {'ON' if auto_cam_follow else 'OFF'}")
            else:
                print("Auto Camera Follow only works in Cheat Mode!")

        buffer = 30
        
        if -GRID_LENGTH + buffer < new_x < GRID_LENGTH - buffer:
            player_x = new_x
            
        if -GRID_LENGTH + buffer < new_y < GRID_LENGTH - buffer:
            player_y = new_y

    glutPostRedisplay()

def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global cam_angle, cam_height
    # Orbit rotation around the grid
    if key == GLUT_KEY_LEFT:
        cam_angle += 0.05
    if key == GLUT_KEY_RIGHT:
        cam_angle -= 0.05   
    # Vertical height control up and down
    if key == GLUT_KEY_UP:
        cam_height +=10
    if key == GLUT_KEY_DOWN:
        cam_height -= 10
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
    global bullets, player_x, player_y, player_angle, first_person    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        gun_offset = 30
        rad = math.radians(player_angle)
        spawn_x = player_x - gun_offset * math.sin(rad)
        spawn_y = player_y + gun_offset * math.cos(rad)
        bullets.append([spawn_x, spawn_y, player_angle])
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person = not first_person

def setupCamera():
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25,0.1,2000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    if first_person:
        rad = math.radians(player_angle)
        eye_x = player_x - 40 * math.sin(rad)
        eye_y = player_y + 40 * math.cos(rad)
        eye_z = 70
        look_x = eye_x -1000 * math.sin(rad)
        look_y = eye_y+1000 * math.cos(rad)
        look_z =70
        gluLookAt(eye_x, eye_y, eye_z, look_x, look_y, look_z, 0,0,1)
    elif auto_cam_follow:
        rad = math.radians(player_angle)
        eye_x = player_x+150 * math.sin(rad)
        eye_y = player_y-150 * math.cos(rad)
        eye_z=200  
        look_x = player_x-500 * math.sin(rad)
        look_y = player_y+500 * math.cos(rad)
        look_z=80 
        gluLookAt(eye_x, eye_y, eye_z, look_x, look_y, look_z, 0,0,1)
    else:
        eye_x = cam_radius * math.cos(cam_angle)
        eye_y = cam_radius * math.sin(cam_angle)
        eye_z = cam_height
        gluLookAt(eye_x, eye_y, eye_z, player_x, player_y,40,0,0,1)

def idle():
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    global player_lives, is_game_over, enemies, bullets, total_bullet_missed, game_score, player_angle, cheat_mode
    if is_game_over:
        return 
    
    if cheat_mode:
    # 1. Continuously rotate the gun 360
        player_angle = (player_angle + 2) % 360
        rad = math.radians(player_angle)
        # Direction vector of the gun
        dir_x, dir_y = -math.sin(rad), math.cos(rad)
        should_fire = False
        target_enemy = None
        for e in enemies:
            ve_x, ve_y = e[0] - player_x, e[1] - player_y
            dist = math.sqrt(ve_x**2 + ve_y**2)
            if dist > 0:
                ve_x, ve_y = ve_x/dist, ve_y/dist
                dot = dir_x * ve_x + dir_y * ve_y
                if dot > 0.995:
                    bullet_exists = False
                    for b in bullets:
                        angle_diff = abs(b[2]-player_angle)
                        if angle_diff > 180:
                            angle_diff = 360-angle_diff
                        if angle_diff < 10: 
                            bullet_to_enemy_x = e[0] - b[0]
                            bullet_to_enemy_y = e[1] - b[1]
                            bullet_to_enemy_dist = math.sqrt(bullet_to_enemy_x**2 + bullet_to_enemy_y**2)
                            if bullet_to_enemy_dist < dist: 
                                bullet_exists = True
                                break
                    if not bullet_exists:
                        should_fire = True
                        target_enemy = e
                        break  
        if should_fire:
            gun_offset = 30
            spawn_x = player_x - gun_offset*math.sin(rad)
            spawn_y = player_y + gun_offset*math.cos(rad)
            bullets.append([spawn_x, spawn_y, player_angle])
            print("Cheat Mode: Player Bullet Fired!")
    # enemy player collision detection
    for i in range(len(enemies)):
        dx = player_x - enemies[i][0]
        dy = player_y - enemies[i][1]
        dist = math.sqrt(dx**2 + dy**2)
        if dist<40: 
            player_lives -= 1
            print(f"Remaining Player Life: {player_lives}") # Console update
            # Enemy shall  despawn and respawns at a new random point
            enemies[i][0] = random.randint(-GRID_LENGTH, GRID_LENGTH)
            enemies[i][1] = random.randint(-GRID_LENGTH, GRID_LENGTH)
    if player_lives <= 0 or total_bullet_missed>=1000:
        is_game_over = True
    for b in bullets:
        rad = math.radians(b[2])
        b[0] -= 15 * math.sin(rad)
        b[1] += 15 * math.cos(rad)

    # colission bullet and enemy

    for b in bullets[:]:
        hit_enemy = False
        for i in range(len(enemies)):
            dist_to_enemy = math.sqrt((b[0] - enemies[i][0])**2 + (b[1] - enemies[i][1])**2)
            if dist_to_enemy < 300:
                game_score += 1
                print(f"Enemy Hit! Score: {game_score}")
                enemies[i][0] = random.randint(-GRID_LENGTH, GRID_LENGTH)
                enemies[i][1] = random.randint(-GRID_LENGTH, GRID_LENGTH)
                hit_enemy = True
                break
        
        if hit_enemy:
            bullets.remove(b)
        elif abs(b[0]) > GRID_LENGTH or abs(b[1]) > GRID_LENGTH:
            total_bullet_missed += 1 # Increment total missed bullets
            print(f"Bullet missed: {total_bullet_missed}")
            bullets.remove(b)

    for i in range(len(enemies)):
        dx = player_x - enemies[i][0]
        dy = player_y - enemies[i][1]
        dist = math.sqrt(dx**2 + dy**2)
        
        if dist > 0:
            next_x = enemies[i][0] + (dx / dist) * .05
            next_y = enemies[i][1] + (dy / dist) * .05
            enemy_buffer = 25
            if -GRID_LENGTH + enemy_buffer < next_x < GRID_LENGTH - enemy_buffer:
                enemies[i][0] = next_x
            if -GRID_LENGTH + enemy_buffer < next_y < GRID_LENGTH - enemy_buffer:
                enemies[i][1] = next_y
            
        if enemies[i][3]:
            enemies[i][2]+=0.01
            if enemies[i][2] > 1.5: enemies[i][3] = False
        else:
            enemies[i][2] -= 0.01
            if enemies[i][2] < 0.5: enemies[i][3] = True

    
            
    glutPostRedisplay()



def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity() 
    glViewport(0, 0, 1000, 800)  # Set viewport size
    setupCamera()
    # checkboard floor draw
    tile_size = 100
    num_tiles = int(GRID_LENGTH / tile_size)

    glBegin(GL_QUADS)
    for i in range(-num_tiles, num_tiles):
        for j in range(-num_tiles, num_tiles):
            if (i + j) % 2 == 0:
                glColor3f(1,1,1)
            else:
                glColor3f(0.7, 0.5, 0.95)
            
            glVertex3f(i * tile_size, j * tile_size, 0)
            glVertex3f((i + 1) * tile_size, j * tile_size, 0)
            glVertex3f((i + 1) * tile_size, (j + 1) * tile_size, 0)
            glVertex3f(i * tile_size, (j + 1) * tile_size, 0)
    glEnd()

    # draw boundaries
    wall_h = 100
    glBegin(GL_QUADS)
    
    glColor3f(0,1,1)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, wall_h)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, wall_h)

    glColor3f(0.2, 0.2, 0.2) 
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, wall_h)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, wall_h)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, wall_h)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, wall_h)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, wall_h)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, wall_h)
    glEnd()
    glPushMatrix()
    glTranslatef(player_x, player_y, 40)
    glRotatef(player_angle, 0, 0, 1) 
    draw_shapes() 
    glPopMatrix()
    
    for e in enemies:
        draw_enemy(e[0], e[1], e[2])
        
    glColor3f(0, 1, 1)
    for b in bullets:
        glPushMatrix()
        glTranslatef(b[0], b[1], 20) 
        glutSolidCube(15)
        glPopMatrix()
    draw_text(10, 770, f"Player Life Remaining: {player_lives}")
    draw_text(10, 740, f"Game Score: {game_score}")
    draw_text(10, 710, f"Player Bullet Missed: {total_bullet_missed}")
    
    if is_game_over:
        draw_text(550, 550, "GAME OVER - Press R to Restart", GLUT_BITMAP_HELVETICA_18)
    glutSwapBuffers()


def draw_enemy(x, y, scale):
    glPushMatrix()
    glTranslatef(x, y, 20)  
    glScalef(scale, scale, scale)
    glColor3f(1.0, 0.0, 0.0) 
    glutSolidSphere(30, 20, 20) 
    glColor3f(0.0, 0.0, 0.0) 
    glPushMatrix()
    glTranslatef(0, 5, 10) 
    glutSolidSphere(15, 20, 20)
    glPopMatrix()
    glPopMatrix()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"3D OpenGL Intro")  # Create the window

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()
