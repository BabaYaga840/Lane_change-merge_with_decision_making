import matplotlib.pyplot as plt
import numpy as np

dt=0.01
simt=30
t=[]
vmax=80
vmin=10
am=4
tau=0.1

for i in range(int(simt/dt)):
    t.append(i*dt)

def rss(V1,V2,t):
    safed=0
    v1=V1.getv(t)
    v2=V2.getv(t)
    #a2c=V2.geta(t)
    a2c=(V2.getv(t+tau)-V2.getv(t))/tau
    l1=V1.length/2
    l2=V2.length/2
    a1=V1.mina
    a2=V2.mina
    if a1>=a2:
        return (a2c/2)*(a2c/a2+1)*(tau**2)+v2*(a2c/a2+1)*tau+(v2**2/(2*a2)-v1**2/(2*a1))+l1+l2+safed
    else:
        if tau>=(v1-v2)/(a2c+a1) and tau<=(v1*a2/a1-v2)/(a2c+a2):
            return (v2-v1)*tau+(tau**2)*(a1+a2c)/2+(v1-v2-(a1+a2c)*tau)**2/(2*(a2-a1))+l1+l2+safed
        else:
            return a2c*(a2c/a2+1)*(tau**2)/2+v2*(a2c/a2+1)*tau+((v2**2)/(2*a2)-(v1**2)/(2*a1))+l1+l2+safed


def getd(v1,v2,t):
    return v1.getx(t)-v2.getx(t)

def lanesp(d,pl,j,t,st):
    t=t/2
    for i in range(j):
        pl.getpl(i, d/(t**2), st, st+t)
        pl.getpl(i, -d/(t**2), st+t, st+t*2)

class graph:
    def __init__(self):
        self.n=0
        self.g=[]

    def add(self,a):
        self.g.append(a)
        self.n=self.n+1

    def plot(self):
        for i in range(self.n):
            plt.plot(t,self.g[i])
        plt.show()

class Car:
    def __init__(self):
        self.x=0
        self.v=0
        self.a=np.zeros(int(simt/dt))
        self.length=2
        self.mina=-am
        self.maxa=am
        self.maxv=vmax
        self.minv=vmin

    def init(self,x,v):
        self.x=x
        self.v=v

    def getx(self,t):
        n=[]
        for i in range(int(simt/dt)):
            n.append((sum(self.a[0:i])*dt)+self.v)
        return sum(n[0:int(t/dt+1)])*dt+self.x

    def getv(self,t):
        return sum(self.a[0:int(t / dt + 1)]) * dt+self.v

    def geta(self,t):
        return self.a[int(t/dt+1)]

    def addplot(self):
        n=[]
        x=[]
        for i in range(int(simt/dt)):
            n.append((sum(self.a[0:i])*dt)+self.v)
        for i in range(int(simt/dt)):
            x.append((sum(n[0:i])*dt)+self.x)
        l1.add(x)

    def upa(self,a,t0,t1):
        for i in range(int(t0/dt),int(t1/dt)):
            self.a[i]=a

class platoon:
    def __init__(self,n,tx,tv):
        self.n=n
        #self.tx=tx
        #self.tv=tv
        self.veh=[]
        for i in range(self.n):
            self.veh.append(Car())
        for i in range(self.n-1):
            self.veh[i].init(tx,tv)
            tx=tx-rss(self.veh[i],self.veh[i+1],0)
            print("----", rss(self.veh[i],self.veh[i+1],0))
        i=i+1
        self.veh[i].init(tx,tv)

    def addplot(self):
        for i in range(self.n):
            self.veh[i].addplot()

    def getpl(self,i,a,t0,t1):
        self.veh[i].upa(a,t0,t1)

