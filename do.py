import matplotlib.pyplot as plt
import numpy as np
from one import *



dt=0.01
simt=30
t=[]
vmax=80
vmin=10
am=4
tau=0.1


pl1=platoon(4,20,15)
l1=graph()
lanesp(15,pl1,3,8,4)
print(getd(pl1.veh[2],pl1.veh[3],1))
print(getd(pl1.veh[2],pl1.veh[3],15))
pl1.addplot()



l1.plot()
