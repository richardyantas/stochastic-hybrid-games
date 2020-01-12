#include <ibex.h>
#include <vector>
#include <queue>
#include <iostream>
#include <sstream>
#include <cmath>

#include "Processing.h"
#include "Matplotlibcpp.h"

using namespace ibex;

// Matplotlib
// sudo apt-get install python-matplotlib python-numpy python2.7-dev

int main()
{
	//SolarWaterHeating();
	
	IntervalVector t_(3,Interval(0,1));
	IntervalVector x(3);

	x[0] = Interval(0,1);
	x[1] = Interval(2,3);
	x[2] = Interval(4,5);

	cout << x << endl;

	// IntervalVector r; // Error



	//solver();
	//test();
	testModel();
	//findPatternsForSolarWaterHeating();

	//plt::xlim(0, 10*10);
	return 0;
}

