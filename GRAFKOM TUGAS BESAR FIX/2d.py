from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from math import cos, sin, radians

window_width = 800
window_height = 600
objects = []
current_color = (1.0, 1.0, 1.0)
line_width = 2
start_point = None
mode = 'line, point, rect, ellipse' 
clipping_window = []

def draw_point(x, y):
    glPointSize(5)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def draw_line(p1, p2):
    glLineWidth(line_width)
    glBegin(GL_LINES)
    glVertex2f(*p1)
    glVertex2f(*p2)
    glEnd()

def draw_rect(p1, p2):
    glLineWidth(line_width)
    glBegin(GL_LINE_LOOP)
    glVertex2f(p1[0], p1[1])
    glVertex2f(p2[0], p1[1])
    glVertex2f(p2[0], p2[1])
    glVertex2f(p1[0], p2[1])
    glEnd()

def draw_ellipse(p1, p2):
    glLineWidth(line_width)
    glBegin(GL_LINE_LOOP)
    cx = (p1[0] + p2[0]) / 2
    cy = (p1[1] + p2[1]) / 2
    rx = abs(p1[0] - p2[0]) / 2
    ry = abs(p1[1] - p2[1]) / 2
    for i in range(360):
        angle = radians(i)
        x = cx + rx * cos(angle)
        y = cy + ry * sin(angle)
        glVertex2f(x, y)
    glEnd()


def screen_to_gl(x, y):
    return (x / window_width * 2 - 1, -(y / window_height * 2 - 1))

INSIDE, LEFT, RIGHT, BOTTOM, TOP = 0, 1, 2, 4, 8


def draw_clipping_window():
    if len(clipping_window) == 2:
        glColor3f(1.0, 0.0, 0.0)
        draw_rect(clipping_window[0], clipping_window[1])


def compute_code(x, y, xmin, xmax, ymin, ymax):
    code = INSIDE
    if x < xmin: code |= LEFT
    elif x > xmax: code |= RIGHT
    if y < ymin: code |= BOTTOM
    elif y > ymax: code |= TOP
    return code

def cohen_sutherland_clip(x1, y1, x2, y2, xmin, xmax, ymin, ymax):
    code1 = compute_code(x1, y1, xmin, xmax, ymin, ymax)
    code2 = compute_code(x2, y2, xmin, xmax, ymin, ymax)
    while True:
        if not (code1 | code2):
            return (x1, y1, x2, y2)
        elif code1 & code2:
            return None
        else:
            code_out = code1 if code1 else code2
            if code_out & TOP:
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                y = ymax
            elif code_out & BOTTOM:
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                y = ymin
            elif code_out & RIGHT:
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                x = xmax
            elif code_out & LEFT:
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                x = xmin
            if code_out == code1:
                x1, y1 = x, y
                code1 = compute_code(x1, y1, xmin, xmax, ymin, ymax)
            else:
                x2, y2 = x, y
                code2 = compute_code(x2, y2, xmin, xmax, ymin, ymax)

def mouse_func(button, state, x, y):
    global start_point, clipping_window
    gl_x, gl_y = screen_to_gl(x, y)

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            start_point = (gl_x, gl_y)
        elif state == GLUT_UP and start_point:
            end_point = (gl_x, gl_y)
            transform = {"translate": (0,0), "rotate": 0, "scale": 1}
            objects.append((mode, start_point, end_point, current_color, transform))
            start_point = None
            glutPostRedisplay()

    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if len(clipping_window) >= 2:
            clipping_window.clear()
        clipping_window.append((gl_x, gl_y))
        if len(clipping_window) > 2:
            clipping_window = clipping_window[-2:]
        glutPostRedisplay()

def keyboard_func(key, x, y):
    global current_color, line_width, mode, clipping_window

    if key == b'r': current_color = (1.0, 0.0, 0.0)
    elif key == b'g': current_color = (0.0, 1.0, 0.0)
    elif key == b'b': current_color = (0.0, 0.0, 1.0)
    elif key == b'+': line_width += 1
    elif key == b'-': line_width = max(1, line_width - 1)
    elif key == b'1': mode = 'point'
    elif key == b'2': mode = 'line'
    elif key == b'3': mode = 'rect'
    elif key == b'4': mode = 'ellipse'
    elif key == b'c':  
        clipping_window.clear()
    elif key == b'\x08' or key == b'h': 
        if objects:
            objects.pop()
    elif objects:
        obj = objects[-1][4]
        if key == b'w': obj["translate"] = (obj["translate"][0], obj["translate"][1] + 0.1)
        elif key == b's': obj["translate"] = (obj["translate"][0], obj["translate"][1] - 0.1)
        elif key == b'a': obj["translate"] = (obj["translate"][0] - 0.1, obj["translate"][1])
        elif key == b'd': obj["translate"] = (obj["translate"][0] + 0.1, obj["translate"][1])
        elif key == b'z': obj["scale"] *= 1.1
        elif key == b'x': obj["scale"] = max(0.1, obj["scale"] * 0.9)
        elif key == b'q': obj["rotate"] -= 5
        elif key == b'e': obj["rotate"] += 5

    glutPostRedisplay()


def display():
    glClear(GL_COLOR_BUFFER_BIT)

    draw_clipping_window() 

    for obj in objects:
        shape, p1, p2, color, transform = obj
        glPushMatrix()
        glTranslatef(transform["translate"][0], transform["translate"][1], 0)
        glScalef(transform["scale"], transform["scale"], 1)
        glRotatef(transform["rotate"], 0, 0, 1)

        if shape == 'line' and len(clipping_window) == 2:
            xmin = min(clipping_window[0][0], clipping_window[1][0])
            xmax = max(clipping_window[0][0], clipping_window[1][0])
            ymin = min(clipping_window[0][1], clipping_window[1][1])
            ymax = max(clipping_window[0][1], clipping_window[1][1])

            clipped = cohen_sutherland_clip(p1[0], p1[1], p2[0], p2[1], xmin, xmax, ymin, ymax)
            if clipped:
                glColor3f(0.0, 1.0, 0.0)
                draw_line((clipped[0], clipped[1]), (clipped[2], clipped[3]))
        else:
            glColor3f(*color)
            if shape == 'point': draw_point(*p1)
            elif shape == 'line': draw_line(p1, p2)
            elif shape == 'rect': draw_rect(p1, p2)
            elif shape == 'ellipse': draw_ellipse(p1, p2)

        glPopMatrix()
    
    glFlush()

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)

glutInit(sys.argv)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(window_width, window_height)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Modul A: Objek 2D Lengkap")
init()
glutDisplayFunc(display)
glutMouseFunc(mouse_func)
glutKeyboardFunc(keyboard_func)
glutMainLoop()
