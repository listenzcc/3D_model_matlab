# coding: utf-8

from vpython import arrow, box, color, cylinder, radians, rate, scene, sphere, vector


class Arm:
    def __init__(self):
        self.up = vector(1, 0, 0)
        self.right = vector(0, 1, 0)
        self.front = vector(0, 0, 1)
        self.note_len = 20

        self.sketch_rad = 3

        self.heart_pos = vector(0, 0, 0)
        self.heart_rad = 5

        self.shoulder_pos = vector(0, 30, 0)
        self.shoulder_rad = 8

        self.upper_arm_len = 40
        self.upper_arm_rad = 5
        self.upper_arm_axis = -self.up
        self.upper_arm_subaxis = self.front
        self.upper_arm_rot = 0

        self.joint_rad = 6

        self.small_arm_len = 40
        self.small_arm_rad = 5
        self.small_arm_flex = 30

    def init_parts(self):
        self.init_heart()
        self.init_sketch()
        self.init_shoulder()
        self.init_upper_arm()
        self.init_joint()
        self.init_small_arm()

    def back_parts(self):
        # cal axis 0, 1, 2
        axis_0 = self.upper_arm_axis.norm()
        axis_2 = self.upper_arm_subaxis.norm()

        # return False, if we are fine
        if all([(abs(axis_0.diff_angle(-self.up)) < radians(3)),
                (abs(axis_2.diff_angle(self.front)) < radians(3)),
                (self.small_arm_flex == 30)]):
            return False

        # back axis_0
        if abs(axis_0.diff_angle(-self.up)) < radians(3):
            axis_0 = -self.up
        else:
            axis_0 = axis_0.rotate(
                axis=axis_0.cross(-self.up), angle=radians(2))

        # back axis_2
        if abs(axis_2.diff_angle(self.front)) < radians(3):
            axis_2 = self.front
        else:
            axis_2 = axis_2.rotate(axis=axis_2.cross(
                self.front), angle=radians(2))

        # setting backed parameters
        self.upper_arm_axis = axis_0.norm()
        self.upper_arm_subaxis = axis_2.norm()
        if abs(self.small_arm_flex) - 30 < 3:
            self.small_arm_flex = 30
        else:
            if self.small_arm_flex > 30:
                self.small_arm_flex -= 2
            else:
                self.small_arm_flex += 2

        return True

    def update_parts(self):
        self.update_upper_arm()
        self.update_joint()
        self.update_small_arm()

    def update_upper_arm(self):
        # cal axis 0, 1, 2
        axis_0 = self.upper_arm_axis.norm()
        axis_2 = self.upper_arm_subaxis.norm()
        axis_1 = axis_0.cross(axis_2).norm()

        # update upper_arm
        self.upper_arm.axis = axis_0 * self.upper_arm_len
        self.upper_arm_x0.axis = axis_0 * self.note_len
        self.upper_arm_y0.axis = axis_1 * self.note_len
        self.upper_arm_z0.axis = axis_2 * self.note_len

        self.joint_pos = self.shoulder.pos + axis_0 * self.upper_arm_len

        self.upper_arm_x1.pos = self.joint_pos
        self.upper_arm_y1.pos = self.joint_pos
        self.upper_arm_z1.pos = self.joint_pos

        self.upper_arm_x1.axis = axis_0 * self.note_len
        self.upper_arm_y1.axis = axis_1 * self.note_len
        self.upper_arm_z1.axis = axis_2 * self.note_len

    def update_joint(self):
        self.joint.pos = self.joint_pos

    def update_small_arm(self):
        # cal axis 0, 1, 2
        axis_0 = self.upper_arm_axis.norm()
        axis_2 = self.upper_arm_subaxis.norm()
        axis_1 = axis_0.cross(axis_2).norm()

        self.small_arm.pos = self.joint.pos
        self.small_arm.axis = axis_0 * self.small_arm_len
        self.small_arm.rotate(axis=axis_1, angle=radians(self.small_arm_flex))

    def init_heart(self):
        # draw heart
        sphere(pos=self.heart_pos, radius=self.heart_rad,
               color=color.cyan, opacity=0.5)
        arrow(pos=self.heart_pos, axis=self.up*self.note_len,
              color=color.red, radius=self.sketch_rad)
        arrow(pos=self.heart_pos, axis=self.right*self.note_len,
              color=color.green, radius=self.sketch_rad)
        arrow(pos=self.heart_pos, axis=self.front*self.note_len,
              color=color.blue, radius=self.sketch_rad)

    def init_sketch(self):
        # draw sketch
        cylinder(pos=self.heart_pos, axis=self.up, color=color.white,
                 radius=self.sketch_rad)
        cylinder(pos=self.heart_pos, axis=self.shoulder_pos-self.heart_pos,
                 color=color.white, radius=self.sketch_rad)

    def init_shoulder(self):
        # draw shoulder
        self.shoulder = sphere(pos=self.shoulder_pos, radius=self.shoulder_rad,
                               color=color.cyan, opacity=0.5)

    def init_upper_arm(self):
        # cal axis 0, 1, 2
        axis_0 = self.upper_arm_axis.norm()
        axis_2 = self.upper_arm_subaxis.norm()
        axis_1 = axis_0.cross(axis_2).norm()

        # draw upper_arm
        self.upper_arm = cylinder(pos=self.shoulder_pos,
                                  axis=axis_0 * self.upper_arm_len,
                                  radius=self.upper_arm_rad,
                                  color=color.cyan, opacity=0.5)

        # draw xyz 0
        self.upper_arm_x0 = arrow(pos=self.shoulder_pos,
                                  axis=axis_0*self.note_len,
                                  color=color.red, radius=self.sketch_rad)
        self.upper_arm_y0 = arrow(pos=self.shoulder_pos,
                                  axis=axis_1*self.note_len,
                                  color=color.green, radius=self.sketch_rad)
        self.upper_arm_z0 = arrow(pos=self.shoulder_pos,
                                  axis=axis_2*self.note_len,
                                  color=color.blue, radius=self.sketch_rad)

        # cal joint_pos
        self.joint_pos = self.shoulder_pos + axis_0 * self.upper_arm_len

        # draw xyz 1
        self.upper_arm_x1 = arrow(pos=self.joint_pos,
                                  axis=axis_0*self.note_len,
                                  color=color.red, radius=self.sketch_rad)
        self.upper_arm_y1 = arrow(pos=self.joint_pos,
                                  axis=axis_1*self.note_len,
                                  color=color.green, radius=self.sketch_rad)
        self.upper_arm_z1 = arrow(pos=self.joint_pos,
                                  axis=axis_2*self.note_len,
                                  color=color.blue, radius=self.sketch_rad)

    def init_joint(self):
        # draw joint
        self.joint = sphere(pos=self.joint_pos, radius=self.joint_rad,
                            color=color.cyan, opacity=0.5)

    def init_small_arm(self):
        # cal axis 0, 1
        axis_0 = self.upper_arm_axis.norm()
        axis_2 = self.upper_arm_subaxis.norm()
        axis_1 = axis_0.cross(axis_2).norm()

        # draw small_arm
        self.small_arm = cylinder(pos=self.joint_pos,
                                  axis=axis_0 * self.small_arm_len,
                                  radius=self.small_arm_rad,
                                  color=color.cyan, opacity=0.5)
        self.small_arm.rotate(axis=axis_1, angle=radians(self.small_arm_flex))


scene.title = 'Arm v0'
scene.forward = vector(0, 0, -1)
scene.up = vector(1, 0, 0)
scene.range = 100
arm = Arm()
arm.init_parts()


def moving_taiqi(arm=arm):
    # Taiqi
    print('Taiqi starts ...')
    for _ in range(30):
        axis_ = arm.upper_arm_axis.cross(arm.upper_arm_subaxis).norm()
        arm.upper_arm_axis = arm.upper_arm_axis.rotate(
            axis=axis_, angle=radians(2))
        arm.upper_arm_subaxis = arm.upper_arm_subaxis.rotate(
            axis=axis_, angle=radians(2))
        rate(30)
        arm.update_parts()
    print('Taiqi done')


def moving_waizhan(arm=arm):
    # Waizhan
    print('Waizhan starts ...')
    for _ in range(30):
        arm.upper_arm_axis = arm.upper_arm_axis.rotate(
            axis=arm.upper_arm_subaxis, angle=radians(-2))
        rate(30)
        arm.update_parts()
    print('Waizhan done.')


def moving_quzhou(arm=arm):
    # Quzhou
    print('Quzhou starts ...')
    for _ in range(30):
        arm.small_arm_flex += 2
        rate(30)
        arm.update_parts()
    print('Quzhou done.')


def moving_backing(arm=arm):
    # Back
    print('Backing...')
    while arm.back_parts():
        rate(30)
        arm.update_parts()
    print('Baking done')


input('press enter to start:')

moving_backing()

moving_taiqi()

moving_waizhan()

moving_quzhou()

moving_backing()

while True:
    m = input()

    if m == 't':
        moving_taiqi()

    if m == 'w':
        moving_waizhan()

    if m == 'q':
        moving_quzhou()

    if m == 'b':
        moving_backing()
