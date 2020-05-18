import os

T_ini = 23
V_ini = 2.3
E_ini = 1230
t_ini = 0.0

def configXML():
	fin = open ("anspretest.xml", "r")
	fout= open ("anstest.xml","w+")
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
		else:
			fout.write(line)
		if not line :
			break
		#print(line.strip())
	fin.close()    
	fout.close()

def callUppaal():
	print("calling .. ")
	#line = "./callStratego "+" "+str(float(s.T))+" "+str(float(s.V))+" "+str(float(s.E))+" "+str(float(s.t))+" "+controlName+" "+queryName+" "+pathUppaal            
	line = "./home/serendipita/Documents/software/uppaal64-4.1.20-stratego-7/bin-Linux/verifyta 1.xml 1.q" 
	n = os.popen(line).read()
	print(n)      
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
