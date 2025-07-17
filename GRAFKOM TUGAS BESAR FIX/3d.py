from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

angle_x, angle_y = 0, 0
pos_x, pos_y, pos_z = 0, 0, -5
mouse_down = False
last_x, last_y = 0, 0
scale = 1.0

current_object = 0
obj_model = []

current_color = [0.8, 0.4, 0.2]
light_ambient = [0.2, 0.2, 0.2, 1.0]
light_diffuse = [0.7, 0.7, 0.7, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [1.0, 1.0, 1.0, 0.0]
lighting_enabled = True

def draw_cube():
    glBegin(GL_QUADS)
    glNormal3f(0, 0, 1)
    glVertex3f(-1, -1,  1)
    glVertex3f( 1, -1,  1)
    glVertex3f( 1,  1,  1)
    glVertex3f(-1,  1,  1)
    glNormal3f(0, 0, -1)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1,  1, -1)
    glVertex3f( 1,  1, -1)
    glVertex3f( 1, -1, -1)
    glNormal3f(0, 1, 0)
    glVertex3f(-1,  1, -1)
    glVertex3f(-1,  1,  1)
    glVertex3f( 1,  1,  1)
    glVertex3f( 1,  1, -1)
    glNormal3f(0, -1, 0)
    glVertex3f(-1, -1, -1)
    glVertex3f( 1, -1, -1)
    glVertex3f( 1, -1,  1)
    glVertex3f(-1, -1,  1)
    glNormal3f(-1, 0, 0)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, -1,  1)
    glVertex3f(-1,  1,  1)
    glVertex3f(-1,  1, -1)
    glNormal3f(1, 0, 0)
    glVertex3f(1, -1, -1)
    glVertex3f(1,  1, -1)
    glVertex3f(1,  1,  1)
    glVertex3f(1, -1,  1)
    glEnd()

def draw_pyramid():
    glBegin(GL_TRIANGLES)
    glNormal3f(0, 0.5, 1)
    glVertex3f(0, 1, 0)
    glVertex3f(-1, -1, 1)
    glVertex3f(1, -1, 1)
    glNormal3f(1, 0.5, 0)
    glVertex3f(0, 1, 0)
    glVertex3f(1, -1, 1)
    glVertex3f(1, -1, -1)
    glNormal3f(0, 0.5, -1)
    glVertex3f(0, 1, 0)
    glVertex3f(1, -1, -1)
    glVertex3f(-1, -1, -1)
    glNormal3f(-1, 0.5, 0)
    glVertex3f(0, 1, 0)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, -1, 1)
    glEnd()
    glBegin(GL_QUADS)
    glNormal3f(0, -1, 0)
    glVertex3f(-1, -1, 1)
    glVertex3f(1, -1, 1)
    glVertex3f(1, -1, -1)
    glVertex3f(-1, -1, -1)
    glEnd()

def draw_obj():
    glBegin(GL_TRIANGLES)
    for face in obj_model:
        for vertex in face:
            glVertex3fv(vertex)
    glEnd()

def load_obj():
    global obj_model
    obj_model.clear()
    vertices = []
    try:
        with open("model.obj") as f:
            for line in f:
                if line.startswith("v "):
                    parts = line.split()
                    vertices.append([float(p) for p in parts[1:4]])
                elif line.startswith("f "):
                    parts = line.split()[1:]
                    face = [vertices[int(p.split("/")[0]) - 1] for p in parts]
                    if len(face) >= 3:
                        obj_model.append(face[:3])
    except FileNotFoundError:
        print("File model.obj")

def save_obj(filename="output3d.obj"):
    with open(filename, "w") as f:
        if current_object == 0:  # Cube
            vertices = [
                [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
                [-1, -1,  1], [1, -1,  1], [1, 1,  1], [-1, 1,  1]
            ]
            faces = [
                [5, 6, 7, 8], [1, 2, 3, 4], [4, 3, 7, 8],
                [2, 1, 5, 6], [3, 2, 6, 7], [1, 4, 8, 5]
            ]
        elif current_object == 1:  # Pyramid
            vertices = [
                [0, 1, 0], [-1, -1, 1], [1, -1, 1], [1, -1, -1], [-1, -1, -1]
            ]
            faces = [[1, 2, 3], [1, 3, 4], [1, 4, 5], [1, 5, 2], [2, 3, 4, 5]]
        else:
            print("Tidak bisa menyimpan objek dari file .obj.")
            return
        for v in vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        for face in faces:
            f.write("f " + " ".join(str(i) for i in face) + "\n")
        print(f"Berhasil disimpan ke: {filename}")

def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glClearColor(0.1, 0.1, 0.1, 1.0)
    load_obj()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)
    if lighting_enabled:
        glEnable(GL_LIGHTING)
    else:
        glDisable(GL_LIGHTING)
    glTranslatef(pos_x, pos_y, pos_z)
    glScalef(scale, scale, scale)
    glRotatef(angle_x, 1, 0, 0)
    glRotatef(angle_y, 0, 1, 0)
    glColor3fv(current_color)
    if current_object == 0:
        draw_cube()
    elif current_object == 1:
        draw_pyramid()
    else:
        draw_obj()
    glutSwapBuffers()

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w/h, 1, 50.0)
    glMatrixMode(GL_MODELVIEW)

def keyboard(key, x, y):
    global pos_x, pos_y, pos_z, current_object, lighting_enabled, current_color, scale, angle_x, angle_y
    if key == b'a': pos_x -= 0.1
    elif key == b'd': pos_x += 0.1
    elif key == b'w': pos_y += 0.1
    elif key == b's': pos_y -= 0.1
    elif key == b'z': pos_z += 0.1
    elif key == b'x': pos_z -= 0.1
    elif key == b'm': current_object = (current_object + 1) % 3
    elif key == b'l': lighting_enabled = not lighting_enabled
    elif key == b'r': current_color = [1.0, 0.0, 0.0]
    elif key == b'g': current_color = [0.0, 1.0, 0.0]
    elif key == b'b': current_color = [0.0, 0.0, 1.0]
    elif key == b'+': scale *= 1.1
    elif key == b'-': scale = max(0.1, scale * 0.9)
    elif key == b'0':
        pos_x, pos_y, pos_z = 0, 0, -5
        angle_x, angle_y = 0, 0
        scale = 1.0
    elif key == b'o':
        save_obj()
    glutPostRedisplay()

def mouse_motion(x, y):
    global angle_x, angle_y, last_x, last_y, mouse_down
    if mouse_down:
        angle_y += (x - last_x)
        angle_x += (y - last_y)
        last_x = x
        last_y = y
        glutPostRedisplay()

def mouse(button, state, x, y):
    global mouse_down, last_x, last_y
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            mouse_down = True
            last_x = x
            last_y = y
        elif state == GLUT_UP:
            mouse_down = False

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Modul B - Objek 3D")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutMotionFunc(mouse_motion)
    glutMainLoop()

if __name__ == '__main__':
    main()
