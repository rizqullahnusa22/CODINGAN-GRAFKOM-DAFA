from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 400, 0, 500)

# Huruf D
def draw_letter_D(x_offset):
    glColor3f(1.0, 1.0, 1.0)  

    # BAGIAN LUAR
    glBegin(GL_POLYGON)
    glVertex2f(x_offset + 0, 100)
    glVertex2f(x_offset + 15, 100)
    for angle in range(-90, 91, 5):
        rad = math.radians(angle)
        x = x_offset + 15 + 30 * math.cos(rad)
        y = 150 + 50 * math.sin(rad)
        glVertex2f(x, y)
    glVertex2f(x_offset + 15, 200)
    glVertex2f(x_offset + 0, 200)
    glEnd()


    glColor3f(0.0, 0.0, 0.0)  
    glBegin(GL_POLYGON)
    glVertex2f(x_offset + 7, 110)
    glVertex2f(x_offset + 15, 110)
    for angle in range(-90, 91, 5):
        rad = math.radians(angle)
        x = x_offset + 15 + 22 * math.cos(rad)
        y = 150 + 40 * math.sin(rad)
        glVertex2f(x, y)
    glVertex2f(x_offset + 15, 190)
    glVertex2f(x_offset + 7, 190)
    glEnd()

# Huruf A
def draw_letter_A(x_offset):
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glVertex2f(x_offset + 10, 100)
    glVertex2f(x_offset + 20, 100)
    glVertex2f(x_offset + 35, 200)
    glVertex2f(x_offset + 25, 200)
    glEnd()

    glBegin(GL_QUADS)
    glVertex2f(x_offset + 35, 200)
    glVertex2f(x_offset + 45, 200)
    glVertex2f(x_offset + 60, 100)
    glVertex2f(x_offset + 50, 100)
    glEnd()

    glBegin(GL_QUADS)
    glVertex2f(x_offset + 25, 145)
    glVertex2f(x_offset + 45, 145)
    glVertex2f(x_offset + 45, 155)
    glVertex2f(x_offset + 25, 155)
    glEnd()

# Huruf F
def draw_letter_F(x_offset):
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glVertex2f(x_offset + 0, 100)
    glVertex2f(x_offset + 15, 100)
    glVertex2f(x_offset + 15, 200)
    glVertex2f(x_offset + 0, 200)
    glEnd()

    glBegin(GL_QUADS)
    glVertex2f(x_offset + 15, 185)
    glVertex2f(x_offset + 45, 185)
    glVertex2f(x_offset + 45, 200)
    glVertex2f(x_offset + 15, 200)
    glEnd()

    glBegin(GL_QUADS)
    glVertex2f(x_offset + 15, 140)
    glVertex2f(x_offset + 40, 140)
    glVertex2f(x_offset + 40, 155)
    glVertex2f(x_offset + 15, 155)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)  # Warna huruf

    draw_letter_D(10)    # D di posisi awal
    draw_letter_A(80)    # A setelah D
    draw_letter_F(150)   # F setelah A
    draw_letter_A(220)   # A lagi

    glFlush()

# Setup window
glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(400, 300)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"OpenGL - DAFA")
init()
glutDisplayFunc(display)
glutMainLoop()
