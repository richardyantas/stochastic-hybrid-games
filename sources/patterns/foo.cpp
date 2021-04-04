#include <ibex.h>
#include <string>
#include <vector>
#include <queue>
#include <cmath>
#include <json/json.h>
#include "foo.h"

using namespace std;
using namespace ibex;

void propagation()
{
  Variable x(2);
  Function m0 = Function(x, Return(x[0] + 1 ));
  Function m1 = Function(x, Return(1 - x[1] ));
  

  // Function m0 = Function(x, Return( -factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
  //                                   - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
  //                                   + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
  //                                   + factorE*r*0.008801843/(0.1*p)  
  //                                   ,rate*( 0.1*p - x[1]) ) ); // 10s time to assent

  Variable x(1);
  Function m = Function(x, Return( 1-Interval(0,1)*x[0] ));
  cout << "m: " <<  m << endl;
}
