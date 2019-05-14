
import numpy as np
import matplotlib.pyplot as plt
from math import exp,pow
from matplotlib.widgets import Slider, Button, RadioButtons


def solve(x,y,T,num,A,d,va,re,vo,Mc,Ce,A_t,A_c,dm,dq,Kc,vp,Tin,Ie,Te,Tinamp,Teamp,Ieamp):

	#Ie  = Ieamp*gauss(86400/2,86400/8,T,num) 
	#Tin = Tinamp*gauss(86400/2,86400/8,T,num)
	#Te  = Teamp*gauss(86400/2,86400/8,T,num)

	for i in range(0,num-1):
		if abs(y[i,0]-100*vo.g[i,0]) <= 0:
			y[i+1,0] = y[i,0]  
		else:
			y[i+1,0] = y[i,0] - vp*T*sign( y[i,0]-100*vo.g[i,0] )            

		Mc = y[i,0]
		A[i,0]  =  ( va.g[i,0]*(-dm/Mc) - Kc*A_t/(Mc*Ce) )
		d[i,0]  =  A_c*Ie[i,0]/(Mc*Ce) + va.g[i,0]*Tin[i,0]*dm/Mc + Kc*A_t*Te[i,0]/(Mc*Ce)
		x[i+1,0]=  x[i,0]/(1-A[i,0]*T) + re.g[i,0]*dq/(Mc*Ce)*T/(1-A[i,0]*T) + d[i,0]*T/(1-A[i,0]*T)

		if x[i,0] < 60:
			re.g[i+1,0] = 1
			an = i
		if x[i,0] >= 60:
			if i - an <= 300:
				re.g[i+1,0] = 1
			else:
				re.g[i+1,0] = 0

		if x[i,0] >= 100:
			x[i,0] = 100

def sign(x):
    if x<0:
        return -1
    if x == 0:
        return 0
    if x>0:
        return 1

def getSec(hrs):
	return int(hrs*60*60)

def gauss(mean, sig, T, num):
	g = np.zeros((num,1))
	for i in range(1,num-1):
		g[i,0] = 5*(1/(2.5066*sig))*exp(-pow((T*i-mean),2)/(2*pow(sig,2)))
	return g

class resistance:
	def __init__(self,num):
		self.g = np.zeros((num,1))
	def setOneValues(self,a,b):
		for i in range(a,b):
			self.g[i,0] = 1


class valve:
	def __init__(self,num):
		self.g = np.zeros((num,1))
	def setOneValues(self,a,b):
		for i in range(a,b):
			self.g[i,0] = 1


class piston:
	def __init__(self,num):
		self.g = np.ones((num,1))
	def setTwoValues(self,a,b):
		for i in range(a,b):
			self.g[i,0] = 2
	def setThreeValues(self,a,b):
		for i in range(a,b):
			self.g[i,0] = 3

def plotWidget(t,x,y,T,num,A,d,va,re,vo,Mc,Ce,A_t,A_c,dm,dq,Kc,vp,Tin,Ie,Te,Tinamp,Teamp,Ieamp):

	fig, ax = plt.subplots( figsize=(8, 6) )
	#fig, ax = plt.subplots()
	#plt.subplots_adjust(left=0.25, bottom=0.25)
	plt.subplots_adjust(left=0.35, bottom=0.25)
	#plt.figure(figsize=(10,15))
	#t = np.arange(0.0, 1.0, 0.001)
	#a0 = 5
	#f0 = 3
	delta_f = 5.0
	#s = a0*np.sin(2*np.pi*f0*t)
	l, = plt.plot(t, x, lw=1, color='red')
	plt.grid(True)

	plt.axis([0, 100000 , 0, 120])
	axcolor= 'lightgoldenrodyellow'

	#axfreq= plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
	#axflow = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)

	axflow   = plt.axes([0.05, 0.75, 0.16, 0.03], facecolor=axcolor)
	#axKc   = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
	axKc     = plt.axes([0.05, 0.8, 0.16, 0.03], facecolor=axcolor)

	axTinamp = plt.axes([0.05, 0.7, 0.16, 0.03], facecolor=axcolor)
	axTeamp  = plt.axes([0.05, 0.65, 0.16, 0.03], facecolor=axcolor)
	axIeamp  = plt.axes([0.05, 0.6, 0.16, 0.03], facecolor=axcolor)


	#axKc   = plt.axes([0.25, 0.00, 0.65, 0.03], facecolor=axcolor)
	#axKc  = plt.axes([0.1, 0.1, 0.65, 0.03], facecolor=axcolor)
	#sfreq = Slider(axfreq, 'Freq', 0.1, 30.0, valinit=f0, valstep=delta_f)


	sflow   = Slider(axflow, 'dm', 0.001, 0.1, valinit=0.02)
	sKc     = Slider(axKc, 'Kc', 0.001, 10, valinit=5)	
	sTinamp = Slider(axTinamp, 'Tina', 0.001, 100, valinit=40)	
	sTeamp  = Slider(axTeamp, 'Tena', 0.001, 100, valinit=48)	
	sIeamp  = Slider(axIeamp, 'Iena', 0.001, 2*1236*5000, valinit=1236*5000 )	


	def update(val):		

		Kc     = sKc.val
		dm     = sflow.val	
		Tinamp = sTinamp.val
		Teamp  = sTeamp.val
		Ieamp  = sIeamp.val					
		#freq = sfreq.val
		#l.set_ydata(amp*np.sin(2*np.pi*freq*t))

		Ie  = Ieamp*gauss(86400/2,86400/8,T,num) 
		Tin = Tinamp*gauss(86400/2,86400/8,T,num)
		Te  = Teamp*gauss(86400/2,86400/8,T,num)


		print("sdf")
		solve(x,y,T,num,A,d,va,re,vo,Mc,Ce,A_t,A_c,dm,dq,Kc,vp,Tin,Ie,Te,Tinamp,Teamp,Ieamp)
		l.set_ydata(x)
		fig.canvas.draw_idle()


	#sfreq.on_changed(update)
	sflow.on_changed(update)
	sKc.on_changed(update)
	sTinamp.on_changed(update)
	sTeamp.on_changed(update)
	sIeamp.on_changed(update)

	resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
	button  = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

	def reset(event):
		#sfreq.reset()
		sflow.reset()
		sKc.reset()
		sTinamp.reset()
		sTeamp.reset()
		sIeamp.reset()

	button.on_clicked(reset)

	rax   = plt.axes([0.05, 0.4, 0.15, 0.15], facecolor=axcolor)	
	radio = RadioButtons(rax, ('Temp', 'Irrad', 'Cost En'), active=0)

	def colorfunc(label):
		#l.set_ydata(Ie)
		#fig.canvas.draw_idle()
		l.set_color(label)		
		fig.canvas.draw_idle()
	radio.on_clicked(colorfunc)	

def plotSimple(t,x,Ie,re,va):
	plt.figure(1)
	plt.plot(t,x, label = 'Temperature')
	plt.plot(t,Ie/10, label = 'Irradiance')
	plt.plot(t, 10*re.g , '-r', label = 'Resistance')
	plt.plot(t, 10*va.g, 'black', label ='Valve')
	plt.legend()
	plt.grid(True)
