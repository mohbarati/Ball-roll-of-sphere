import pygame
from pygame.locals import *
from math import cos, sin, sqrt, atan, copysign
import matplotlib.pyplot as plt

pygame.init()
sc = pygame.display.set_mode((650, 600))
red = (255, 0, 0)
blue = (100, 100, 255)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (30, 60, 30)
sc.fill(black)
font = pygame.font.SysFont(None, 70)


def distance(x, y):
    return sqrt(x**2 + y**2)


def Surface_touch(x, y, r, rsph):
    if int(distance(x, y) - r) <= rsph:
        return True
    else:
        return False


def draw_circle(c, x, y, r):
    pygame.draw.circle(sc, c, (x + 200, -y + 300), r)


def drawGrid():
    blockSize = 50  # Set the size of the grid block
    for x in range(0, 650, blockSize):
        for y in range(0, 600, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(sc, (0, 10, 10), rect, 1)


def draw_line(color, x_sph, y_sph, r_sph, theta):
    pygame.draw.line(
        sc,
        color,
        (x_sph + 200, y_sph + 300),
        (200 + r_sph * sin(theta), 300 - r_sph * cos(theta)),
        3,
    )


x_sph = 0
y_sph = 0
r_sph = 200
# -----------------
theta = 0.001
r_ball = 20
x = (r_sph + r_ball) * sin(theta)
y = (r_sph + r_ball) * cos(theta)
vx = 0
vy = 0
ax, ay = 0, 0
m = 1
g = 9.8
c_drag = 0
drawGrid()
draw_circle(yellow, x_sph, y_sph, r_sph)
draw_circle(white, x, y, r_ball + 1.32)
T = []
X = []
Y = []
VX = []
VY = []
AX = []
AY = []
counter = 0
# ---------------
pygame.display.update()
cont = True
dt = 0.001
while cont:
    if 300 - y > 600 - r_ball:
        cont = False
    counter += 1
    T.append(counter * dt)
    X.append(x)
    Y.append(y)
    VX.append(vx)
    VY.append(vy)
    AX.append(ax)
    AY.append(ay)
    drawGrid()

    draw_circle(yellow, x_sph, y_sph, r_sph)
    draw_line(blue, x_sph, y_sph, r_sph, 0)
    draw_circle(white, x, y, r_ball + 1)
    if distance(x, y) < (r_ball + r_sph + 1.315):
        theta_final = theta
        draw_line(blue, x_sph, y_sph, r_sph, theta)
        img = font.render(f"Angle = {round(theta,2)} rad", True, red)
        sc.blit(img, (50, 510))
    else:
        draw_line(blue, x_sph, y_sph, r_sph, theta_final)
        img = font.render(f"Angle = {round(theta_final,2)} rad", True, red)
        sc.blit(img, (50, 510))
    if Surface_touch(x, y, r_ball, r_sph):
        Rx = m * g * sin(theta) - c_drag * copysign(1, vx) * abs(vx)
        Ry = m * g * cos(theta) - c_drag * copysign(1, vy) * abs(vy)
    else:
        Rx = 0
        Ry = 0
    ax = Rx
    ay = Ry - m * g
    vx += ax * dt
    vy += ay * dt
    x += vx * dt
    y += vy * dt
    theta = atan(x / y)

    pygame.display.update()
    sc.fill(black)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == K_q:
                cont = False
        if event.type == QUIT:
            cont = False
    sc.fill(black)

pygame.quit()
print("Theta at the point of seperation of the balls: ", theta_final)
# -----------------------
# Visualizing the data points
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, sharex=True, gridspec_kw={"hspace": 0})
fig.suptitle("Modeling a Small Ball Rolling Off a Bigger ball")
ax1.plot(T, VX, ".--", c="g", linewidth=2, markersize=2)
ax1.set_ylabel("vx      ", rotation=0)
ax1.grid("true")
ax2.plot(T, VY, ".--", c="r", linewidth=2, markersize=2)
ax2.set_ylabel("vy      ", rotation=0)
ax2.grid("true")
ax3.plot(T, AX, ".-", c="b", linewidth=1, markersize=1)
ax3.set_ylabel("ax      ", rotation=0)
ax3.grid("true")
ax4.plot(T, AY, ".--", c="g", linewidth=2, markersize=2)
ax4.set_xlabel("time (s)")
ax4.set_ylabel("ay      ", rotation=0)
ax4.grid("true")
plt.show()
