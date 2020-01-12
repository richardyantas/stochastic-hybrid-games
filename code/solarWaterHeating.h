#pragma once

#include <ibex/ibex.h>
using namespace std;
using namespace ibex;

namespace job
{

    class solver
    {
        Interval T;
        Interval V;
        Interval Te;
        Interval I;

        double n = 100000;
        double dt = 1/n;
        
        public:
            solver( Interval T = Interval(1.0,50.0),Interval V=Interval(1.0,10.1),
            Interval Te = Interval(0.0, 30.0),Interval I = Interval(1.0,900.0) ){
                this->T = T;
                this->V = V;
                this->Te = Te;
                this->I = I;
            };

            void run();
            IntervalVector POST(const sampledSwitchedSystem& sys,
     const IntervalVector W, const std::vector<int> pattern);
    };

    IntervalVector solver::POST(const sampledSwitchedSystem& sys,
     const IntervalVector W, const std::vector<int> pattern)
        for(int i=1; i<=n; i++)
        {
            //T = T - 2.8811059759131854e-06*(T-Te)/V + 8.403225763080125e-07*I;
            T = T + dt*T/V;
            V = V + dt*Interval(1.0,1.0);
            cout << "Time = " << dt*i << " T:" << T << " :V" << V << endl;
            //V = V + 0.001*( Interval(0.2,0.25) - V);
            
        }
    }

    void solver::run()
    {

        for(int i=1; i<=n; i++)
        {
            //T = T - 2.8811059759131854e-06*(T-Te)/V + 8.403225763080125e-07*I;
            T = T + dt*T/V;
            V = V + dt*Interval(1.0,1.0);
            cout << "Time = " << dt*i << " T:" << T << " :V" << V << endl;
            //V = V + 0.001*( Interval(0.2,0.25) - V);
            
        }

        
        cout << "POST = ( " << T << ", " << V << ")" << endl;  
    }


}