# coding: utf-8

from vpython import arrow, box, color, compound, radians, rate, vector

O = vector(0, 0, 0)
up = vector(1, 0, 0)
right = vector(0, 1, 0)
front = vector(0, 0, 1)

arrow(pos=O, axis=up, color=color.red)
arrow(pos=O, axis=right, color=color.green)
arrow(pos=O, axis=front, color=color.blue)

box1 = box(pos=O+vector(0, 10, 0), width=1, height=2,
           length=3, color=color.cyan, opacity=0.5)
box2 = box(pos=O+vector(0, -10, 0), width=1, height=2,
           length=3, color=color.cyan, opacity=0.5)

cb = compound([box1, box2])

while True:
    rate(30)
    cb.rotate(axis=up, angle=radians(2))
