// g++ -frounding-math -ffloat-store -I/usr/local/include -I/usr/local/include/ibex  -O3 -DNDEBUG -Wno-deprecated -frounding-math  -o main main.cpp -L/usr/local/lib -libex -lprim -lClp -lCoinUtils

// g++ -frounding-math -ffloat-store -I/usr/local/include/ibex  -o main main.cpp -libex -lprim -lClp -lCoinUtils

// g++  -I/usr/local/include/ibex  -o main main.cpp -libex -lprim

#include <ibex/ibex.h>
#include <vector>
#include <queue>
#include <iostream>
#include <sstream>
#include <cmath>

#include "LSwitchedSystem.h"
#include "LUtils.h"
#include "LMatplotlibcpp.h"

using namespace ibex;
using namespace LSwitchedSystem;

// Matplotlib
// sudo apt-get install python-matplotlib python-numpy python2.7-dev
