import os


def forecast(self,X,pivotWindow,predictionSize):
        days_in_year = pivotWindow
        differenced = list()
        #print(X)   
        for i in range(days_in_year, len(X)):
            value = X[i] - X[i - days_in_year]
            differenced.append(value)
        # fit model
        model = ARIMA(differenced, order=(7,0,1))
        model_fit = model.fit(disp=0)
        # multi-step out-of-sample forecast
        start_index = len(differenced)
        end_index   = start_index + predictionSize
        #end_index   = start_index + 49#6
        forecast    = model_fit.predict(start=start_index, end=end_index)
        #print(forecast)
        # invert the differenced forecast to something usable
        history = [x for x in X]
        day = 1
        pred = []
        for yhat in forecast:
            #inverted = inverse_difference(history, yhat, days_in_year)
            inverted = yhat + history[-days_in_year] 
            #print('Day %d: %f' % (day, inverted))
            pred.append(inverted)
            history.append(inverted)
            day += 1
        return pred


                     
def configXML(self, f, it):
    fin = open (f[0], "r")
    fout= open (f[1], "w+")
    t_min = int(it)+1 # +1    - t_min = int(self.state_curr.t/60)  #  ???????????????????????????????
    print("configXML t_min it:", t_min)
    #print("Predicting perturbations ..  ")
    #pTe = self.forecast(list(self.Te[t_min-60*24:t_min]), 5*60, 59)
    #pI  = self.forecast(list(self.I[t_min-60*24:t_min]), 5*60, 59)
    pat_size = len(self.pattern_curr)
    a = list( self.Te[ t_min : t_min + self.H_uppaal] ) 
    b = list( self.I [ t_min : t_min + self.H_uppaal] )
    c = list( self.Ti[ t_min : t_min + self.H_uppaal] )
    d = list( self.t [ t_min : t_min + self.H_uppaal] )
    e = list( self.v [ t_min : t_min + self.H_uppaal] )
    f = list( self.pattern_curr[ 0: pat_size])
    T_env_string = '{'+','.join([str(elem) for elem in a] )+'}'
    I_string     = '{'+','.join([str(elem) for elem in b] )+'}'
    #T_env_string = '{'+','.join([str(elem) for elem in pTe ])+'}'
    #I_string     = '{'+','.join([str(elem) for elem in pI  ])+'}'
    T_in_string  = '{'+','.join([str(elem) for elem in c] )+'}'
    t_string     = '{'+','.join([str(elem) for elem in d] )+'}'
    va_string    = '{'+','.join([str(elem) for elem in e] )+'}'
    pat_ans_string = '{'+','.join([str(elem) for elem in f ] ) +'}'
    #print("pattern_curr: ",self.pattern_curr)
    #print("pat sent to uppaal: ",pat_ans_string)
    #print("size: ",pat_size)
    #print("Te sent to uppaal: %d "%(t_min),self.Te[ t_min:t_min+15])
    while True:
        line = fin.readline()
        if (line == "//HOLDER_T_ini\n"):
            fout.write('const double T_ini    = %5.5f; \n' % self.state_curr.T)
        if (line == "//HOLDER_V_ini\n"):
            fout.write('const double V_ini    = %5.5f; \n' % self.state_curr.V)
        if (line == "//HOLDER_E_ini\n"):
            fout.write('const double E_ini    = %5.5f; \n' % self.state_curr.E)
        if (line == "//HOLDER_t_ini\n"):
            fout.write('const double t_ini    = %5.5f; \n' % self.state_curr.t)
        if (line == "//HOLDER_u\n"):
            fout.write('int u                 = %d; \n' % int(self.state_curr.t/60) )
        if (line == "//HOLDER_taumin\n"):
            fout.write('int taumin            = %d; \n' % int(tau/60) )
        if (line == "//HOLDER_factorTe\n"):
            fout.write('const double factorTe = %5.5f; \n' % factorTe)
        if (line == "//HOLDER_factorI\n"):
            fout.write('const double factorI  = %5.5f; \n' % factorI)
        if (line == "//HOLDER_factorKe\n"):
            fout.write('const double factorKe = %5.5f; \n' % factorKe)
        if (line == "//HOLDER_rateVo\n"):
            fout.write('const double rateVo   = %5.5f; \n' % rate)
        if (line == "//HOLDER_TwaterIn\n"):
            fout.write('const double TwaterIn = %5.5f; \n' % TwaterIn)
        if (line == "//HOLDER_tau\n"):
            fout.write('const double tau      = %5.5f; \n' % tau)
        if (line == "//HOLDER_T_env[H+1]\n"):
            fout.write('const double T_env[%d]= %s; \n' % (self.H_uppaal,T_env_string) )
        if (line == "//HOLDER_T_in[H+1]\n"):
            fout.write('const double T_in[%d] = %s; \n' % (self.H_uppaal,T_in_string) )
        if (line == "//HOLDER_I[H+1]\n"):
            fout.write('const double I[%d]    = %s; \n' % (self.H_uppaal,I_string) )
        if (line == "//HOLDER_t[H+1]\n"):
            fout.write('const double t[%d]    = %s; \n' % (self.H_uppaal,t_string) )
        if (line == "//HOLDER_va[H+1]\n"):                                                  # ????
            fout.write('const double va[%d]   = %s; \n' % (self.H_uppaal,va_string) )		
        if (line == "//HOLDER_modeAns\n"):
            fout.write('const int modeAns     = %d; \n' % (self.d) )
        if (line == "//HOLDER_mvalve\n"):
            fout.write('int mvalve            = %d; \n' % (self.mode.v) )
        if (line == "//HOLDER_robot\n"):
            fout.write('int robot             =  0; \n')
        else:
            fout.write(line)
        if not line :
            break
    return


def readUppaalValues(self,v):
    v.pop(0)
    for i in range(0,len(v)):
        v[i] = v[i][1:len(v[i])-1].split(",")
        v[i][0] = float(v[i][0])
        v[i][1] = float(v[i][1])
    #values = self.coordToVector(values)
    l = [None]*self.nrSteps
    print("v len: ",len(v))
    for i in range(0,len(v)-1):
        if (v[i][0] == v[i+1][0] and v[i+1][0]!=self.nrSteps*self.step ) :
            it = int(v[i][0]/self.step)
            l[it] = int(v[i+1][1])
    for i in range(0,self.nrSteps):
        if l[i] == None:
            l[i] = 0
    print("l:", l)
    return l


def callUppaal(self,f):
    print("calling Uppaal .. ")
    line = "/home/serendipita/Documents/Ans/AugustFiles/software/uppaal64-4.1.20-stratego-7/bin-Linux/verifyta " + f[1] + " " + f[2] + " --learning-method 5"
    n = os.popen(line).readlines()
    i = 0
    #print("line:  ",n)
    while(1):
        if n[i] == "ppos:\n":
            ppos = n[i+1].split()
        if n[i] == "visitedPatterns:\n":
            visitedPatterns = n[i+1].split()
        if n[i] == "mode:\n":
            mode  = n[i+1].split()
        if n[i] == "flag:\n":
            flag  = n[i+1].split()
        if n[i] == "Tnext:\n":
            Tnext = n[i+1].split()
        if n[i] == "zi:\n":
            zi = n[i+1].split()
        if n[i] == "mvalve:\n":
            mvalve = n[i+1].split()
            break
        i = i + 1
    mvalve = self.readUppaalValues(mvalve)
    ppos   = self.readUppaalValues(ppos)
    mode   = self.readUppaalValues(mode)
    flag   = self.readUppaalValues(flag)
    visitedPatterns = self.readUppaalValues(visitedPatterns)
    
    #print("Tnext: ", Tnext)
    #print("zi: ", zi)
    Tnext = Tnext[2][1:len(Tnext[2])-1].split(",")
    zi    = zi[2][1:len(zi[2])-1].split(",")
    print("Tnext uppaal: ",Tnext[1])
    print("zonotope uppaal:  ",zi[1])
    index = len(ppos)-1
    for i in range(0,len(ppos)):
        if ppos[index]==1:
            break
        index = index -1
    pt = mode[0:index]
    print("pt: ", pt)
    #gValves.append(mvalve[0:index])
    return pt

def test(self,s):
        s_test = state(s.t,s.V,s.T,s.E)
        taumin   = int(tau/60)
        for i in range(self.it,self.it+taumin):
            Es = s_test.E + self.dt*self.mode.r*2  # dt = 0.1
            Vs = s_test.V + self.dt*rate*( 0.1*self.mode.p - s_test.V) # 0.5 = rate 0.01 = rate            self.rate_volume_change = 0.0002 # 0.193 
            Ts = s_test.T + self.dt*(1/(0.1*self.mode.p))*(
                        - factorTe*2.8811059759131854e-06*(s_test.T-self.Te[i]) 
                        - self.mode.v*9.34673995175876e-05*(s_test.T-self.Ti[i])                 # valve
                        - self.mode.f*factorKe*0.001005026*(0.1*self.mode.p-s_test.V)*(s_test.T-self.Ti[i])
                        + factorI*0.7*0.7*8.403225763080125e-07*self.I[i]
                        + self.mode.r*0.008801843 )#0.00048018432931886426
            s_test.E = Es
            s_test.V = Vs
            s_test.T = Ts
            s_test.t = s_test.t + self.dt        
        print("then: ",s_test, " mode: ",self.mode)
        return s_test

def trapezoideToRectangleInterpolation(a, nnum):
    for i in range(0,len(a)):
        if a[i] != 1.0 and  a[i] != 0.0:
            a[i] = 0.0
    return a