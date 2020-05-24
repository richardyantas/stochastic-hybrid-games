import os

T_ini = 23
V_ini = 2.3
E_ini = 1230
t_ini = 0.0
factorTe = 2.5
factorI  = 0.8
factorKe = 1
rate     = 0.01
TwaterIn = 22.5
tau      = 300

H = 5

# list -> segment list -> convert to string 
T_env    = "{2,3,4}"
T_in     = "{2,3,4}"
I        = "{2,3,4}"

def configXML():
	fin = open ("1.xml", "r")
	fout= open ("1c.xml","w+")
	while True:
		line = fin.readline()
		if (line == "//HOLDER_T_ini\n"):
			fout.write('const double T_ini = %5.2f; \n' % T_ini)
		if (line == "//HOLDER_V_ini\n"):
			fout.write('const double V_ini = %5.2f; \n' % V_ini)
		if (line == "//HOLDER_E_ini\n"):
			fout.write('const double E_ini = %5.2f; \n' % E_ini)
		if (line == "//HOLDER_t_ini\n"):
			fout.write('const double t_ini = %5.2f; \n' % t_ini)
		if (line == "//HOLDER_factorTe\n"):
			fout.write('const double factorTe = %5.2f; \n' % factorTe)
		if (line == "//HOLDER_factorI\n"):
			fout.write('const double factorI = %5.2f; \n' % factorI)
		if (line == "//HOLDER_factorKe\n"):
			fout.write('const double factorKe = %5.2f; \n' % factorKe)
		if (line == "//HOLDER_rateVo\n"):
			fout.write('const double rateVo = %5.2f; \n' % rate)
		if (line == "//HOLDER_TwaterIn\n"):
			fout.write('const double TwaterIn = %5.2f; \n' % TwaterIn)
		if (line == "//HOLDER_tau\n"):
			fout.write('const double tau = %5.2f; \n' % tau)
		if (line == "//HOLDER_T_env[H+1]\n"):
			fout.write('const double T_env[%d] = %s; \n' % (H+1,T_env))
		if (line == "//HOLDER_T_in[H+1]\n"):
			fout.write('const double T_in[%d] = %s; \n' % (H+1,T_in) )
		if (line == "//HOLDER_I[H+1]\n"):
			fout.write('const double I[%d] = %s; \n' % (H+1,I) )		
		else:
			fout.write(line)
		if not line :
			break
		#print(line.strip())
	fin.close()    
	fout.close()

def callUppaal():
	print("calling .. ")
	line = "/home/serendipita/Documents/software/uppaal64-4.1.20-stratego-7/bin-Linux/verifyta cat.xml query.q" 
	n = os.popen(line).readlines()
	l = n[11].split()
	l.pop(0)
	print(l[1])      
	
	# patterns = np.matrix('[0,-1,-1;7,-1,-1]')

configXML()
callUppaal()

# 1.-      Print patterns and zonotopes from c++ to xml, c++ Ibex code 6 callStratego generate xml 
# 2.-      callStratego in python 
a = 3
# Ibex  -> pre_test.xml
# Python -> call test.xml each tau
#f = open("pre_test.xml", "r")
#s = string(f.readline() )
#print(f.readline(),end="")
