"""
#python 2.x
"""
import numpy as np
import math
import matplotlib.pyplot as plt

from abaqus import *
from abaqusConstants import *
from driverUtils import *

executeOnCaeStartup()

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


def sineAroundCircle(cx, cy, radius, amplitude, angle, frequency):
    p = Point()
    p.x = cx + (radius + amplitude * np.sin(frequency * angle)) * np.cos(angle)
    p.y = cy + (radius + amplitude * np.sin(frequency * angle)) * np.sin(angle)
    return p

Mdb()

s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)

cx=0
cy=0
radius=50
amp=0.5
frequency=30
pt= Point()
depth = 50

fig, ax = plt.subplots()

x = []
y = []

list_spline = []

for i in range(1, 360):
    angle = i * math.pi / 180
    pt = sineAroundCircle(cx, cy, radius, amp, angle, frequency)
    line1, = ax.plot(pt.x, pt.y, 'o')
    x.append(pt.x)
    y.append(pt.y)
    list_spline = list_spline + [(pt.x, pt.y)]

plt.show()

# Drawing lines
# for j in range(360-1):
#     s.Line(point1=(x[j],y[j]), point2=(x[j-1],y[j-1]))

# sp = ((list_abaqus[0]),)
#
# for k in range(1,len(list_abaqus)):
#     sp = sp + ((list_abaqus[k]),)
# print(sp)

#Drawing Spline
sp = ((list_spline[0]),)

for k in range(1,len(list_spline)):
    sp = sp + ((list_spline[k]),)

sp = sp + ((list_spline[0]),)

#print(sp)

s.Spline(points=(sp))

# N = 2
# n_points = 50
# r0 = 10.
# rf = 20.
#
# theta = np.linspace(0,2*np.pi*N, n_points)
# r = r0 + (rf -r0) *theta/(2*np.pi*N)
#
# x_new = r*np.cos(theta)
# y_new = r*np.sin(theta)
#
# print(x_new)
# print(y_new)
#
# s.Spline(zip(x_new,y_new))


p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Part-1']
p.BaseSolidExtrude(sketch=s, depth=depth)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Part-1']
del mdb.models['Model-1'].sketches['__profile__']

# Job
job = mdb.Job(name='Job-1', model='Model-1')
job.writeInput()

# Submit the job
# job.submit()
# job.waitForCompletion()

# Save abaqus model

model_name = 'model_cylinder_CX_' + str(cx) + '_CY_' + str(cy) + '_Rad_' + str(radius) + '_Amp_' + str(amp) + '_freq_' + str(frequency)+ '_depth_' + str(depth) + '.cae'

mdb.saveAs(model_name)
