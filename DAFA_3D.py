import math

def extrude_polygon(polygon_2d, depth=5):
    vertices = []
    faces = []
    n = len(polygon_2d)
    for x, y in polygon_2d:
        vertices.append((x, y, 0))
    for x, y in polygon_2d:
        vertices.append((x, y, -depth))
    for i in range(n - 1):
        faces.append((i, i + 1, i + 1 + n, i + n))
    faces.append(tuple(range(n)))
    faces.append(tuple(range(n, 2 * n)))
    return vertices, faces

def create_letter_D(offset_x=0, offset_y=0, depth=5):
    outer = [(offset_x + 0, offset_y + 100), (offset_x + 15, offset_y + 100)]
    for angle in range(-90, 91, 5):
        rad = math.radians(angle)
        x = offset_x + 15 + 30 * math.cos(rad)
        y = offset_y + 150 + 50 * math.sin(rad)
        outer.append((x, y))
    outer += [(offset_x + 15, offset_y + 200), (offset_x + 0, offset_y + 200)]
    return extrude_polygon(outer, depth)

def create_letter_A(offset_x=0, offset_y=0, depth=5):
    left = [(offset_x + 10, offset_y + 100), (offset_x + 20, offset_y + 100),
            (offset_x + 35, offset_y + 200), (offset_x + 25, offset_y + 200), (offset_x + 10, offset_y + 100)]
    right = [(offset_x + 35, offset_y + 200), (offset_x + 45, offset_y + 200),
             (offset_x + 60, offset_y + 100), (offset_x + 50, offset_y + 100), (offset_x + 35, offset_y + 200)]
    cross = [(offset_x + 25, offset_y + 145), (offset_x + 45, offset_y + 145),
             (offset_x + 45, offset_y + 155), (offset_x + 25, offset_y + 155), (offset_x + 25, offset_y + 145)]
    return combine_shapes([extrude_polygon(left, depth), extrude_polygon(right, depth), extrude_polygon(cross, depth)])

def create_letter_F(offset_x=0, offset_y=0, depth=5):
    vertical = [(offset_x + 0, offset_y + 100), (offset_x + 15, offset_y + 100),
                (offset_x + 15, offset_y + 200), (offset_x + 0, offset_y + 200), (offset_x + 0, offset_y + 100)]
    top = [(offset_x + 15, offset_y + 185), (offset_x + 45, offset_y + 185),
           (offset_x + 45, offset_y + 200), (offset_x + 15, offset_y + 200), (offset_x + 15, offset_y + 185)]
    mid = [(offset_x + 15, offset_y + 140), (offset_x + 40, offset_y + 140),
           (offset_x + 40, offset_y + 155), (offset_x + 15, offset_y + 155), (offset_x + 15, offset_y + 140)]
    return combine_shapes([extrude_polygon(vertical, depth), extrude_polygon(top, depth), extrude_polygon(mid, depth)])

def combine_shapes(shapes):
    vertices, faces = [], []
    offset = 0
    for vtx, fcs in shapes:
        vertices.extend(vtx)
   
        faces.extend([tuple(i + offset for i in f) for f in fcs])
        offset += len(vtx)
    return vertices, faces

def save_to_obj(filename, objects):
    lines = []
    offset = 1
    for vertices, faces in objects:
        for v in vertices:
            lines.append(f"v {v[0]} {v[1]} {v[2]}")
        for f in faces:
            lines.append("f " + " ".join(str(i + offset) for i in f))
        offset += len(vertices)
    with open(filename, 'w') as f:
        f.write("\n".join(lines))
    print(f"File berhasil disimpan sebagai: {filename}")

d = create_letter_D(0)
a1 = create_letter_A(100)
f = create_letter_F(220)
a2 = create_letter_A(340)
save_to_obj("DAFA_3D.obj", [d, a1, f, a2])