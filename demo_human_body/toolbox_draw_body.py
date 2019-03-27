# coding: utf-8

import os
from vpython import arrow, bumpmaps, box, color, compound, distant_light, quad, radians, rate, sphere, textures, triangle, vector, vertex

p0 = vector(-13.75, -2.991, 1.813)  # finger end
p1 = (vector(-7.382, 2.788, -0.2068) + vector(-6.331, 1.749, -1.528) +
      vector(-5.594, 2, -0.4682)) / 3  # joint
p1_ = vector(-7.382, 2.788, -0.2068)
p2 = (vector(-4.735, 6.364, -1.425) + vector(-3.647, 4.584, -0.3449) +
      vector(-4.222, 6.02, -2.201)) / 3  # shoulder
p2_ = vector(-4.735, 6.364, -1.425)

p0_la = vector(13.75, -2.991, 1.813)  # finger end
p1_la = (vector(7.382, 2.788, -0.2068) + vector(6.331, 1.749, -1.528) +
         vector(5.594, 2, -0.4682)) / 3  # joint
p1__la = vector(7.382, 2.788, -0.2068)
p2_la = (vector(4.735, 6.364, -1.425) + vector(3.647, 4.584, -0.3449) +
         vector(4.222, 6.02, -2.201)) / 3  # shoulder
p2__la = vector(4.735, 6.364, -1.425)

pp_right_leg = vector(-4.14, -21.09, 4.1)
p0_right_leg = vector(-4.154, -21.26, -1.964)
p1_right_leg = vector(-3.87, -10.76, -0.1997)
p2_right_leg = vector(-3.563, -3.918, -0.2727)

pp_left_leg = vector(4.14, -21.09, 4.1)
p0_left_leg = vector(4.154, -21.26, -1.964)
p1_left_leg = vector(3.87, -10.76, -0.1997)
p2_left_leg = vector(3.563, -3.918, -0.2727)

points = [0]
with open(os.path.join('..', 'parts', 'body_v.txt'), 'rb') as pFile:
    string = pFile.readline()
    while string:
        p = [float(e) for e in string.split()]
        points.append(vector(p[0], p[1], p[2]))
        string = pFile.readline()

points_n = [0]
with open(os.path.join('..', 'parts', 'body_vn.txt'), 'rb') as pFile:
    string = pFile.readline()
    while string:
        p = [float(e) for e in string.split()]
        points_n.append(vector(p[0], p[1], p[2]))
        string = pFile.readline()


def is_in(p, start, stop, d=1.8):
    if (p-start).dot(stop-start) < 0:
        return False
    if (p-stop).dot(start-stop) < 0:
        return False

    a = p - start
    b = p - stop
    c = start - stop
    if abs(a.cross(b).mag / c.mag) > d:
        return False

    return True


body_faces = dict()
body_faces['body'] = []
body_faces['small_arm'] = []
body_faces['upper_arm'] = []
body_faces['small_left_arm'] = []
body_faces['upper_left_arm'] = []
body_faces['small_right_leg'] = []
body_faces['upper_right_leg'] = []
body_faces['small_left_leg'] = []
body_faces['upper_left_leg'] = []

with open(os.path.join('..', 'parts', 'body_f.txt'), 'rb') as pFile:
    string = pFile.readline()
    while string:
        f = [int(float(e)) for e in string.split() if b'NaN' not in e]
        if not len(f) == 4:
            string = pFile.readline()
            continue

        body_faces_idx = 'body'
        if any(is_in(points[j], p0, p1) for j in f):
            body_faces_idx = 'small_arm'

        if all(is_in(points[j], p1, p2, d=1.6) for j in f):
            body_faces_idx = 'upper_arm'

        if any(is_in(points[j], p0_la, p1_la) for j in f):
            body_faces_idx = 'small_left_arm'

        if all(is_in(points[j], p1_la, p2_la, d=1.6) for j in f):
            body_faces_idx = 'upper_left_arm'

        if any(is_in(points[j], pp_right_leg, p0_right_leg, d=3) for j in f):
            body_faces_idx = 'small_right_leg'
        if any(is_in(points[j], p0_right_leg, p1_right_leg, d=3.2) for j in f):
            body_faces_idx = 'small_right_leg'
        if any(is_in(points[j], p1_right_leg, p2_right_leg, d=3.1) for j in f):
            body_faces_idx = 'upper_right_leg'

        if any(is_in(points[j], pp_left_leg, p0_left_leg, d=3) for j in f):
            body_faces_idx = 'small_left_leg'
        if any(is_in(points[j], p0_left_leg, p1_left_leg, d=3.2) for j in f):
            body_faces_idx = 'small_left_leg'
        if any(is_in(points[j], p1_left_leg, p2_left_leg, d=3.1) for j in f):
            body_faces_idx = 'upper_left_leg'

        body_faces[body_faces_idx].append(f)
        string = pFile.readline()


def draw_part(idx, color_=vector(1, 0.7, 0.2)):  # color.gray(0.5)):
    print('Compounding %s ...' % idx)
    part = compound([quad(vs=[vertex(
        pos=points[j], normal=points_n[j], color=color_)
        for j in f]) for f in body_faces[idx]])
    print('Done.')
    return part
