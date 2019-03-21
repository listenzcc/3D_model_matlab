# coding: utf-8

from vpython import arrow, box, bumpmaps, color, distant_light, radians, rate, scene, sphere, textures, vector
from toolbox_draw_body import draw_part, p0, p1, p1_, p2, p2_

up = vector(0, 1, 0)
right = vector(-1, 0, 0)
front = vector(0, 0, 1)

p2 -= right*0.3
p2_ -= right*0.3
p2 -= up*0.2
p2_ -= up*0.2


def draw_anchor(p, a0=up, a1=right, a2=front, full=False):
    # draw anchor and regular axis
    if full:
        arrow(pos=p, radius=0.5, axis=a0.norm()*4, color=color.red)
        arrow(pos=p, radius=0.5, axis=a1.norm()*4, color=color.green)
        arrow(pos=p, radius=0.5, axis=a2.norm()*4, color=color.blue)
    return sphere(pos=p, radius=0.5, color=color.white)


def draw_arm_anchor(p, a0, a1, radius=0.5, color_=color.white):
    # draw anchor
    # a0: main_axis
    # a1: sub_axis
    a = [0, 0, 0]
    a[0] = arrow(pos=p, radius=0.5, axis=a0.norm()*4, color=color.red)
    a[1] = arrow(pos=p, radius=0.5, axis=a1.norm()*4, color=color.green)
    a[2] = arrow(pos=p, radius=0.5, axis=a0.cross(a1).norm()*4,
                 color=color.blue)
    s = sphere(pos=p, radius=radius, color=color_)
    return s, a


# crown
draw_anchor(up*15, full=True)

# chair :-)
abox = box(pos=vector(0.02575, -5.062, 1.366)+up-front*2,
           axis=right, length=10, width=10, height=6)
abox.texture = {'file': textures.stones, 'bumpmaps': bumpmaps.stones}
abox.shininess = 0

# body init
body = draw_part('body')

# upper_arm init
upper_arm = draw_part('upper_arm', color.red)
upper_arm_main_axis = (p1-p2).norm()
upper_arm_sub_axis = upper_arm_main_axis.cross(front).cross(
    upper_arm_main_axis).norm()
# shoulder anchor
shoulder_anchor_pos = p2
shoulder_anchor, shoulder_axis = draw_arm_anchor(
    shoulder_anchor_pos, upper_arm_main_axis, upper_arm_sub_axis,
    radius=(p2-p2_).mag*1.2, color_=vector(1, 0.7, 0.2))

# small_arm init
small_arm = draw_part('small_arm', color.green)
small_arm_main_axis = (p0-p1).norm()
small_arm_sub_axis = small_arm_main_axis.cross(front).cross(
    small_arm_main_axis).norm()
# joint anchor
joint_anchor_pos = p1
joint_anchor, joint_axis = draw_arm_anchor(
    joint_anchor_pos, small_arm_main_axis, small_arm_sub_axis)

# hand anchor
hand_anchor_pos = p0
hand_anchor = draw_anchor(hand_anchor_pos)

distant_light(direction=up*10, color=color.gray(0.8))

input('Press ENTER to continue')


def motion_backing():
    m1 = motion_backing_upper_arm()
    m2 = motion_backing_small_arm()
    return any([m1, m2])


def motion_backing_upper_arm(angle=radians(2)):
    # return False, if we are fine
    if all([abs(shoulder_axis[0].axis.diff_angle(upper_arm_main_axis)) < angle,
            abs(shoulder_axis[1].axis.diff_angle(upper_arm_sub_axis)) < angle]):
        return False

    origin = shoulder_anchor.pos

    # back main_axis
    if abs(shoulder_axis[0].axis.diff_angle(upper_arm_main_axis)) > angle:
        axis = shoulder_axis[0].axis.cross(upper_arm_main_axis)
        [e.rotate(origin=origin, axis=axis, angle=angle)
         for e in [upper_arm, joint_anchor, small_arm, hand_anchor] +
         joint_axis + shoulder_axis]
        return True

    # back sub_axis
    if abs(shoulder_axis[1].axis.diff_angle(upper_arm_sub_axis)) > angle:
        axis = shoulder_axis[1].axis.cross(upper_arm_sub_axis)
        [e.rotate(origin=origin, axis=axis, angle=angle)
         for e in [upper_arm, joint_anchor, small_arm, hand_anchor] +
         joint_axis + shoulder_axis]
        return True


def motion_backing_small_arm(angle=radians(2)):
    # return False, if we are fine
    if all([abs(joint_axis[0].axis.diff_angle(small_arm_main_axis)) < angle,
            abs(joint_axis[1].axis.diff_angle(small_arm_sub_axis)) < angle]):
        return False

    origin = joint_anchor.pos

    # back main_axis
    if abs(joint_axis[0].axis.diff_angle(small_arm_main_axis)) > angle:
        axis = joint_axis[0].axis.cross(small_arm_main_axis)
        [e.rotate(origin=origin, axis=axis, angle=angle)
         for e in [small_arm, hand_anchor] + joint_axis]
        return True

    # back sub_axis
    if abs(joint_axis[1].axis.diff_angle(small_arm_sub_axis)) > angle:
        axis = joint_axis[1].axis.cross(small_arm_sub_axis)
        [e.rotate(origin=origin, axis=axis, angle=angle)
         for e in [small_arm, hand_anchor] + joint_axis]
        return True


def motion_waizhan(angle=radians(2)):
    print('Waizhan ...')
    for _ in range(40):
        rate(30)
        axis = - joint_axis[1].axis
        origin = shoulder_anchor.pos
        [e.rotate(origin=origin, angle=angle, axis=axis)
         for e in [upper_arm, joint_anchor, small_arm, hand_anchor] +
         shoulder_axis + joint_axis]
    print('Done.')


def motion_quzhou(angle=radians(2)):
    print('Quzhou ...')
    for _ in range(50):
        rate(30)
        axis = joint_axis[0].axis.cross(joint_axis[1].axis)
        origin = joint_anchor.pos
        [e.rotate(origin=origin, angle=angle, axis=axis)
         for e in [small_arm, hand_anchor] + joint_axis]
    print('Done.')


def motion_taishou(angle=radians(2)):
    print('Taishouing ...')
    for _ in range(40):
        rate(30)
        axis = shoulder_axis[0].axis.cross(shoulder_axis[1].axis)
        origin = shoulder_anchor.pos
        [e.rotate(origin=origin, angle=angle, axis=axis)
         for e in [upper_arm, joint_anchor, small_arm, hand_anchor] +
         shoulder_axis + joint_axis]
    print('Done.')


def motion_back():
    print('Backing ...')
    while True:
        rate(30)
        if not motion_backing():
            break
    print('Done.')


while True:
    print('Press q for quzhou, t for taishou, w for waizha, b for back')
    ev = scene.waitfor('click keydown')
    if ev.event == 'click':
        print('Clicked at', ev.pos)
    else:
        print('Pressed key', ev.key)
        if ev.key == 't':
            motion_taishou()
        if ev.key == 'q':
            motion_quzhou()
        if ev.key == 'w':
            motion_waizhan()
        if ev.key == 'b':
            motion_back()
