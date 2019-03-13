# code: utf-8

from vpython import *

ball = sphere(pos=vector(-5, 0, 0), radius=0.5, color=color.cyan)
wallR = box(pos=vector(6, 0, 0), size=vector(0.2, 12, 12), color=color.green)
wallL = box(pos=vector(-6, 0, 0), size=vector(0.2, 12, 12), color=color.green)
ball.velocity = vector(25, 0, 0)
deltat = 0.005
t = 0
ball.pos = ball.pos + ball.velocity*deltat
while t < 3:
    rate(1)
    ball.pos = ball.pos + ball.velocity*deltat
    if ball.pos.x > 6 or ball.pos.x < -6:
    	ball.velocity *= -1
    t = t + deltat
    wallR.rotate(pi/4)
    print(t)
