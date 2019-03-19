# coding: utf-8

from vpython import compound, color, vector, box, radians, rate


box1 = box(pos=vector(1, 0, 0), length=1, width=2, height=3, color=color.red)
box2 = box(pos=vector(5, 0, 0), length=1, width=2, height=3, color=color.blue)

bb = compound([box1, box2])
print(bb)
print(box2)

while True:
    rate(30)
    bb.rotate(axis=vector(1, 0, 0), angle=radians(2))
