# coding: utf-8

from vpython import arrow, box, color, cylinder, radians, rate, scene, sphere, vector


class Arm:
    def __init__(self):
        self.shoulder_pos = vector(0, 0, 0)

        self.upper_arm_len = 10
        self.upper_arm_rad = 1
        self.upper_arm_axis = vector(1, 0, 0)
        self.upper_arm_rot = 45

        self.small_arm_len = 10
        self.small_arm_rad = 1
        self.small_arm_flex = 30

    def init_parts(self):
        self.shoulder = sphere(pos=self.shoulder_pos,
                               radius=self.upper_arm_rad*2,
                               color=color.cyan, opacity=0.5)
        axis_0 = self.upper_arm_axis.norm()
        axis_1 = axis_0.cross(axis_0.rotate(1)).norm()
        axis_1.rotate(axis=axis_0, angle=radians(self.upper_arm_rot))
        axis_2 = axis_0.cross(axis_1).norm()
        self.upper_arm_x0 = arrow(pos=self.shoulder_pos, axis=axis_0*3,
                                  color=color.red, shaftwidth=0.2)
        self.upper_arm_y0 = arrow(pos=self.shoulder_pos, axis=axis_1*3,
                                  color=color.green, shaftwidth=0.2)
        self.upper_arm_z0 = arrow(pos=self.shoulder_pos, axis=axis_2*3,
                                  color=color.blue, shaftwidth=0.2)
        self.upper_arm = box(pos=self.shoulder_pos+axis_0*self.upper_arm_len/2,
                             axis=axis_0,
                             length=self.upper_arm_len,
                             height=self.upper_arm_rad,
                             width=self.upper_arm_rad*1.5,
                             color=color.cyan, opacity=0.5)
        joint_pos = self.shoulder_pos + axis_0 * self.upper_arm_len
        self.upper_arm_x1 = arrow(pos=joint_pos, axis=axis_0*3,
                                  color=color.red, shaftwidth=0.2)
        self.upper_arm_y1 = arrow(pos=joint_pos, axis=axis_1*3,
                                  color=color.green, shaftwidth=0.2)
        self.upper_arm_z1 = arrow(pos=joint_pos, axis=axis_2*3,
                                  color=color.blue, shaftwidth=0.2)

        self.joint = sphere(pos=joint_pos, radius=self.upper_arm_rad*1.5,
                            color=color.cyan, opacity=0.5)
        axis_small_arm = axis_0.rotate(axis=axis_1,
                                       angle=radians(self.small_arm_flex))
        self.small_arm = box(pos=joint_pos+axis_small_arm*self.small_arm_len/2,
                             axis=axis_small_arm,
                             length=self.small_arm_len,
                             height=self.small_arm_rad,
                             width=self.small_arm_rad*1.5,
                             color=color.cyan, opacity=0.5)


scene.title = 'Arm v0'
X = arrow(pos=vector(-10, -10, -10), axis=vector(5, 0, 0),
          color=color.red, shaftwidth=0.5)
Y = arrow(pos=vector(-10, -10, -10), axis=vector(0, 5, 0),
          color=color.green, shaftwidth=0.5)
Z = arrow(pos=vector(-10, -10, -10), axis=vector(0, 0, 5),
          color=color.blue, shaftwidth=0.5)

arm = Arm()
arm.init_parts()
