# code: utf-8
from mpl_toolkits.mplot3d import proj3d
from matplotlib import animation
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect("equal")

# draw sphere


def init():
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x = np.cos(u)*np.sin(v)
    y = np.sin(u)*np.sin(v)
    z = np.cos(v)
    sphere = ax.plot_wireframe(x, y, z, color="r")
    sphere.__setattr__('target', 1)
    return sphere


def is_target(x, t='target'):
    return hasattr(x, t)


def animate(i):
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    u += i*5
    x = np.cos(u)*np.sin(v)
    y = np.sin(u)*np.sin(v)
    z = np.cos(v)
    ax.findobj(is_target)[0].remove()
    sphere = ax.plot_wireframe(x, y, z, color="r")
    sphere.__setattr__('target', 1)
    return sphere


ani = animation.FuncAnimation(fig=fig,
                              func=animate,
                              frames=100,
                              init_func=init,
                              interval=20,
                              blit=False)

plt.show()
