# coding: utf-8

import os
from vpython import arrow, color, compound, quad, radians, rate, sphere, vector, vertex

O = vector(0, 0, 0)
up = vector(1, 0, 0)
right = vector(0, 1, 0)
front = vector(0, 0, 1)

arrow(pos=O, axis=up, color=color.red)
arrow(pos=O, axis=right, color=color.green)
arrow(pos=O, axis=front, color=color.blue)


points = [0]
with open(os.path.join('..', 'parts', 'small_arm_v.txt'), 'rb') as pFile:
    line = pFile.readline()
    while line:
        p = [float(e) for e in line.split()]
        points.append(vector(p[0], p[1], p[2]))
        line = pFile.readline()

faces = []
with open(os.path.join('..', 'parts', 'small_arm_f.txt'), 'rb') as pFile:
    line = pFile.readline()
    while line:
        f = [int(float(e)) for e in line.split() if b'NaN' not in e]
        faces.append(f)
        line = pFile.readline()

input('press Enter to continue.')

arm = compound([quad(vs=[vertex(pos=points[e], color=color.cyan) for e in f])
                for f in faces if len(f) == 4])
while True:
    rate(30)
    arm.rotate(axis=vector(0, 0, 1), angle=radians(2), origin=O)
