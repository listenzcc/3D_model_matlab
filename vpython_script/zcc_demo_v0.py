# code: utf-8

from vpython import scene, vector, arrow, cylinder, sphere, color, rate, radians
import numpy as np

rnd = np.random.rand()

scene.title = 'Coordinates'
scene.width = 600
scene.height = 400
#scene.forward = vector(-1,-1,-1)
#scene.range = 10

X = arrow(pos=vector(-10, -10, -10), axis=vector(5, 0, 0),
          color=color.red, shaftwidth=0.5)
Y = arrow(pos=vector(-10, -10, -10), axis=vector(0, 5, 0),
          color=color.green, shaftwidth=0.5)
Z = arrow(pos=vector(-10, -10, -10), axis=vector(0, 0, 5),
          color=color.blue, shaftwidth=0.5)

'''
ev = scene.waitfor('click keydown')
if ev.event == 'click':
    print('You clicked at', ev.pos)
else:
    print('You pressed key '+ev.key)
'''

S0 = sphere(pos=vector(0, 0, 0), radius=2, color=color.cyan)
C0 = cylinder(pos=S0.pos, axis=vector(10, 0, 0), radius=1, color=color.cyan)
S1 = sphere(pos=C0.pos+C0.axis, radius=2, color=color.cyan)
C1 = cylinder(pos=S1.pos, axis=vector(10, 0, 0), radius=1, color=color.cyan)
S2 = sphere(pos=C1.pos+C1.axis, radius=2, color=color.cyan)


def be_ready(S0=S0, C0=C0, C1=C1):
    ready = True
    zp = vector(0, 0, 0)
    if not S0.pos == zp:
        diff = S0.pos - zp
        if diff.dot(diff) < 0.1:
            rate(100)
            S0.pos = zp
        else:
            ready = False
            rate(100)
            S0.pos -= diff.norm() / 2

    C0.axis = vector(0, -1, 0).norm() * 10
    C1.axis = vector(0, -1, 0).norm() * 10
    update_pos()
    return ready


def update_pos(S0=S0, C0=C0, S1=S1, C1=C1, S2=S2):
    rate(100)
    C0.pos = S0.pos
    S1.pos = C0.pos + C0.axis
    C1.pos = S1.pos
    S2.pos = C1.pos + C1.axis


def rotation_C0(ta, C0=C0):
    if C0.axis == ta:
        return True
    cv = C0.axis.norm().cross(ta.norm())
    if cv.dot(cv) < 0.1:
        rate(100)
        C0.axis = ta.norm() * 10
        return False
    rate(100)
    C0.rotate(angle=radians(1), axis=cv)
    return False


be_ready()
update_pos()

ta = vector(1, 0, 0)
while not rotation_C0(ta):
    update_pos()

'''
for j in range(100):
    rate(2)
    C0.rotate(angle=radians(10), axis=vector(0, 0, 1))
    update_pos()
'''
