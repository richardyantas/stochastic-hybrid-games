#include <ibex.h>
#include <vector>
#include <queue>
#include <iostream>
#include <sstream>
#include <cmath>

#include "Matplotlibcpp.h"

using namespace ibex;
namespace plt = matplotlibcpp;


void plotBox(IntervalVector Box, string color);

//(sign(x)+1)2

vector< vector<Interval> > run(vector<Function> modes, IntervalVector W, double period)
{
    vector< vector<Interval> > states;
    vector<Interval> temperature;
    vector<Interval> volume;

    Affine2Vector y0 = Affine2Vector(W);

    for(int i = 0; i < modes.size() ; i++)
    {
        
        ivp_ode  mode = ivp_ode(modes[i], 0.0, y0); // cambios de y0 a W
        simulation run = simulation(&mode, period, HEUN, 1e-5);
        run.run_simulation();
        y0 = *(run.list_solution_j.back().box_jnh_aff);

        for(int i = 1; i<period; i += 1)
        {
            temperature.push_back( run.get_tight(i)[0] );
            volume.push_back( run.get_tight(i)[1] );
        }
    }

    states.push_back(temperature);
    states.push_back(volume);

    return states;

}



int main()
{


    IntervalVector W(2);
    W[0]= Interval(40.0,40.1);
    W[1]= Interval(0.1,0.11);

    const int n = 2;
	Variable x(n);
    Interval Te(0.0, 30.0);
    Interval Ti(0.0,25.0);
    Interval I(0.0, 900.0);

    double period = 1*60; // CAMBIOS,  not works with 100

    // -9.34673995175876e-05(x[0]-Ti)/x[1]   ->   (Ti,v = 0,1) -> [Tmin - 0], max added temperature  zero
    

    /*
    Function m1 = Function(x, Return( -2.8811059759131854e-6*(x[0]-Te)/x[1] + 
    -9.34673995175876e-05*(x[0]-Ti)/x[1] - sign(0.1 - x[1])*9.34673995175876e-05*(x[0]-Ti)/x[1]
    + 0.7*0.7*8.403225763080125e-07*I/x[1] + 0.0048018432931886426/x[1]
    ,0.1*( Interval(0.1) - x[1]) ) );

    Function m2 = Function(x, Return( -2.8811059759131854e-6*(x[0]-Te)/x[1] + 
    -9.34673995175876e-05*(x[0]-Ti)/x[1] - sign(0.1 - x[1])*9.34673995175876e-05*(x[0]-Ti)/x[1]
    + 0.7*0.7*8.403225763080125e-07*I/x[1]
    ,0.1*( Interval(0.1) - x[1]) ) );

    Function m3 = Function(x, Return( -2.8811059759131854e-6*(x[0]-Te)/x[1] + 
    -9.34673995175876e-05*(x[0]-Ti)/x[1] - sign(0.2 - x[1])*9.34673995175876e-05*(x[0]-Ti)/x[1]
    + 0.7*0.7*8.403225763080125e-07*I/x[1] + 0.0048018432931886426/x[1]
    ,0.1*( Interval(0.2) - x[1]) ) );

    Function m4 = Function(x, Return( -2.8811059759131854e-6*(x[0]-Te)/x[1] + 
    -9.34673995175876e-05*(x[0]-Ti)/x[1] - sign(0.2 - x[1])*9.34673995175876e-05*(x[0]-Ti)/x[1]
    + 0.7*0.7*8.403225763080125e-07*I/x[1] 
    ,0.1*( Interval(0.2) - x[1]) ) );

    Function m5 = Function(x, Return( -2.8811059759131854e-6*(x[0]-Te)/x[1] + 
    -9.34673995175876e-05*(x[0]-Ti)/x[1] - sign(0.3 - x[1])*9.34673995175876e-05*(x[0]-Ti)/x[1]
    + 0.7*0.7*8.403225763080125e-07*I/x[1] + 0.0048018432931886426/x[1]
    ,0.1*( Interval(0.3) - x[1]) ) );

    Function m6 = Function(x, Return( -2.8811059759131854e-6*(x[0]-Te)/x[1] + 
    -9.34673995175876e-05*(x[0]-Ti)/x[1] - sign(0.3 - x[1])*9.34673995175876e-05*(x[0]-Ti)/x[1]
    + 0.7*0.7*8.403225763080125e-07*I/x[1] 
    ,0.1*( Interval(0.3) - x[1]) ) );

   */

    
    cout << 5*sign( Interval(0.3) - Interval(0.5) ) << endl;
    Function m1 = Function(x, Return( 0.005*x[0], 0.001*sign(0.001) ));
    Function m2 = Function(x, Return( -0.005*x[0] + Interval(0.001), 0.001*sign(0.001) ));
    Function m3 = Function(x, Return( +0.005*x[0], 0.001*sign(-0.001) ));
    Function m4 = Function(x, Return( -0.005*x[0], 0.001*sign(-0.001) ));
    //Function m5 = Function(x, Return( +0.005*x[0]+(sign(x[0]-1)+1)/2, 0.001*sign(0.001) ));
    Function m5 = Function(x, Return( sign( int(x[0]) ), 0.001*sign(0.001) ));
    Function m6 = Function(x, Return( -0.005*x[0], 0.001*sign(0.001) ));
    


    vector< vector<double> > Temperature(2);
    vector< vector<double> > Volume(2);

    vector< vector<Interval> > states;

    vector<Function> modes;
    
    modes.push_back(m1);
    modes.push_back(m2);
    modes.push_back(m3);
    modes.push_back(m4);
    modes.push_back(m5);
    modes.push_back(m6);

    
    //model(modes, W);
    states = run(modes, W, period);

    cout << "State Size: " << states[0].size() << endl;

    for (int j = 0; j < states[0].size(); j++)
    {
        Temperature[0].push_back(states[0][j].lb());
        Temperature[1].push_back(states[0][j].ub());

        Volume[0].push_back(states[1][j].lb());
        Volume[1].push_back(states[1][j].ub());
        
    }

    cout << "W:" << W << endl;
    
    plt::figure(1);
    plt::plot(Temperature[0] ,"black"); 
    plt::plot(Temperature[1] ,"red");  
    plt::xlim( 0.0, 15*60.0);
    plt::ylim( 0.0, 70.0);  
    plt::xlabel("time");
    plt::ylabel("Temp");
    plt::grid(true);


    plt::figure(2);
    plt::plot(Volume[0] ,"black"); 
    plt::plot(Volume[1] ,"red");  
    plt::xlim( 0.0, 15*60.0);
    plt::ylim( 0.0, 0.4);  
    plt::xlabel("time");
    plt::ylabel("Volume");
    plt::grid(true);
    plt::show();


    //plt::figure(3);
    //plotBox(W, "black");

    for(int i=1;i<period;i+=5)// 5 -> 1
    {
        //cout <<  i << ".- " << run.get_tight(i) <<  endl;

        //cout << "EXP  = " << (run.get_tight(i)[0] - Te)/x[1] << "--" << run.get_tight(i)[1] << endl;
        //cout << "dif: " << -2.8811059759131854e-06*(run.get_tight(i)[0] - Te)/run.get_tight(i)[1] - 8.403225763080125e-07*I/run.get_tight(i)[1] << endl;
        //cout <<  -2.8811059759131854e-06*(run.get_tight(i)[0] - Te)/run.get_tight(i)[1] + 8.403225763080125e-07*I/run.get_tight(i)[1] << endl;
        //cout << 0.001*( Interval(0.2,0.25) - run.get_tight(i)[1]) << endl;
      //  plotBox( run.get_tight(i), "-r");                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
    }
    

    //cout << "POST = " <<  y0.itv() << endl;
    //plotBox(y0.itv(), "-r");


    //cout << "EXPERIMENT = " << Interval(-50,-50.1)/Interval(5,5.1) << endl; // EMPTY
    //cout << "EXPERIMENT = " << Interval(-50,50.1)/Interval(-5,5.1) << endl;  // ENTIRE
    //cout << "EXPERIMENT = " << Interval(-50,50.1)-Interval(-5,5.1) << endl;  // ENTIRE

     
    /*
    plt::xlim( 30.0, 50.0);
    plt::ylim( 0.0, 0.3);  
    plt::xlabel("Temp");
    plt::ylabel("Vol");
    plt::grid(true);
    */

    


    plt::show();


    return 0;
}

void plotBox(IntervalVector Box, string color) // bl, bu
{
    double x1 = Box[0].lb();
    double y1 = Box[1].lb();
    double x2 = Box[0].ub();
    double y2 = Box[1].ub();

    int n = 5;
    vector<double> x(n), y(n); 
    // Change to x[0] = x1;
    x.at(0) = x1;y.at(0) = y1;
    x.at(1) = x1;y.at(1) = y2;
    x.at(2) = x2;y.at(2) = y2;
    x.at(3) = x2;y.at(3) = y1;
    x.at(4) = x1;y.at(4) = y1;

    plt::plot(x, y, color);              
}
