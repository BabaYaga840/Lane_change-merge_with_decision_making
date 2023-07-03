import matplotlib.pyplot as plt
import numpy as np
from base import *

dt=0.01
simt=30
t=20
vmax=80
vmin=10
am=4
tau=0.1


pl1=platoon(5,100,30)
car=Car()
car.init(100,20)
pos=pl1.chk(car,20)
#30.0 40.0 500.1
l1=graph()
l2=graph()


u=car.getv(0)





"""for i in range(10):
   vi=pl1.veh[i].getv(20)
   si=pl1.veh[i].getx(20)
   print("check",chk(vi,si,20))"""




#lanesp(15,pl1,pos-2,16,2)
get_path(car,pl1.veh[pos],20)
lanesp(rss(car,pl1.veh[pos],20),pl1,pos,8,4)

car.follow(pl1.veh[pos],t,30)
#print(getd(pl1.veh[2],pl1.veh[3],1))
#print(getd(pl1.veh[2],pl1.veh[3],15))
pl1.addplot(l1)
car.addplot(l1,20,30)
car.addplot(l2)


l1.plot()
l2.plot(1)
l2.show()
