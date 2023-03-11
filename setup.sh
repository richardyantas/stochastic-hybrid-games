

# model

# network

# RL

# https://locuslab.github.io/mpc.pytorch/
# https://github.com/AtsushiSakai/PythonRobotics#nonlinear-model-predictive-control-with-c-gmres
# https://github.com/yangyutu/DeepReinforcementLearning-PyTorch/tree/master/Example

# environments: https://github.com/p-christ/Deep-Reinforcement-Learning-Algorithms-with-PyTorch/tree/master/environments

# training -> model trought - network

# controller - test 

# policy 

# git push bitbucket HEAD


# https://www.youtube.com/watch?v=wI2w0GwNcGs&ab_channel=SimonsInstitute

# https://linuxconfig.org/bash-scripting-tutorial#h6-simple-bash-if-else-statement

# git submodule add https://github.com/open-source-parsers/jsoncpp lib/jsoncpp
# git remote add origin https://github.com/richardyantas/uppaalLibrary
# git remote remove origin
# git remote add origin https://github.com/richardyantas/uppaalLibrary.git

# ➜  bin git:(main) ./test_config 
# ➜  bin git:(main) echo $LD_LIBRARY_PATH
# ➜  bin git:(main)

# alias uppaaltest="/home/serendipita/Documents/Ans/AugustFiles/software/uppaal64-4.1.20-stratego-7/bin-Linux/verifyta"
# alias uppaal="/home/serendipita/Documents/Ans/AugustFiles/software/uppaal64-4.1.20-stratego-7/uppaal"

# Automate make and test operation from one file
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/serendipita/Documents/uppaalLibrary/build/lib/

# alias uppaaltest="/home/serendipita/Documents/Ans/AugustFiles/software/uppaal64-4.1.20-stratego-7/bin-Linux/verifyta"
# alias uppaal="/home/serendipita/Documents/Ans/AugustFiles/software/uppaal64-4.1.20-stratego-7/uppaal"

# ../lib/uppaal/bin-Linux/verifyta
# ../lib/uppaal/uppaal

#  /home/serendipita/Documents/uppaalLibrary/lib/uppaal/uppaal test/foo.xml

if [ $1 = "build" ]; then
  #export LD_LIBRARY_PATH=/home/serendipita/Documents/uppaalLibrary/build/lib/${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/serendipita/Documents/uppaalLibrary/build/lib/
  # export LD_LIBRARY_PATH=/home/serendipita/Documents/uppaalLibrary/build/lib/${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
  echo "* Compiling libraries and dependencies(Only once)"
  cd build
  cmake ..
  make
  cd ..
elif [ $1 = "run" ]; then  
  echo "* Running test/main.py test/foo.xml test/foo.q"
  python test/main.py lib/uppaal/bin-Linux/verifyta test/foo.xml test/foo.q  
elif [ $1 = "tests" ]; then
  echo "#######################################"
  echo "# run test(important) TDD Preferences #"
  echo "#######################################"
  echo ""
  echo ""
  #echo "testing test_json ... "
  #./build/bin/test_json ./test/static_json.json
  #echo "done"
  echo "testing test_lib_config ... "
  ./build/bin/test_libconfig
  echo "done\n"
  #echo "testing test_mylib ... "
  #./build/bin/test_mylib
  #echo "done\n"
elif [ $1 = "uppaal" ]; then  
  cd test/
  ../lib/uppaal/uppaal foo.xml
  cd ..
else
  echo "No option Found ..\n"
fi
