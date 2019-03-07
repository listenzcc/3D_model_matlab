# code: utf-8
import mpl_toolkits
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
    return sphere


def animate(i):
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    u += i
    x = np.cos(u)*np.sin(v)
    y = np.sin(u)*np.sin(v)
    z = np.cos(v)
    ax.clear()
    sphere = ax.plot_wireframe(x, y, z, color="r")
    return sphere


ani = animation.FuncAnimation(fig=fig,
                              func=animate,
                              frames=100,
                              init_func=init,
                              interval=20,
                              blit=False)

plt.show()
