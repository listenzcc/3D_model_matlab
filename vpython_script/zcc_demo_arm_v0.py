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
        self.upper_arm_axis = vector(-1, 0, 0)
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
        axis_1 = axis_0.cross(axis_0.rotate(1)).norm()
        axis_1.rotate(axis=axis_0, angle=radians(self.upper_arm_rot))
        axis_2 = axis_0.cross(axis_1).norm()

        # draw upper_arm
        self.upper_arm = cylinder(pos=self.shoulder_pos,
                                  axis=axis_0 * self.upper_arm_len,
                                  radius=self.upper_arm_rad,
                                  color=color.cyan, opacity=0.5)

        # draw xyz 0
        self.upper_arm_x0 = arrow(pos=self.shoulder_pos, axis=axis_0*self.note_len,
                                  color=color.red, radius=self.sketch_rad)
        self.upper_arm_y0 = arrow(pos=self.shoulder_pos, axis=axis_1*self.note_len,
                                  color=color.green, radius=self.sketch_rad)
        self.upper_arm_z0 = arrow(pos=self.shoulder_pos, axis=axis_2*self.note_len,
                                  color=color.blue, radius=self.sketch_rad)

        # cal joint_pos
        self.joint_pos = self.shoulder_pos + axis_0 * self.upper_arm_len

        # draw xyz 1
        self.upper_arm_x1 = arrow(pos=self.joint_pos, axis=axis_0*self.note_len,
                                  color=color.red, radius=self.sketch_rad)
        self.upper_arm_y1 = arrow(pos=self.joint_pos, axis=axis_1*self.note_len,
                                  color=color.green, radius=self.sketch_rad)
        self.upper_arm_z1 = arrow(pos=self.joint_pos, axis=axis_2*self.note_len,
                                  color=color.blue, radius=self.sketch_rad)

    def init_joint(self):
        # draw joint
        self.joint = sphere(pos=self.joint_pos, radius=self.joint_rad,
                            color=color.cyan, opacity=0.5)

    def init_small_arm(self):
        # cal axis 0, 1
        axis_0 = self.upper_arm_axis.norm()
        axis_1 = axis_0.cross(axis_0.rotate(1)).norm()
        axis_1.rotate(axis=axis_0, angle=radians(self.upper_arm_rot))

        # draw small_arm
        self.small_arm = cylinder(pos=self.joint_pos,
                                  axis=axis_0 * self.small_arm_len,
                                  radius=self.small_arm_rad,
                                  color=color.cyan, opacity=0.5)
        self.small_arm.rotate(axis=axis_1, angle=radians(self.small_arm_flex))


scene.title = 'Arm v0'
scene.forward = vector(0, 0, -1)

arm = Arm()
arm.init_parts()
