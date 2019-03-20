# coding: utf-8

from vpython import arrow, box, bumpmaps, color, distant_light, radians, rate, sphere, textures, vector
from toolbox_draw_body import draw_part

p0 = vector(-13.75, -2.991, 1.813)  # finger end
p1 = vector(-7.382, 2.788, -0.2068)  # joint
p2 = vector(-4.78, 6.444, -0.9699)  # shoulder

up = vector(0, 1, 0)
right = vector(-1, 0, 0)
front = vector(0, 0, 1)


def draw_anchor(p, a0=up, a1=right, a2=front, full=False):
    if full:
        arrow(pos=p, radius=0.5, axis=a0.norm()*4, color=color.red)
        arrow(pos=p, radius=0.5, axis=a1.norm()*4, color=color.green)
        arrow(pos=p, radius=0.5, axis=a2.norm()*4, color=color.blue)
    return sphere(pos=p, radius=0.5, color=color.white)


def draw_arm_anchor(p, a0, a1):
    a = [0, 0, 0]
    a[0] = arrow(pos=p, radius=0.5, axis=a0.norm()*4, color=color.red)
    a[1] = arrow(pos=p, radius=0.5, axis=a1.norm()*4, color=color.green)
    a[2] = arrow(pos=p, radius=0.5, axis=a0.cross(a1).norm()*4,
                 color=color.blue)
    s = sphere(pos=p, radius=0.5, color=color.white)
    return s, a


draw_anchor(up*15, full=True)

abox = box(pos=vector(0.02575, -5.062, 1.366)+up-front*2,
           axis=right, length=10, width=10, height=6)
abox.texture = {'file': textures.stones, 'bumpmaps': bumpmaps.stones}
abox.shininess = 0

body = draw_part('body')

upper_arm = draw_part('upper_arm', color.red)
upper_arm_main_axis = (p1-p2).norm()
upper_arm_sub_axis = upper_arm_main_axis.cross(front).cross(
    upper_arm_main_axis).norm()
shoulder_anchor_pos = p2
shoulder_anchor, shoulder_axis = draw_arm_anchor(
    shoulder_anchor_pos, upper_arm_main_axis, upper_arm_sub_axis)

small_arm = draw_part('small_arm', color.green)
small_arm_main_axis = (p0-p1).norm()
small_arm_sub_axis = small_arm_main_axis.cross(front).cross(
    small_arm_main_axis).norm()
joint_anchor_pos = p1
joint_anchor, joint_axis = draw_arm_anchor(
    joint_anchor_pos, small_arm_main_axis, small_arm_sub_axis)

hand_anchor_pos = p0
hand_anchor = draw_anchor(hand_anchor_pos)

distant_light(direction=up*10, color=color.gray(0.8))

input('Press ENTER to continue')


def motion_quzhou():
    for _ in range(50):
        rate(30)
        axis = joint_axis[0].axis.cross(joint_axis[1].axis).norm()
        origin = joint_anchor_pos
        angle = radians(2)

        small_arm.rotate(origin=origin, angle=angle, axis=axis)
        hand_anchor.rotate(origin=origin, angle=angle, axis=axis)
        [a.rotate(origin=origin, angle=angle, axis=axis) for a in joint_axis]


def motion_taishou():
    for _ in range(40):
        rate(30)
        axis = shoulder_axis[0].axis.cross(shoulder_axis[1].axis).norm()
        origin = shoulder_anchor_pos
        angle = radians(2)

        upper_arm.rotate(origin=origin, angle=angle, axis=axis)
        joint_anchor.rotate(origin=origin, angle=angle, axis=axis)
        [a.rotate(origin=origin, angle=angle, axis=axis)
         for a in shoulder_axis]

        small_arm.rotate(origin=origin, angle=angle, axis=axis)
        hand_anchor.rotate(origin=origin, angle=angle, axis=axis)
        [a.rotate(origin=origin, angle=angle, axis=axis) for a in joint_axis]


motion_taishou()
