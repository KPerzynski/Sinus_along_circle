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

cylinder_lenght = 50
cylinder_radius = 60

s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=STANDALONE)

fig, ax = plt.subplots()

x = []
y = []

list_spline = []

s1.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
s1.Line(point1=(0.0, 0.0), point2=(cylinder_radius, 0.0))

# Compute the x and y coordinates for points on a sine curve

y = np.linspace(0,50,100)
# sampling rate
sr = 25
# sampling interval
ts = 1.0/sr
# amplituda
A = 0.5

y = np.arange(0,cylinder_lenght,ts)

# frequency of the signal
freq = 0.5
x = A*np.sin(2*np.pi*freq*y)

for i in range(len(x)):
    list_spline = list_spline + [(cylinder_radius+x[i], y[i])]

list_spline = list_spline + [(cylinder_radius, cylinder_lenght)]

#Drawing Spline
sp = ((list_spline[0]),)

for k in range(1,len(list_spline)):
    sp = sp + ((list_spline[k]),)

print(sp)

print("Plot the points using matplotlib:")
plt.plot(y, x)
plt.show()

s1.Spline(points=(sp))

#s1.Spline(points=((50.0, 0.0), (46.25, 6.25), (56.25, 8.75), (48.75, 17.5), (52.5, 22.5), (45.0, 28.75), (52.5, 36.25), (50.0, 38.75), (47.5, 47.5), (50.0, 50.0)))

s1.Line(point1=(cylinder_radius, cylinder_lenght), point2=(0.0, cylinder_lenght))
s1.Line(point1=(0.0, cylinder_lenght), point2=(0.0, 0.0))

p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Part-1']
p.BaseSolidRevolve(sketch=s1, angle=360.0, flipRevolveDirection=OFF)
s1.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']

# Job
job = mdb.Job(name='Job-1', model='Model-1')
job.writeInput()

# Submit the job
# job.submit()
# job.waitForCompletion()

# Save abaqus model

model_name = 'model_cylinder_A_'+ str(A) + '_freq_' + str(freq) + '_radius_' + str(cylinder_radius) + '_lenght_' + str(cylinder_lenght) + '_sampling_' + str(ts) +'.cae'

mdb.saveAs(model_name)
