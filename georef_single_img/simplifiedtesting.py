import math
import numpy as np
from matplotlib import pyplot as plt

distancetocorner = 1
x1 = 0
y1 = 0
yaw = 30

angletocorner = math.degrees(math.sin(24 / 35.9))
print(angletocorner)

angles = (angletocorner, angletocorner+(90-angletocorner)*2, angletocorner+(90-angletocorner)*2+angletocorner*2, 360-angletocorner)
print(angles)
angles = [x-yaw for x in angles]
print(angles)
newpoints = []
for a in angles:
    x2 = x1 + distancetocorner*math.cos(math.radians(a))
    y2 = y1 + distancetocorner*math.sin(math.radians(a))
    # print(x1, "+", distancetocorner*math.cos(math.radians(a)), y1, "+", distancetocorner*math.sin(math.radians(a)))
    newpoints.append((x2, y2))

print(newpoints)



data = np.asarray(newpoints)
x, y = data.T
plt.scatter(x,y)
plt.text(x[0], y[0], "0")
plt.text(x[1], y[1], "1")
plt.text(x[2], y[2], "2")
plt.text(x[3], y[3], "3")
plt.xlim(-2, 2)
plt.ylim(-2, 2)
plt.show()


topleft = newpoints[0]
bottomleft = newpoints[1]
bottomright = newpoints[2]
topright = newpoints[3]