
import numpy as np

class Point:
    def __init__(self,x=0,y=1):
        self.x = x
        self.y = y
    def __repr__(self):
        return "[%d,%d]" % (self.x,self.y)
    def __str__(self):
        return "["+ str(self.x)+"," + str(self.y)+ "]"

    def module(self):
        return self.x+self.y



class Line:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __repr__(self):
        return "[%d,%d]" % (self.x,self.y)
    def __str__(self):
        return "[%s,%s]" % (self.x.__str__(),self.y.__str__())



a = Point()
print(a)

x = [2,1]
y = [4,1]

#print(len(x))


t = {
    'dx': x,
    'dy': y
}

class foo:
    def __init__(self,t = {'dx':8,'dy':1}):
        self.t = t

    #def get_l(self):
    #    for i in t:
    #        for j in range(0,len(t[i])):
    #            print(t[i][j])
    def __repr__(self):        
        return "[%d,%d]" % (self.t['dx'],self.t['dy'])


#f = foo(t)
f = foo()

print(f)

#f.get_l()



#b= Point(0,7)
#print(b)






'''

a = Point(3,4)
b = Point(1,1)
print ( a.module() )

l = Line(a,b)
print(l)


x = 4
y = 3

n = {
    'x': x,
    'y': y
}

print(n)
print( "[%d,%d]" % (n['x'], n['y']) )



num = 10

irr = np.zeros((num,1))

I = irr[0:num]


e = {
    'I': I,  
    'T': "T"
}


print(e['I'][0])



y = []
y.append(4)
y.append(5)

print(y)
print(y[0])

y[0] = 7

print(y)


r = np.array(y)

print(r)


for i in e:
    print(i)



for i in range(0,5):
    print(i)

'''


