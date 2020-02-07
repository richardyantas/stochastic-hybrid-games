#include <ibex.h>
#include <vector>
#include <queue>
#include <iostream>
#include <sstream>
#include <cmath>

#include "Matplotlibcpp.h"
#include "read.h"
#include "system.h"
#include "safeTools.h"

using namespace ibex;
namespace plt = matplotlibcpp;

#define e 2.718281828

//#define NB_K 4
//#define NB_D 20

void plotBox(IntervalVector Box, string color);
void plotIntervalVector(vector<Interval> feature, string x_name, string y_name, double xlimit, double ylimit);
void render(vector< IntervalVector > states, double horizont);

IntervalVector postTest(vector<Function> modes, IntervalVector W, double period, vector< IntervalVector > &states)
{    
    Affine2Vector y0 = Affine2Vector(W);
    for(int i = 0; i < modes.size() ; i++)
    {
        ivp_ode  mode = ivp_ode(modes[i], 0.0, y0); // cambios de y0 a W
        simulation run = simulation(&mode, period, HEUN, 1e-5);
        run.run_simulation();
        y0 = *(run.list_solution_j.back().box_jnh_aff);

        for(int t = 1; t<period; t += 1)
        {
            cout << run.get_tight(t) << endl;
            states.push_back( run.get_tight(t) );
        }
        
    }
    return y0.itv();
}


int main()
{
    //  Model Simulation 
    /*

    CVSReader v_ = CVSReader("../valve.csv");
    CVSReader d_ = CVSReader("../Solargis_min15_Almeria_Spain.csv");

    map<string,vector<double>> v = v_.getFeatures();
    map<string,vector<double>> d = d_.getFeatures();

    systemModel sys = systemModel(15*60, 24*4*15*60, state(0,40,0,0), d);
    sys.run();
    vector<state> states  = sys.states;

    */

   // DynIbex Simulation

    int NB_K = 3;
    int NB_D = 20;


    IntervalVector R(2);
    R[0] = Interval(40.0,80.0);
    R[1] = Interval(0.09,0.31);

    IntervalVector W(2);
    
    //W[0] = Interval(40.0,40.1);  // if you dont define is ENTIRE the second variable:
    //W[1] = Interval(0.2,0.21);
    
    //W[0] = Interval(40.0,45.1);
    //W[1] = Interval(0.09,0.31);

    W[0] = Interval(44.0,44.1);
    W[1] = Interval(0.1,0.11);

    IntervalVector B(2);
    B[0] = Interval(0.0,0.0);
    B[1] = Interval(0.0,0.0);

    IntervalVector S(2);
    S[0] = Interval(20.0, 100.0);
    S[1] = Interval(0.05, 0.4);

    const int n = 2;
	Variable x(n);
    Interval Te(0.0, 30.0);
    Interval Ti(20.0,25.0);
    Interval I(0.0, 900.0);

    //int period = 1*60; // CAMBIOS,  not works with 100

    // -9.34673995175876e-05(x[0]-Ti)/x[1]   ->   (Ti,v = 0,1) -> [Tmin - 0], max added temperature  zero


    sampledSwitchedSystem sys;
    //sys.period = 15*60;
    sys.period = 5*60; // critical 
    //sys.period = 10*60;
    //sys.period = 25;

    //sys.period = 3*60;
    //sys.period = 2*60;
    sys.states.push_back(W);    
         
    double p,r;   
    p = 1, r = 0; 
    Function m1 = Function(x, Return( - 2.8811059759131854e-6*(x[0]-Te)/(0.1*p)                                        
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
                                            + 0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
                                            + r*0.008801843/(0.1*p)  
                                            ,0.5*( 0.1*p - x[1]) ) ); // 10s time to assent
    p = 1, r = 1; 
    Function m2 = Function(x, Return( - 2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)                                            
                                            + 0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
                                            + r*0.008801843/(0.1*p)  
                                            ,0.5*( 0.1*p - x[1]) ) ); // 10s time to assent


    p = 2, r = 0; 
    Function m3 = Function(x, Return( - 2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
                                            + 0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
                                            + r*0.008801843/(0.1*p)  
                                            ,0.5*( 0.1*p - x[1]) ) ); // 10s time to assent

    cout << "m3: " << m3 << endl;

    p = 2, r = 1; 
    Function m4 = Function(x, Return( - 2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)                                        
                                            + 0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
                                            + r*0.008801843/(0.1*p)  
                                            ,0.5*( 0.1*p - x[1]) ) ); // 10s time to assent
    p = 3, r = 0; 
    Function m5 = Function(x, Return( - 2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
                                            - 0.001005026*(0.1*p-x[1])*(x[0]-Ti)/(0.1*p)            //  original -> 0.00009346739
                                            + 0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
                                            + r*0.008801843/(0.1*p)  
                                            ,0.5*( 0.1*p - x[1]) ) ); // 10s time to assent
    p = 3, r = 1; 
    Function m6 = Function(x, Return( - 2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
                                            - 0.001005026*(0.1*p-x[1])*(x[0]-Ti)/(0.1*p)            //  original -> 0.00009346739
                                            + 0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
                                            + r*0.008801843/(0.1*p)  
                                            ,0.5*( 0.1*p - x[1]) ) ); // 10s time to assent

    p = 2, r = 0; 
    Function m7 = Function(x, Return( - 2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
                                            - 0.001005026*(0.1*p-x[1])*(x[0]-Ti)/(0.1*p)            //  original -> 0.00009346739
                                            + 0.7*0.7*8.403225763080125e-07*I/(0.1*p)
                                            + r*0.008801843/(0.1*p)  
                                            ,0.5*( 0.1*p - x[1]) ) ); // 10s time to assent
    p = 2, r = 1;     
    Function m8 = Function(x, Return( - 2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
                                            - 0.001005026*(0.1*p-x[1])*(x[0]-Ti)/(0.1*p)           //  original -> 0.00009346739
                                            + 0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
                                            + r*0.008801843/(0.1*p)  
                                            ,0.5*( 0.1*p - x[1]) ) ); // 10s time to assent

    

   /*
    Function m1 = Function( x, Return(Interval(1),Interval(1))  );
    Function m2 = Function( x, Return(Interval(1),Interval(1))  );
    Function m3 = Function( x, Return(Interval(1),Interval(1))  );
    Function m4 = Function( x, Return(Interval(1),Interval(1))  );
    Function m5 = Function( x, Return(Interval(1),Interval(1))  );
    Function m6 = Function( x, Return(Interval(1),Interval(1))  );
    Function m7 = Function( x, Return(Interval(1),Interval(1))  );
    Function m8 = Function( x, Return(Interval(1),Interval(1))  );
    */


    sys.dynamics.push_back(m1);
    sys.dynamics.push_back(m2);
    sys.dynamics.push_back(m3);
    sys.dynamics.push_back(m4);
    sys.dynamics.push_back(m5);
    sys.dynamics.push_back(m6);
    sys.dynamics.push_back(m7);
    sys.dynamics.push_back(m8);
    



    sys.nb_dynamics = sys.dynamics.size();



    //cout << "DYNAMIC: " << sys.dynamics.size() << endl;

    /*
    double horizont = 1.5*sys.dynamics.size()*sys.period;
    vector< IntervalVector > states1;
    IntervalVector f = postTest( sys.dynamics, W, sys.period, states1 );


    if( states1.size() != 0)
    {
        render(states1, horizont);
        cout << "Warning: There are not states, Richard " << endl;
    }
    */
    

    list<IntervalVector> list_W;
    list_W.push_back(W);

    ofstream file("solarwaterheatingpatterns.txt");

    while(!list_W.empty())
    {
        IntervalVector current_W = list_W.front();
        list_W.pop_front();
    
        if (current_W.diam().max() > 0.6)
        {
            LargestFirst bbb(0.1,0.5);

            std::pair<IntervalVector,IntervalVector> p = bbb.bisect(current_W);
            list_W.push_back(p.first);
            list_W.push_back(p.second);
            continue;
        }
                
        std::cout << "taille list_W : " << list_W.size() << std::endl;
        
        std::vector< std::pair<IntervalVector, std::vector<int> > > result;
        unsigned int k = NB_K;
        unsigned int d = NB_D;

        bool flag = decompose(sys, current_W, R, B, S, k, d, result);

        if (result.empty()) {
            std::cerr << "No solution with k = " << k << " and d = " << d << std::endl;
            file << current_W << " : no sol" << std::endl;
        }

        else{
            if (flag)
            {
                std::cerr << "Complete result -> PROOF" << std::endl;
            }
            else
            {
                std::cerr << "Incomplete result" << std::endl;
            }            
            // Display result
            std::vector< std::pair<IntervalVector, std::vector<int> > >::const_iterator it = result.begin();
            for (; it != result.end(); it++)
            {
                file << "zon = str2zon2(\"" ;
                file << it->first << "\"); \n if is_in_zonotope(X,zon) \t \n pattern = [";

                std::vector<int>::const_iterator it_pat = (it->second).begin();
                for (; it_pat != (it->second).end(); it_pat++) {
                file << *it_pat << " ";
                }
                file << "]; \n endif" << std::endl;
            }
        }        
    }

    
    file.close();

    /*
    plt::figure();
    double y;
    vector<double> sig;
    for (double i = 0; i < 10; i+=0.1)
    {
        y = 1/(1+pow(e,-10*(i-0.1*1)));
        sig.push_back(y);
    }
    plt::plot(sig ,"black");
    plt::grid(true);
    plt::show();

*/


    /*
    double horizont = 1.5*modes.size()*period;
    vector< IntervalVector > states;
    IntervalVector f = post(modes, W, period, states);


    if( states.size() != 0)
    {
        render(states, horizont);
        cout << "Warning: There are not states, Richard " << endl;
    }
    */
    

    return 0;
}



void render(vector< IntervalVector > states, double horizont)
{
    int n_states = states.size();
    vector< vector<Interval> > features(n_states);
    for (int i = 0; i < n_states; i++)
    {   
        //cout << states[i][0] << endl;
        features[0].push_back( states[i][0] );
        features[1].push_back( states[i][1] );
    }
    plotIntervalVector(features[0], "time", "Temperature", horizont, 70.0);    
    plotIntervalVector(features[1], "time", "Volume", horizont, 0.4);


    


    plt::figure();
    for (int i = 0; i < n_states; i++)
    {   
        //cout << states[i][0] << endl;
        //features[0].push_back( states[i][0] );
        plotBox(states[i], "red");
    }
    plt::grid(true);
    plt::show();
}


void plotIntervalVector(vector<Interval> feature, string x_name, string y_name, double xlimit, double ylimit)
{
    vector<double> feature_upper;
    vector<double> feature_lower;
    
    for(int i=0;i<feature.size();i++)
    {
        feature_upper.push_back( feature[i].ub() );
        feature_lower.push_back( feature[i].lb() );
    }
    
    plt::figure();
    plt::plot(feature_upper ,"black"); 
    plt::plot(feature_lower ,"red");  
    plt::xlim( 0.0, xlimit);
    plt::ylim( 0.0, ylimit);  
    plt::xlabel(x_name);
    plt::ylabel(y_name);
    plt::grid(true);
    //plt::show();

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


   
    /*
    for (double p = 1; p <= 3 ;p++) // piston
    {
        for(double r = 0; r <= 1; r++) // resistor
        {

     
            Function m = Function(x, Return( - 2.8811059759131854e-6*(x[0]-Te)/0.1*p
                                            //- 1/(1+pow(e,-100*(0.1*p-x[1])))*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)            //  original -> 0.00009346739
                                            - (1-x[1]/0.1*p)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
                                            + 0.7*0.7*8.403225763080125e-07*I/0.1*p       
                                            + r*0.008801843/(0.1*p)  
                                            ,0.5*( 0.1*p - x[1]) ) ); // 10s time to assent     
            //modes.push_back(m);


            sys.dynamics.push_back(m);
            
            //num++;
        }
        
    }
    sys.nb_dynamics = sys.dynamics.size();

    */


    // - 1/(1+pow(e,-10*(0.1*p-x[1])))*9.34673995175876e-05*(x[0]-Ti)/(0.1*p) 
