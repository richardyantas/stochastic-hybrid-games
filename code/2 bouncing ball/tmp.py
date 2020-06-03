
import matplotlib.pyplot as plt
import random

#import turtle


# make the equations, latex document. conclusion, show results. 
# add bouncing ball 

# controller F -> v 
y = +5
v = 0
dt = 0.1
'''
    u = 1,2,3 controller()
    rango  v , y  
'''
class state:
    def __init__(self,t,y,v):
        self.t = t
        self.y = y 
        self.v = v 

class model:
    def __init__(self,si):
        self.dt = 0.1
        self.gravity = 9.81
        self.states = []
        self.actions = []
        self.si = si
    
    def controller(self,s): #u = self.controller(s)
        if ( s.y >= 4 and s.v >= 0 ):  # Hit 
            s.v = -(0.9+float(random.randint(0,10))/100.0 )*s.v - 4
        if ( s.y >= 4 and -4 >= s.v and s.v < 0 ):
            s.v = -4
        return

    def simulation(self) :
        s = self.si
        self.states.append(s)
        self.controller(s)
        for i in range(0,1000): 
            self.controller(s)     # Hit ? 
            if ( s.y <= 0 ):           # Bouncing
                s.v = -(0.85+float(random.randint(0,12)/100) )*s.v
            v = s.v - self.dt*self.gravity
            y = s.y + self.dt*s.v
            t = s.t + self.dt
            s = state(t,y,v)
            self.states.append(s)
            #self.actions.append(u)

    def plot(self):
        t = []
        y = []
        for i in self.states:
            t.append(i.t)
            y.append(i.y)        
        plt.plot(t,y)
        plt.grid(True)
        plt.show()

A = model( state(0,7+random.randint(0,3),3) )
A.simulation()
A.plot()

'''
import turtle
import random
 
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Bouncing Ball Simulator")
#wn.tracer(0)

ball = turtle.Turtle()
ball.shape("circle")
ball.color("green")
ball.penup()
ball.speed(0)
ball.goto(0,200)
ball.dy = 2
ball.dx = 0

gravity = 0.1

while True:
    ball.dy -= gravity 
    ball.dx -= 5 
    ball.sety(ball.ycor()+ball.dy)
    # ball.setx(ball.xcor()+ball.dx)
    if ball.xcor() > 300:
        ball.dx *= -1
    if ball.xcor() < -300:
        ball.dx *= -1
    if ball.ycor() < -300:
        ball.dy *= -1
'''