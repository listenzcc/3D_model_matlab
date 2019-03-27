# coding: utf-8

from vpython import arrow, box, bumpmaps, color, distant_light, radians, rate, scene, sphere, textures, vector
import time
from toolbox_draw_body import draw_part
from toolbox_draw_body import p0, p1, p1_, p2, p2_
from toolbox_draw_body import p0_la, p1_la, p1__la, p2_la, p2__la
from toolbox_draw_body import pp_right_leg, p0_right_leg, p1_right_leg, p2_right_leg
from toolbox_draw_body import pp_left_leg, p0_left_leg, p1_left_leg, p2_left_leg


up = vector(0, 1, 0)
right = vector(-1, 0, 0)
front = vector(0, 0, 1)

p2 -= up*0.2
p2_la -= up*0.2
# p2 -= right*0.3
# p2_ -= right*0.3
# p2 -= up*0.2
# p2_ -= up*0.2

visible = False


def draw_anchor(p, a0=up, a1=right, a2=front, full=False, visible=visible):
    # draw anchor and regular axis
    if full:
        arrow(pos=p, radius=0.5, axis=a0.norm()*4,
              color=color.red, visible=visible)
        arrow(pos=p, radius=0.5, axis=a1.norm()*4,
              color=color.green, visible=visible)
        arrow(pos=p, radius=0.5, axis=a2.norm()*4,
              color=color.blue, visible=visible)
    return sphere(pos=p, radius=0.5, color=color.white, visible=visible)


def draw_arm_anchor(p, a0, a1, radius=0.5, color_=color.white, visible=visible):
    # draw anchor
    # a0: main_axis
    # a1: sub_axis
    a = [0, 0, 0]
    a[0] = arrow(pos=p, radius=0.5, axis=a0.norm()*4,
                 color=color.red, visible=visible)
    a[1] = arrow(pos=p, radius=0.5, axis=a1.norm()*4,
                 color=color.green, visible=visible)
    a[2] = arrow(pos=p, radius=0.5, axis=a0.cross(a1).norm()*4,
                 color=color.blue, visible=visible)
    if not color_ == color.white:
        visible = True
    s = sphere(pos=p, radius=radius, color=color_, visible=visible)
    return s, a


# crown
draw_anchor(up*15, full=True)

# chair :-)
# abox = box(pos=vector(0.02575, -5.062-6, 1.366)+up-front*2,
#           axis=right, length=10, width=10, height=10)
# abox.texture = {'file': textures.stones, 'bumpmaps': bumpmaps.stones}
# abox.shininess = 0
bbox = box(pos=vector(0, -9.5, 0),
           axis=right, length=9, width=7, height=10)
bbox.texture = {'file': textures.rug}
bbox.shininess = 0

# body init
body = draw_part('body')
skincolor = vector(1, 0.7, 0.2)


# right_leg init
draw_part('upper_right_leg', skincolor)
upper_right_leg = draw_part('upper_right_leg', skincolor)
small_right_leg = draw_part('small_right_leg', skincolor)
# right_leg sit motion
main_axis = (p0_right_leg-p1_right_leg).norm()
sub_axis = main_axis.cross(front).cross(main_axis).norm()
small_right_leg.rotate(origin=p1_right_leg,
                       axis=sub_axis.cross(main_axis), angle=radians(90))
s = sphere(pos=p1_right_leg+vector(1, 0, 0), radius=1, color=skincolor)
main_axis = (p1_right_leg-p2_right_leg).norm()
sub_axis = main_axis.cross(front).cross(main_axis).norm()
[e.rotate(origin=p2_right_leg, axis=main_axis.cross(sub_axis), angle=radians(90))
 for e in [upper_right_leg, small_right_leg, s]]

# left_leg init
draw_part('upper_left_leg', skincolor)
upper_left_leg = draw_part('upper_left_leg', skincolor)
small_left_leg = draw_part('small_left_leg', skincolor)
# left_leg sit motion
main_axis = (p0_left_leg-p1_left_leg).norm()
sub_axis = main_axis.cross(front).cross(main_axis).norm()
small_left_leg.rotate(origin=p1_left_leg,
                      axis=sub_axis.cross(main_axis), angle=radians(90))
s = sphere(pos=p1_left_leg+vector(-1, 0, 0), radius=1, color=skincolor)
main_axis = (p1_left_leg-p2_left_leg).norm()
sub_axis = main_axis.cross(front).cross(main_axis).norm()
[e.rotate(origin=p2_left_leg, axis=main_axis.cross(sub_axis), angle=radians(90))
 for e in [upper_left_leg, small_left_leg, s]]


# upper_left_arm init
upper_left_arm = draw_part('upper_left_arm', skincolor)
upper_left_arm_main_axis = (p1_la-p2_la).norm()
upper_left_arm_sub_axis = upper_left_arm_main_axis.cross(front).cross(
    upper_left_arm_main_axis).norm()
# left_shoulder anchor
left_shoulder_anchor_pos = p2_la
left_shoulder_anchor, left_shoulder_axis = draw_arm_anchor(
    left_shoulder_anchor_pos, upper_left_arm_main_axis, upper_left_arm_sub_axis,
    radius=(p2_la-p2__la).mag, color_=skincolor)

# small_left_arm init
small_left_arm = draw_part('small_left_arm', skincolor)
small_left_arm_main_axis = (p0_la-p1_la).norm()
small_left_arm_sub_axis = small_left_arm_main_axis.cross(front).cross(
    small_left_arm_main_axis).norm()
# left_joint anchor
left_joint_anchor_pos = p1_la
left_joint_anchor, left_joint_axis = draw_arm_anchor(
    left_joint_anchor_pos, small_left_arm_main_axis, small_left_arm_sub_axis,
    radius=0.8, color_=skincolor)

# left_hand anchor
left_hand_anchor_pos = p0_la
left_hand_anchor = draw_anchor(left_hand_anchor_pos)

# regular left_arm
[e.rotate(origin=p2_la, axis=upper_left_arm_sub_axis, angle=radians(-20))
 for e in [upper_left_arm, left_joint_anchor, small_left_arm, left_hand_anchor] +
 left_shoulder_axis + left_joint_axis]
# modify init left axis
upper_left_arm_main_axis = (
    left_joint_anchor.pos-left_shoulder_anchor.pos).norm()
upper_left_arm_sub_axis = upper_left_arm_main_axis.cross(front).cross(
    upper_left_arm_main_axis).norm()
small_left_arm_main_axis = (left_hand_anchor.pos-left_joint_anchor.pos).norm()
small_left_arm_sub_axis = small_left_arm_main_axis.cross(front).cross(
    small_left_arm_main_axis).norm()
[e.rotate(origin=left_joint_anchor.pos, axis=small_left_arm_main_axis,
          angle=radians(80)) for e in [small_left_arm]]
[e.rotate(origin=left_joint_anchor.pos, axis=small_left_arm_sub_axis, angle=radians(-20))
 for e in [small_left_arm, left_hand_anchor]+left_joint_axis]


# upper_arm init
upper_arm = draw_part('upper_arm', skincolor)
upper_arm_main_axis = (p1-p2).norm()
upper_arm_sub_axis = upper_arm_main_axis.cross(front).cross(
    upper_arm_main_axis).norm()
# shoulder anchor
shoulder_anchor_pos = p2
shoulder_anchor, shoulder_axis = draw_arm_anchor(
    shoulder_anchor_pos-right*0.2, upper_arm_main_axis, upper_arm_sub_axis,
    radius=(p2-p2_).mag*1.1, color_=skincolor)

# small_arm init
small_arm = draw_part('small_arm', skincolor)
small_arm_main_axis = (p0-p1).norm()
small_arm_sub_axis = small_arm_main_axis.cross(front).cross(
    small_arm_main_axis).norm()
# joint anchor
joint_anchor_pos = p1
joint_anchor, joint_axis = draw_arm_anchor(
    joint_anchor_pos, small_arm_main_axis, small_arm_sub_axis,
    radius=0.8, color_=skincolor)

# hand anchor
hand_anchor_pos = p0
hand_anchor = draw_anchor(hand_anchor_pos)

# regular arm
[e.rotate(origin=p2, axis=upper_arm_sub_axis, angle=radians(20))
 for e in [upper_arm, joint_anchor, small_arm, hand_anchor] +
 shoulder_axis + joint_axis]
# modify init axis
upper_arm_main_axis = (joint_anchor.pos-shoulder_anchor.pos).norm()
upper_arm_sub_axis = upper_arm_main_axis.cross(front).cross(
    upper_arm_main_axis).norm()
small_arm_main_axis = (hand_anchor.pos-joint_anchor.pos).norm()
small_arm_sub_axis = small_arm_main_axis.cross(front).cross(
    small_arm_main_axis).norm()
[e.rotate(origin=joint_anchor.pos, axis=small_arm_main_axis,
          angle=radians(-80)) for e in [small_arm]]
[e.rotate(origin=joint_anchor.pos, axis=small_arm_sub_axis, angle=radians(20))
 for e in [small_arm, hand_anchor]+joint_axis]
small_arm_main_axis = (hand_anchor.pos-joint_anchor.pos).norm()
small_arm_sub_axis = small_arm_main_axis.cross(front).cross(
    small_arm_main_axis).norm()

distant_light(direction=up*10-front*2, color=color.gray(0.8))

print('Click scene to continue')
scene.waitfor('click keydown')


def motion_backing():
    m1 = motion_backing_upper_arm()
    if m1:
        return True
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


def motion_waizhan(angle=radians(2/1.5)):
    print('Waizhan ...')
    for _ in range(30):
        rate(30)
        axis = - joint_axis[1].axis
        origin = shoulder_anchor.pos
        [e.rotate(origin=origin, angle=angle, axis=axis)
         for e in [upper_arm, joint_anchor, small_arm, hand_anchor] +
         shoulder_axis + joint_axis]
    print('Done.')


def motion_quzhou(angle=radians(2)):
    print('Quzhou ...')
    for _ in range(55):
        rate(30)
        axis = joint_axis[0].axis.cross(joint_axis[1].axis)
        origin = joint_anchor.pos
        [e.rotate(origin=origin, angle=angle, axis=axis)
         for e in [small_arm, hand_anchor] + joint_axis]
    print('Done.')


def motion_taishou(angle=radians(2)):
    print('Taishouing ...')
    for _ in range(35):
        rate(30)
        if _ % 5 == 0:
            axis = joint_axis[0].axis.cross(joint_axis[1].axis)
            origin = joint_anchor.pos
            [e.rotate(origin=origin, angle=angle, axis=axis)
             for e in [small_arm, hand_anchor] + joint_axis]

        axis = shoulder_axis[0].axis.cross(shoulder_axis[1].axis)
        origin = shoulder_anchor.pos
        [e.rotate(origin=origin, angle=angle, axis=axis)
         for e in [upper_arm, joint_anchor, small_arm, hand_anchor] +
         shoulder_axis + joint_axis]
    print('Done.')


def motion_shenchu(angle=radians(2)):
    print('Shenchuing ...')
    for _ in range(40):
        rate(30)
        axis = joint_axis[0].axis.cross(joint_axis[1].axis)
        origin = joint_anchor.pos
        [e.rotate(origin=origin, angle=angle, axis=axis)
         for e in [small_arm, hand_anchor] + joint_axis]

    time.sleep(0.5)
    for __ in range(2):
        for _ in range(40):
            rate(30)
            axis = shoulder_axis[0].axis.cross(shoulder_axis[1].axis)
            origin = shoulder_anchor.pos
            [e.rotate(origin=origin, angle=angle, axis=axis)
             for e in [upper_arm, joint_anchor, small_arm, hand_anchor] +
             shoulder_axis + joint_axis]

            axis = joint_axis[0].axis.cross(joint_axis[1].axis)
            origin = joint_anchor.pos
            [e.rotate(origin=origin, angle=-angle, axis=axis)
             for e in [small_arm, hand_anchor] + joint_axis]

        for _ in range(40):
            rate(30)
            axis = shoulder_axis[0].axis.cross(shoulder_axis[1].axis)
            origin = shoulder_anchor.pos
            [e.rotate(origin=origin, angle=-angle, axis=axis)
             for e in [upper_arm, joint_anchor, small_arm, hand_anchor] +
             shoulder_axis + joint_axis]

            axis = joint_axis[0].axis.cross(joint_axis[1].axis)
            origin = joint_anchor.pos
            [e.rotate(origin=origin, angle=angle, axis=axis)
             for e in [small_arm, hand_anchor] + joint_axis]
    print('Done.')


def motion_back():
    print('Backing ...')
    time.sleep(0.2)
    while True:
        rate(30)
        if not motion_backing():
            break
    time.sleep(0.2)
    print('Done.')


while True:
    print('Press q for quzhou, t for taishou, w for waizha, s for shenshou, b for back')
    ev = scene.waitfor('click keydown')
    if ev.event == 'click':
        print('Clicked at', ev.pos)
    else:
        print('Pressed key', ev.key)
        if ev.key == 't':
            for _ in range(2):
                motion_taishou()
                motion_back()
        if ev.key == 'q':
            for _ in range(2):
                motion_quzhou()
                motion_back()
        if ev.key == 'w':
            for _ in range(2):
                motion_waizhan()
                time.sleep(0.2)
                motion_back()
        if ev.key == 's':
            motion_shenchu()
        if ev.key == 'b':
            motion_back()
