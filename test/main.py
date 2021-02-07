import os
import sys

# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/serendipita/Documents/uppaalLibrary/build/lib/
# g++ main.cpp -o main build/libconfig.so  #  works after export
# g++ -I. -L.  main.cpp  -o main -lconfig # works after export, is very important add -I. -L.
# g++ -I. -L./build/ main.cpp -o main -lconfig  # whe lib is in build
# ./main
#  g++ -I. -I./lib/jsoncpp/include/ -L./build/ -L./build/lib/ main.cpp -o main -lconfig -ljsoncpp
# Check uppaal version: last
# ./lib/uppaal/bin-Linux/verifyta foo.xml foo.q  #without --learning-method 5)
# ./lib/uppaal/uppaal foo.xml
# uppaaltest foo.xml foo.q
# uppaal setup or libconfig generation ? -> test with lfconfig file of other project
# import "../build/lib/libconfig.so" {
#     double get_num();
# };
#command_line = "../lib/uppaal/bin-Linux/verifyta foo.xml foo.q --learning-method 5"
#command_line = "../lib/uppaal/bin-Linux/veri sfyta " + f[0] + " " + f[1] + " --learning-method 5"
#command_line = "/home/serendipita/Documents/uppaalLibrary/lib/uppaal/bin-Linux/verifyta " + f[0] + " " + f[1] + " --learning-method 5"
# f = ["foo.xml","foo.q"]
# callUppaal(f)
#print(callUppaal(f))

def callUppaal():
  print("calling Uppaal .. ")
  command_line = str(sys.argv[1]) + " " + str(sys.argv[2]) + " " + str(sys.argv[3]) + " --learning-method 5"
  print(command_line)
  n = os.popen(command_line).readlines()
  print(n)

# python main.py ../lib/uppaal/bin-Linux/verifyta foo.xml foo.q 
callUppaal()
# /home/serendipita/Documents/Ans/AugustFiles/software/uppaal64-4.1.20-stratego-7/bin-Linux/verifyta

# */
# strategy plan = minE (total) [<=200] : <> Robot.Done

# /*

# */
# simulate 1 [<= 200] {\
#     Robot.cur_loc, Robot.dest\
# } under plan

# /*

# */
# saveStrategy("station_strategy.json", plan)


# /home/serendipita/Documents/uppaalLibrary/lib/uppaal/uppaal test/foo.xml