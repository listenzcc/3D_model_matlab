# code: utf-8

from mpl_toolkits.mplot3d import proj3d
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect('equal')


class Sphere:
    def __init__(self, ax):
        u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        x = np.cos(u)*np.sin(v)
        y = np.sin(u)*np.sin(v)
        z = np.cos(v)
        self.xyz = np.concatenate(
            (x[:, :, np.newaxis],
             y[:, :, np.newaxis],
             z[:, :, np.newaxis]), axis=2)
        self.u0, self.v0 = 0, 0
        self.x0, self.y0, self.z0 = 0, 0, 0
        self.ax = ax

    def draw(self):
        trans_v = np.array([
            [1, 0, 0],
            [0, np.cos(self.v0), -np.sin(self.v0)],
            [0, np.sin(self.v0), np.cos(self.v0)]
        ])

        trans_u = np.array([
            [np.cos(self.u0), -np.sin(self.u0), 0],
            [np.sin(self.u0), np.cos(self.u0), 0],
            [0, 0, 1]
        ])

        xyz = np.matmul(self.xyz, np.matmul(trans_v, trans_u))
        sphere = ax.plot_wireframe(xyz[:, :, 0]+self.x0,
                                   xyz[:, :, 1]+self.y0,
                                   xyz[:, :, 2]+self.z0, color='r')
        sphere.__setattr__('___target___', 1)


sp = Sphere(ax)
sp1 = Sphere(ax)
sp1.x0, sp1.y0, sp1.z0 = 1, 1, 1
# sp.u0 = np.pi/4
# sp.draw()
# plt.show(block=True)


def is_target(x, t='___target___'):
    return hasattr(x, t)


for j in range(10000):
    print(j)
    # sp.u0 += np.pi/100
    sp.v0 += np.pi/50
    any(e.remove() for e in ax.findobj(is_target))
    sp.draw()
    sp1.draw()
    plt.ion()
    plt.pause(0.001)

print('done.')
