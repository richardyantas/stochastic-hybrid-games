#pragma once

#include <queue>
#include <ibex/ibex.h>
#include <vector>
#include <cmath>
#include <cstring>
#include "GraphicsUtils.h"
#include "ProcessingUtils.h"
#include "Matplotlibcpp.h"

#define FIND_PATTERN 1 // Then comment again

#define DECOMPOSE 0


#define NB_K 3
#define NB_D 20


using namespace ibex;
using namespace GraphicsUtils;

void tube2( IntervalVector initialState ,Variable State, vector<Function *> mathModes, double period, double rate)
{

    for(int k=0;k<mathModes.size();k++)
    {
        ivp_ode  mode = ivp_ode(*(mathModes[k]), 0.0, initialState);
        simulation run = simulation(&mode, period, HEUN, 1e-5);

        run.run_simulation();
        plotBox(initialState, "black");
        for(int i=1;i<period;i+=rate)
        {
            cout << run.get_tight(i) << endl;
            plotBox( run.get_tight(i), "-r");                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
        }

        initialState = run.get_tight(period); 
    }

    plt::xlim( 0.0, 100.0);
    plt::ylim( 120.0, 200.0);  
    plt::xlabel("Temp");
    plt::ylabel("Vol");
    plt::grid(true);
    plt::show();
}



void tube( IntervalVector initialState ,Variable State, vector<Function> mathModes, double period, double rate)
{

    for(int k=0;k<mathModes.size();k++)
    {
        ivp_ode  mode = ivp_ode(mathModes[k], 0.0, initialState);
        simulation run = simulation(&mode, period, HEUN, 1e-5);

        run.run_simulation();
        plotBox(initialState, "black");
        for(int i=1;i<period;i+=rate)
        {
            cout << run.get_tight(i) << endl;
            plotBox( run.get_tight(i), "-r");                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
        }

        initialState = run.get_tight(period); 
    }

    plt::xlim( 20.0, 30.0);
    plt::ylim( 0.0, 5.0);  
    plt::xlabel("Temp");
    plt::ylabel("Vol");
    plt::grid(true);
    plt::show();
}



void solver()
{
    //IntervalVector x(2);
    Interval T(1.0,50.0);
    Interval V(1.0,10.1);
    Interval Te(0.0, 30.0);
    Interval I (1.0, 900.0);

    double n = 100000;
    double dt = 1/n;

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


void test()
{

    double period = 1;//114, 115
    Variable x(2);
    IntervalVector W(2);
    W[0]= Interval(1.0,50.0);
    W[1]= Interval(1.0,10.1);  // (20,22)
    //Function m6 = Function(x, Return( Interval(100.0,100.1) -  x[0] , Interval(1.0,1.1) ) );
    Function m6 = Function(x, Return( x[0]/x[1] , Interval(1.0,1.0) ) );
    Affine2Vector y0 = Affine2Vector(W);

    //cout << "W:" << W << endl;
    plotBox(W, "black");

    ivp_ode  mode = ivp_ode(m6, 0.0, y0); // cambios de y0 a W 
    simulation run = simulation(&mode, period, HEUN, 1e-5);
    run.run_simulation();
    y0=*(run.list_solution_j.back().box_jnh_aff);

    
    
    for(int i=1;i<period;i+=1)// 5 -> 1
    {
        //cout << run.get_tight(i) << endl;
        plotBox( run.get_tight(i), "-r");                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
    }
    

    cout << "***************************************** "<< endl;
    cout << "POST = " <<  y0.itv() << endl;
    plotBox(y0.itv(), "-r");

    plt::xlim( 0.0, 2000.0);
    plt::ylim( 0.0, 200.0);  
    plt::xlabel("Temp");
    plt::ylabel("Vol");
    plt::grid(true);
    plt::show();
}




void testModel()
{
    IntervalVector W(2);              // ensemble de depart
	//W[0]= Interval(50,55);  // (20,22)
	W[0]= Interval(20.0,50.1);
    W[1]= Interval(0.101,0.102);  // (20,22)

    const int n = 2;
	Variable x(n);
    Interval Te(0.0, 30.0);
    Interval I (1.0, 900.0);

    double period = 10; // CAMBIOS,  not works with 100
    //T = T - 2.8811059759131854e-06*(x[0]-Te)/x[1] + 8.403225763080125e-07*I/x[1], 0.001*(0.2-x[1])

    Function m6 = Function(x, Return( -2.8811059759131854e-06*(x[0]-Te)/x[1] + 
    8.403225763080125e-07*I ,0.001*( Interval(0.2,0.25) - x[1]) ) ); // 0.2 -> interval(0.2,0.25)
    // We found the problem x[0] - Te  -> x[0]

    Affine2Vector y0 = Affine2Vector(W);

    cout << "W:" << W << endl;
    plotBox(W, "black");

    ivp_ode  mode = ivp_ode(m6, 0.0, y0); // cambios de y0 a W
    simulation run = simulation(&mode, period, HEUN, 1e-6);
    run.run_simulation();
    y0=*(run.list_solution_j.back().box_jnh_aff);
    
    for(int i=1;i<period;i+=1)// 5 -> 1
    {
        //cout << run.get_tight(i) << endl;

        //cout << "EXP  = " << (run.get_tight(i)[0] - Te) << "--" << run.get_tight(i)[1] << endl;
        //cout << -2.8811059759131854e-06*(run.get_tight(i)[0] - Te)/run.get_tight(i)[1] << endl;
        //cout << 8.403225763080125e-07*I/run.get_tight(i)[1] << endl;
        //cout <<  -2.8811059759131854e-06*(run.get_tight(i)[0] - Te)/run.get_tight(i)[1] + 8.403225763080125e-07*I/run.get_tight(i)[1] << endl;
        //cout << 0.001*( Interval(0.2,0.25) - run.get_tight(i)[1]) << endl;
        plotBox( run.get_tight(i), "-r");                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
    }
    

    cout << "POST = " <<  y0.itv() << endl;
    plotBox(y0.itv(), "-r");


    //cout << "EXPERIMENT = " << Interval(-50,-50.1)/Interval(5,5.1) << endl; // EMPTY
    //cout << "EXPERIMENT = " << Interval(-50,50.1)/Interval(-5,5.1) << endl;  // ENTIRE
    //cout << "EXPERIMENT = " << Interval(-50,50.1)-Interval(-5,5.1) << endl;  // ENTIRE

    plt::xlim( 0.0, 40.0);
    plt::ylim( 0.0, 3.0);  
    plt::xlabel("Temp");
    plt::ylabel("Vol");
    plt::grid(true);
    plt::show();

}



void SolarWaterHeating()
{

    IntervalVector W(2);              // ensemble de depart
	//W[0]= Interval(50,55);  // (20,22)
	W[0]= Interval(23.0,23.7);
    W[1]= Interval(0.11,0.12);  // (20,22)

    const int n = 2;
	Variable x(n);
    Interval Te(0.0, 40.0);
    Interval I (0.0, 900.0);

    double period = 4*15*60; // CAMBIOS,  not works with 100

    //IntervalVector x0(2);        
    //x0[0] = Interval(23.0, 23.2);
    //x0[1] = Interval(1.0, 1.13);   // Initial Volumen

    Function m1 = Function(x, Return( -2.8811059759131854e-06*(x[0]-Te)/x[1] + 8.403225763080125e-07*I/x[1] + 0.00048018432931886426/x[1], 0.001*(0.1-x[1]) ) );
    Function m2 = Function(x, Return( -2.8811059759131854e-06*(x[0]-Te)/x[1] + 8.403225763080125e-07*I/x[1] + 0.00048018432931886426/x[1], 0.001*(0.2-x[1]) ) );
	Function m3 = Function(x, Return( -2.8811059759131854e-06*(x[0]-Te)/x[1] + 8.403225763080125e-07*I/x[1] + 0.00048018432931886426/x[1], 0.001*(0.3-x[1]) ) );
	Function m4 = Function(x, Return( -2.8811059759131854e-06*(x[0]-Te)/x[1] + 8.403225763080125e-07*I/x[1], 0.001*(0.1-x[1]) ) );
	Function m5 = Function(x, Return( -2.8811059759131854e-06*(x[0]-Te)/x[1] + 8.403225763080125e-07*I/x[1], 0.001*(0.2-x[1]) ) );
	
    
    
    //Function m6 = Function(x, Return( -2.8811059759131854e-06*(x[0]-Te)/x[1].mid() + 
    //8.403225763080125e-07*I/ (x[1].mid()), 0.001*(0.2-x[1]) ) );
    
    //Function m6 = Function(x, Return( -0.0000028811059759131854*(x[0]-Te)/x[1] + 
    //0.0000008403225763080125*I/x[1], 0.001*(0.1-x[1]) ) );
    
    //Function m6 = Function(x, Return( -1*(x[0]-Interval(30.0,31.0))/x[1] + 
    //Interval(0.0,7.0)/x[1], (1-x[1]) ) );


    Interval out1;
    Interval out2;

    div2(-(Interval(2,2.1)-Interval(1,1.1)), Interval(5,5.2) ,out1,out2 );
    //div2(Interval(-2,-2.1), Interval(5,5.2) ,out1,out2 );

    cout << "intervals result: " << out1 << "-" << out2 << endl;



    Interval r = -(Interval(2,2.1)-Interval(1,1.1)) / Interval(5,5.2);

    cout << "r: " << r << endl;

    Function m6 = Function(x, Return( (x[0]+Interval(1,1.1))/x[1] , Interval(1,1.1) ) );


    vector<Function> mathModes;

    //mathModes.push_back(m1);
	
    //mathModes.push_back(m2);
    //mathModes.push_back(m3);
    //mathModes.push_back(m4);
    //mathModes.push_back(m5);
    mathModes.push_back(m6);
    
    
    //cout << "hi " << endl;

    cout << "W:" << W << endl;

    Affine2Vector y0 = Affine2Vector(W);

    //IntervalVector initialState = x0;

    //plotBox(W, "black");

    for(int k=0;k<mathModes.size();k++)
    {
        ivp_ode  mode = ivp_ode(mathModes[k], 0.0, W); // cambios de y0 a W
        simulation run = simulation(&mode, period, HEUN, 1e-9);
        run.run_simulation();
        y0=*(run.list_solution_j.back().box_jnh_aff);
        /*s
        for(int i=1;i<period;i+=5)
        {
            cout << run.get_tight(i) << endl;
            plotBox( run.get_tight(i), "-r");                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
        }
        */
        //initialState = run.get_tight(period); 
    }

    cout << "POST = " <<  y0.itv() << endl;

    //plotBox(y0.itv(), "-r");

    plt::xlim( 0.0, 100.0);
    plt::ylim( 0.0, 1.0);  
    plt::xlabel("Temp");
    plt::ylabel("Vol");
    plt::grid(true);
    plt::show();



    //tube(x0,x,mathmodes,period,5);            
}


void findPatternsForSolarWaterHeating()
{
    

    const int n = 2;
	Variable x(n);
    //IntervalVector W(2);
    //W[0] = Interval(40,100);
    //W[1] = Interval(0,300);

    //Interval Ti(20, 40); // It include valve mode = OFF and ON
    Interval Te(0.0, 40.0);
    Interval I (0.0, 900.0);

    //double period = 15*60; // not works with 100

    IntervalVector x0(2);        
    x0[0] = Interval(23.0, 23.2);
    x0[1] = Interval(1.0, 1.13);   // Initial Volumen


    Function m1 = Function(x, Return( -2.8811059759131854e-06*(x[0]-Te)/x[1] + 8.403225763080125e-07*I/x[1] + 0.00048018432931886426/x[1], 0.001*(0.1-x[1]) ) );
	/*
    Function m2 = Function(x, Return( -2.8811059759131854e-06*(x[0]-Te)/x[1] + 8.403225763080125e-07*I/x[1] + 0.00048018432931886426/x[1], 0.001*(0.2-x[1]) ) );
	Function m3 = Function(x, Return( -2.8811059759131854e-06*(x[0]-Te)/x[1] + 8.403225763080125e-07*I/x[1] + 0.00048018432931886426/x[1], 0.001*(0.3-x[1]) ) );
	Function m4 = Function(x, Return( -2.8811059759131854e-06*(x[0]-Te)/x[1] + 8.403225763080125e-07*I/x[1], 0.001*(0.1-x[1]) ) );
	Function m5 = Function(x, Return( -2.8811059759131854e-06*(x[0]-Te)/x[1] + 8.403225763080125e-07*I/x[1], 0.001*(0.2-x[1]) ) );
	Function m6 = Function(x, Return( -2.8811059759131854e-06*(x[0]-Te)/x[1] + 8.403225763080125e-07*I/x[1], 0.001*(0.3-x[1]) ) );
	*/

	sampledSwitchedSystem sys;

	sys.period = 60*15;
	
    sys.dynamics.push_back(&m1);

    /*
	sys.dynamics.push_back(&m2);
    sys.dynamics.push_back(&m3);
    sys.dynamics.push_back(&m4);
    sys.dynamics.push_back(&m5);
    sys.dynamics.push_back(&m6);
    */

    sys.nb_dynamics = 6;

    
    //tube2(x0,x,sys.dynamics,sys.period,5);  
    //plt::xlim(0, 10*10);


    IntervalVector R(2);           // Objectif
	R[0] = Interval(40,80); // (20,22)
	R[1] = Interval(0.1,0.3); // (20,22) 

    IntervalVector W(2);              // ensemble de depart
	W[0]= Interval(50,60);  // (20,22)
	W[1]= Interval(0.2,0.25);  // (20,22)
	//W[2]= Interval(20,22);
	//W[3]= Interval(20,22);

	IntervalVector B(2);               // zone interdite
	B[0] = Interval(0.0,10.0); //0.0,1.0
	B[1] = Interval(0.0,0.1); // 0.0,1.0
	//B[2] = Interval(0.0,1.0);
	//B[3] = Interval(0.0,1.0);

	IntervalVector S(2);
	S[0] = Interval(0,100);
	S[1] = Interval(0.0,0.4);
	//S[2] = Interval(19,23);
	//S[3] = Interval(19,23);



	std::list<IntervalVector> list_W;
	list_W.push_back(W);

	//file for solutions
	std::ofstream file("./result_solar_water_heating.txt", std::ios::out | std::ios::trunc);

	while (!list_W.empty())
	{
		IntervalVector current_W = list_W.front();
		list_W.pop_front();

		if (current_W.diam().max() > 0.6)
		{
			LargestFirst bbb(0.1, 0.5);
			std::pair<IntervalVector, IntervalVector> p = bbb.bisect(current_W);
			list_W.push_back(p.first);
			list_W.push_back(p.second);
			continue;
		}

		std::cout << "taille list_W : " << list_W.size() << std::endl;

		std::vector<std::pair<IntervalVector, std::vector<int> > > result;
		unsigned int k = NB_K;
		unsigned int d = NB_D;

		bool flag = decompose(sys, current_W, R, B, S, k, d, result);

		if (result.empty())
		{
			std::cerr << "No solution with k = " << k << " and d = " << d << std::endl;
			file << current_W << " : no sol" << std::endl;
		}
		else
		{
			if (flag)
			{
				std::cerr << "Complete result -> PROOF" << std::endl;
			}
			else
			{
				std::cerr << "Incomplete result" << std::endl;
			}

			// Display result
			std::vector<std::pair<IntervalVector, std::vector<int> > >::const_iterator it = result.begin();
			for (; it != result.end(); it++)
			{
				file << "zon = str2zon2(\"";
				file << it->first << "\"); \n if is_in_zonotope(X,zon) \t \n pattern = [";

				std::vector<int>::const_iterator it_pat = (it->second).begin();
				for (; it_pat != (it->second).end(); it_pat++)
				{
					file << *it_pat << " ";
				}
				file << "]; \n endif" << std::endl;
			}
		}

	}
	file.close();

}



void SWH()
{

    Variable x(2); // x[0] = T, x[1] = V
    IntervalVector W(2);
    W[0] = Interval(40, 100);
    W[1] = Interval( 0, 300);

    Interval Ti(20, 40); // It include valve mode = OFF and ON
    Interval Te(25, 45);
    Interval I(5, 3000);

    Interval one(0.1,0.11);

    double period = 20; // not works with 100

    IntervalVector x0(2);        
    x0[0] = Interval(23.0, 23.2);
    x0[1] = Interval(130.0, 130.2);


    Function m1 = Function(x, Return( ( 0.000030526755852842805*(x[0]-Te) + 
        0.000004777830864787386*I + 0.004777830864787387 ),one ) );
    
    Function m2 = Function(x, Return( ( 0.000030526755852842805*(x[0]-Te) + 
        0.000004777830864787386*I  ),one ) );
    /*
    Function m3 = Function(x, Return( ( 0.000030526755852842805*(x[0]-Te) + 0.000004777830864787386*I  ),one ) );

    Function m4 = Function(x, Return( ( 0.000030526755852842805*(x[0]-Te) + 0.000004777830864787386*I  ),one ) );
    Function m5 = Function(x, Return( ( 0.000030526755852842805*(x[0]-Te) + 0.000004777830864787386*I  ),one ) );
    Function m6 = Function(x, Return( ( 0.000030526755852842805*(x[0]-Te) + 0.000004777830864787386*I  ),one ) );
    */
                        
    //Function m(x, Return( -x[1], x[0]));
    ivp_ode mode = ivp_ode( m1, 0.0, x0); // Is necessary to use simulation before
    simulation simu = simulation(&mode, period, HEUN, 1e-5);
    plotBox(x0,"black");
    simu.run_simulation();
    for(int i=1;i<period;i+=5)
    {
        cout << simu.get_tight(i) << endl;
        plotBox( simu.get_tight(i), "-r");                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
    } 
    plotBox( simu.get_tight(period), "purple");


    //Affine2Vector ddd = *(simu.list_solution_j.back().box_jnh_aff) ;        
    x0 = simu.get_tight(period);
    //return y0.itv();

    ivp_ode mode2 = ivp_ode( m2, 0.0, x0); // Is necessary to use simulation before
    simulation simu2 = simulation(&mode2, period, HEUN, 1e-5);
    plotBox(x0,"black");
    
    simu2.run_simulation();

    for(int i=1;i<period;i+=5)
    {
        cout << simu2.get_tight(i) << endl;
        plotBox( simu2.get_tight(i), "-r");                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
    } 
    plotBox( simu2.get_tight(period), "purple");

    
    plt::xlim( 0.0, 100.0);
    plt::ylim( 120.0, 150.0);
    //plt::legend();  
    plt::xlabel("T");
    plt::ylabel("V");
    plt::grid(true);
    plt::show();

}


void foo()
    {
        Variable x(2);   
        IntervalVector W(2); // ensemble de depart
        W[0] = Interval(10, 12);
        W[1] = Interval(10, 12);

        Interval k(0.1, 0.1);

        //Function m = Function(T, (T-Ti)*0.1 + (T-Te)*0.4 + I*0.21);        
        //Function m1( x, Return( -x[1]+3, 2*x[0] ) );
        // 1. Function m1( x, Return( -   x[1], k ) );

        // kx = 1.3

        double kc = 3.2;
        double cc = 1.2;
        double m  = 10;

        //Interval dx1 = k- x[1];
        //Interval dx2 = k;

        int period = 100;

        //Affine2Vector x0 = Affine2Vector(W);
        IntervalVector x0(2);
        
        x0[0] = Interval(2,2.2);
        x0[1] = Interval(4,4.2);

        //Function m1( x, Return( k- x[1], k ) );
        Function m1( x, Return( x[1],  -kc/m*x[0]- cc/m*x[1]) );
    
        //NumConstraint csp1(x, sqr(x[0])+sqr(x[1])-1.0 = 0);
        //Array<NumConstraint> csp(csp1);
        ivp_ode mode = ivp_ode( m1, 0, x0);  // If the code is run only, it doesnt work!.
        //ivp_ode mode = ivp_ode( m1, 0.0, x0, csp1);
        
        simulation simu = simulation(&mode, period, HEUN, 1e-5);
        simu.run_simulation();

        plotBox(W, "blue");
        plotBox(x0,"black");

        for(int i=1;i<99;i++)
        {
            cout << simu.get_tight(i) << endl;
            plotBox( simu.get_tight(i), "-r");
        }


        plotBox( simu.get_tight(100), "purple");


        IntervalVector R(2);
        R[0] = Interval(-2.5,2.5);
        R[1] = Interval(-5,5);
        plotBox(R,"green");

        plt::xlim( -20.0, 20.0);
        plt::ylim(-6.0, 6.0);
        //plt::legend();  
        plt::xlabel("x1");
        plt::ylabel("x2");
        plt::grid(true);
        plt::show();
    }
