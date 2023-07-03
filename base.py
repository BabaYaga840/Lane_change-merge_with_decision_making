import matplotlib.pyplot as plt
import numpy as np
from sympy.solvers import nonlinsolve
from sympy import Symbol

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
    safed=15
    v1=V1.getv(t)
    v2=V2.getv(t)
    print(v1,v2)

    a2c=V1.maxa
    l1=V1.length/2
    l2=V2.length/2
    a1=-V1.mina
    a2=-V2.mina
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
    for i in range(j,pl.n):
        pl.getpl(i, -d/(t**2), st, st+t)
        pl.getpl(i, d/(t**2), st+t, st+t*2)


def chk(V1, V2, t):
    u = V1.getv(0)
    s = 0
    a = V1.maxa
    v = V2.getv(t)
    #print("----////",u,v,s)
    if v < (2 * vmax - u - a * t) :
        ub = u * t + 0.5 * a * (t ** 2 - 2 * (t - ((v  - u) / a + t) / 2) ** 2) + s
    else:
        ub = (vmax ** 2 - u ** 2) / (2 * a) + vmax * (t - (vmax - u) / a) - 0.5 * ((vmax - v ) ** 2) / a + s
    a = -a
    if v < (2 * vmin - u - a * t) :
        lb = (vmin ** 2 - u ** 2) / (2 * a) + vmin * (t - (vmin - u) / a) - 0.5 * ((vmin - v ) ** 2) / a + s
    else:
        lb = u * t + 0.5 * a * (t ** 2 - 2 * (t - ((v  - u) / a + t) / 2) ** 2) + s
    S=V2.getx(t)-V1.getx(0)
    print("////----",ub,S,lb)
    if S <= ub and S >= lb:
        return 1
    else:
        return 0


def get_path(V1, V2, t):
    u = V1.getv(0)
    s = V2.getx(t) - V1.getx(0)
    v = V2.getv(t)
    print("v,s",v,s,u)
    vmax = V1.maxv
    vmin = V1.minv
    amax=V1.maxa
    amin=V1.mina
    if s > (u + v) * t / 2:
        a = Symbol('a')
        t0 = Symbol('t0')
        sol = list(
            nonlinsolve([v - u - a * (2 * t0 - t), u * t + 0.5 * a * (t0 ** 2 + 2 * t0 * (t - t0) - (t - t0) ** 2) - s],
                        [a, t0]))
        # t0 = t / 2  # Symbol('t0')
        # a = solve(u * t + 0.5 * a * (t0 ** 2 + 2 * t0 * (t - t0) - (t - t0) ** 2) - s)
        # t1=t0
        for i in range(len(sol)):
            a = sol[i][0]
            t0 = sol[i][1]
            if a >= 0 and a <= amax and u + a * t0 <= vmax:

                print("rtdh")
                V1.upa(a, 0, t0)
                V1.upa(-a, t0, t)
                return 1
        """if a[0] >= 0 and a[0] <= amax and u + a[0] * t1[0] <= vmax:
            a = a[0]
            t0 = t1[0]
            V1.upa(a, 0, t0)
            V1.upa(-a, t0, t)
            return 1
        elif a[1] >= 0 and a[1] <= amax and u + a[1] * t1[1] <= vmax:
            a = a[1]
            t0 = t1[1]
            V1.upa(a, 0, t0)
            V1.upa(-a, t0, t)
            return 1"""

        a = ((vmax ** 2 - u ** 2) / 2 - vmax * (vmax - u) - ((vmax - u) ** 2) / 2) / (s - vmax * t)
        V1.upa(a, 0, (vmax - u) / a)
        V1.upa(-a, t - (vmax - v) / a, t)
        return 1
    else:

        a = Symbol('a')
        t0 = Symbol('t0')
        sol = list(nonlinsolve([v - u - a * (2 * t0 - t), u * t + 0.5 * a * (t0 ** 2 + 2 * t0 * (t - t0) - (t - t0) ** 2) - s],[a,t0]))
        #t0 = t / 2  # Symbol('t0')
        #a = solve(u * t + 0.5 * a * (t0 ** 2 + 2 * t0 * (t - t0) - (t - t0) ** 2) - s)
        #t1=t0
        for i in range(len(sol)):
            a=sol[i][0]
            t0=sol[i][1]
            if a <= 0 and a >= amin and u + a * t0 >= vmin:

                print("rtdh")
                V1.upa(a, 0, t0)
                V1.upa(-a, t0, t)
                return 1


        a = ((vmin ** 2 - u ** 2) / 2 - vmin * (vmin - u) - ((vmin - u) ** 2) / 2) / (s - vmin * t)
        V1.upa(a, 0, (vmin - u) / a)
        V1.upa(-a, t - (vmin - v) / a, t)
        return 1
    return 0


class graph:
    def __init__(self):
        self.n=0
        self.g=[]
        self.st=[]
        self.et=[]
    def add(self,a,st=0,et=30):
        self.g.append(a)
        self.st.append(st)
        self.et.append(et)
        self.n=self.n+1

    def plot(self,last=0):
        for i in range(self.n):
            plt.plot(t[int(self.st[i]/dt):int(self.et[i]/dt)],self.g[i][int(self.st[i]/dt):int(self.et[i]/dt)])
        if not last:
            plt.figure()

    def show(self):
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

    def addplot(self,l1,st=0,et=30):
        n=[]
        x=[]
        for i in range(int(simt/dt)):
            n.append((sum(self.a[0:i])*dt)+self.v)
        for i in range(int(simt/dt)):
            x.append((sum(n[0:i])*dt)+self.x)
        l1.add(x,st,et)

    def upa(self,a,t0,t1):
        for i in range(int(t0/dt),int(t1/dt)):
            self.a[i]=a+self.a[i]

    def score(self,veh,t):
        return 100/(((self.getx(t)-veh.getx(t))**2/100+(self.getv(t)-veh.getv(t)))+0.01)

    def follow(self,veh,t,et):
        self.a[int(t/dt):int(et/dt)]=veh.a[int(t/dt):int(et/dt)]

class platoon:
    def __init__(self,n,tx,tv):
        self.n=n
        #self.tx=tx
        #self.tv=tv
        self.veh=[]
        for i in range(self.n):
            self.veh.append(Car())
            self.veh[i].init(tx, tv)
        for i in range(self.n-1):
            self.veh[i].init(tx,tv)
            self.veh[i].upa(1,15,25)
            tx=tx-rss(self.veh[i],self.veh[i+1],0)
            print("----", rss(self.veh[i],self.veh[i+1],0))
        i=i+1
        self.veh[i].init(tx,tv)
        self.veh[i].upa(1, 15, 25)

    def addplot(self,l1,st=0,et=30):
        for i in range(self.n):
            self.veh[i].addplot(l1,st,et)

    def getpl(self,i,a,t0,t1):
        self.veh[i].upa(a,t0,t1)

    def chk(self,car,t):
        max = -1
        pos = -1
        for i in range(self.n):
            if(chk(car,self.veh[i],t)):
                score=car.score(self.veh[i],t)
                print("score ",i,score)
                if max<score:

                    max=score
                    pos=i
        print("pos",pos)
        return pos



"""pl1=platoon(10,20,15)
l1=graph()
lanesp(15,pl1,3,8,4)
#print(getd(pl1.veh[2],pl1.veh[3],1))
#print(getd(pl1.veh[2],pl1.veh[3],15))
pl1.addplot()



l1.plot()"""
