#pragma once
#include "common.h"
//#include "config.h"

namespace config
{
  void setFunction(){
    // const int n = 2;
    // Variable x(n);
    // double p,r; 
    // p = 1, r = 0; 
    // Function m0 = Function(x, Return(
    //     - factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
    //     - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
    //     + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
    //     + factorE*r*0.008801843/(0.1*p)  
    //     , rate*( 0.1*p - x[1]) )
    // ); // 10s time to assent
    // Affine2Vector y0 = Affine2Vector(W);
    // ivp_ode mode = ivp_ode( (m0), 0.0, y0);
    // simulation simu = simulation(&mode, sys.period, HEUN, 1e-5);
    // simu.run_simulation();
    // y0 = *(simu.list_solution_j.back().box_jnh_aff);
    // yo -> array of boxex export to file and read with a python file and plot and check what will happen
    // terminar las entradas y salidas del cpp project
    // lectura de jsons patterns.json y parameters.json to python project and simulate with valve in 1 all the time
    // add plot to the python project to  the simulation

  }

  void setModel(){

      // int modes[8][3] = { 
      //                     {1,0,0},
      //                     {1,1,0},
      //                     {2,0,0},
      //                     {2,1,0},
      //                     {3,0,1},
      //                     {3,1,1},
      //                     {2,0,1},
      //                     {2,1,1}
      //                   };
      // const int n = 2;
      // Variable x(n);
      // double p,r,f;
      // for(int i=0;i<8;i++){
      //   p = modes[i][0];
      //   r = modes[i][1];
      //   f = modes[i][2];
      //   Function mode = Function(x, Return( 
      //     - factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
      //     - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
      //     - f*0.001005026*(0.1*p-x[1])*(x[0]-Ti)/(0.1*p)            //  original -> 0.00009346739
      //     + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p)               
      //     + factorE*r*0.008801843/(0.1*p)  
      //     , rate*( 0.1*p - x[1]) ) 
      //   );
      //   sys.dynamics.push_back(mode);
      // }             
      


      const int n = 2;
      Variable x(n);
      double p,r; 
      p = 1, r = 0;  // f = 0
      Function m0 = Function(x, Return( 
        - factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
        - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
        + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
        + factorE*r*0.008801843/(0.1*p)  
        , rate*( 0.1*p - x[1]) ) 
      ); // 10s time to assent

      p = 1, r = 1;  // f = 0
      Function m1 = Function(x, Return( 
        - factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
        - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
        + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
        + factorE*r*0.008801843/(0.1*p)  
        , rate*( 0.1*p - x[1]) ) 
      ); // 10s time to assent

      p = 2, r = 0;  // f = 0
      Function m2 = Function(x, Return( 
        - factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
        - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
        + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
        + factorE*r*0.008801843/(0.1*p)  
        , rate*( 0.1*p - x[1]) ) 
      ); // 10s time to assent

      p = 2, r = 1; // f = 0
      Function m3 = Function(x, Return( 
        - factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
        - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)                                        
        + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
        + factorE*r*0.008801843/(0.1*p)  
        , rate*( 0.1*p - x[1]) ) 
      ); // 10s time to assent

      p = 3, r = 0; // f = 1
      Function m4 = Function(x, Return( 
        - factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
        - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
        - 0.001005026*(0.1*p-x[1])*(x[0]-Ti)/(0.1*p)            //  original -> 0.00009346739
        + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
        + factorE*r*0.008801843/(0.1*p)  
        , rate*( 0.1*p - x[1]) ) ); // 10s time to assent

      p = 3, r = 1; // f = 1
      Function m5 = Function(x, Return( 
        -factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
        - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
        - 0.001005026*(0.1*p-x[1])*(x[0]-Ti)/(0.1*p)            //  original -> 0.00009346739
        + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
        + factorE*r*0.008801843/(0.1*p)  
        ,rate*( 0.1*p - x[1]) ) 
      ); // 10s time to assent
      
      p = 2, r = 0; // f = 1
      Function m6 = Function(x, Return( 
        - factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
        - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
        - 0.001005026*(0.1*p-x[1])*(x[0]-Ti)/(0.1*p)            //  original -> 0.00009346739
        + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p)
        + factorE*r*0.008801843/(0.1*p)  
        , rate*( 0.1*p - x[1]) ) 
      ); // 10s time to assent

      p = 2, r = 1; // f = 1  
      Function m7 = Function(x, Return( 
        - factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
        - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
        - 0.001005026*(0.1*p-x[1])*(x[0]-Ti)/(0.1*p)           //  original -> 0.00009346739
        + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
        + factorE*r*0.008801843/(0.1*p)  
        , rate*( 0.1*p - x[1]) ) 
      ); // 10s time to assent
      
      sys.dynamics.push_back(m0);
      sys.dynamics.push_back(m1);    
      sys.dynamics.push_back(m2);
      sys.dynamics.push_back(m3);
      sys.dynamics.push_back(m4);
      sys.dynamics.push_back(m5);
      sys.dynamics.push_back(m6);
      sys.dynamics.push_back(m7);

      sys.nb_dynamics = sys.dynamics.size();
      return;
  }

}
