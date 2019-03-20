# coding: utf-8

import os
import numpy as np
from vpython import arrow, bumpmaps, box, color, compound, distant_light, quad, radians, rate, sphere, textures, triangle, vector, vertex

p0 = vector(-13.75, -2.991, 1.813)
p1 = vector(-7.382, 2.788, -0.2068)
p2 = vector(-4.78, 6.444, -0.9699)

up = vector(0, 1, 0)
right = vector(-1, 0, 0)
front = vector(0, 0, 1)


def draw_anchor(p, a0=up, a1=right, a2=front):
    sphere(pos=p, radius=0.5, color=color.white)
    arrow(pos=p, radius=0.5, axis=a0.norm()*4, color=color.red)
    arrow(pos=p, radius=0.5, axis=a1.norm()*4, color=color.green)
    arrow(pos=p, radius=0.5, axis=a2.norm()*4, color=color.blue)


draw_anchor(p0)
draw_anchor(p1)
draw_anchor(p2)

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


def is_in(p, start, stop):
    if (p-start).dot(stop-start) < 0:
        return False
    if (p-stop).dot(start-stop) < 0:
        return False

    a = p - start
    b = p - stop
    c = start - stop
    if abs(a.cross(b).mag / c.mag) > 2.2:
        return False

    return True


body_faces = dict()
body_faces['body'] = []
body_faces['small_arm'] = []
body_faces['upper_arm'] = []
with open(os.path.join('..', 'parts', 'body_f.txt'), 'rb') as pFile:
    string = pFile.readline()
    while string:
        f = [int(float(e)) for e in string.split() if b'NaN' not in e]
        if not len(f) == 4:
            string = pFile.readline()
            continue

        body_faces_idx = 'body'

        for j in f:
            if is_in(points[j], p0, p1):
                body_faces_idx = 'small_arm'
                break
            if is_in(points[j], p1, p2):
                body_faces_idx = 'upper_arm'
                break

        body_faces[body_faces_idx].append(f)
        string = pFile.readline()


def draw_part(idx, color=vector(1, 0.7, 0.2)):  # color.gray(0.5)):
    print('Compounding %s ...' % idx)
    part = compound([quad(vs=[vertex(
        pos=points[j], normal=points_n[j], color=color)
        for j in f]) for f in body_faces[idx]])
    print('Done.')
    return part


abox = box(pos=vector(0.02575, -5.062, 1.366)+up-front*2,
           axis=right, length=10, width=10, height=6)
abox.texture = {'file': textures.stones, 'bumpmaps': bumpmaps.stones}
abox.shininess = 0
body = draw_part('body')
small_arm = draw_part('small_arm', color.green)
upper_arm = draw_part('upper_arm', color.red)


distant_light(direction=up*10, color=color.gray(0.8))
