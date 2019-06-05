#pragma once
#include <queue>
#include <ibex/ibex.h>
#include <vector>
#include <cmath>
#include <cstring>
#include "LSwitchedSystem.h"
#include "LMatplotlibcpp.h"

using namespace ibex;
using namespace LSwitchedSystem;

namespace plt = matplotlibcpp;

namespace LUtils
{
 
    //void rectangles(vector<>)
    void plotBox(IntervalVector Box, string color) // bl, bu
    {

        double x1 = Box[0].lb();
        double y1 = Box[1].lb();

        double x2 = Box[0].ub();
        double y2 = Box[1].ub();

        // Prepare data.
        
        /*
        int n = 5000; // number of data points
        vector<double> x(n),y(n); 
        for(int i=0; i<n; ++i) {
            double t = 2*M_PI*i/n;
            x.at(i) = 16*sin(t)*sin(t)*sin(t);
            y.at(i) = 13*cos(t) - 5*cos(2*t) - 2*cos(3*t) - cos(4*t);
        }
        */

        int n = 5;
        vector<double> x(n), y(n); 
        // x1,x2

        x.at(0) = x1;
        y.at(0) = y1;
        x.at(1) = x1;
        y.at(1) = y2;
        x.at(2) = x2;
        y.at(2) = y2;
        x.at(3) = x2;
        y.at(3) = y1;
        x.at(4) = x1;
        y.at(4) = y1;

        // plot() takes an arbitrary number of (x,y,format)-triples. 
        // x must be iterable (that is, anything providing begin(x) and end(x)),
        // y must either be callable (providing operator() const) or iterable. 
        //plt::plot(x, y, "r-", x, [](double d) { return 12.5+abs( int(sin(d)) ) ; }, "k-");
       
        plt::plot(x, y, color);
        //plt::legend(label = 'okx');                
    }


    Interval sign(Interval x)
    {
        if(x.ub() >= 0.0 && x.lb() <= 0.0)return Interval(0.0,0.2);
        if(x.ub() < 0)return Interval(-1.2,-1.0);
        if(x.lb() > 0)return Interval(1.0,1.2);            
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

        double period = 50; // not works with 100

        IntervalVector x0(2);        
        x0[0] = Interval(23.0, 23.2);
        x0[1] = Interval(130.0, 130.2);

        
        Function m1 = Function(x, Return( ( 0.000030526755852842805*(x[0]-Te) + 0.000004777830864787386*I + 0.004777830864787387 ),one ) );
        Function m2 = Function(x, Return( ( 0.000030526755852842805*(x[0]-Te) + 0.000004777830864787386*I  ),one ) );
        Function m3 = Function(x, Return( ( 0.000030526755852842805*(x[0]-Te) + 0.000004777830864787386*I  ),one ) );

        Function m4 = Function(x, Return( ( 0.000030526755852842805*(x[0]-Te) + 0.000004777830864787386*I  ),one ) );
        Function m5 = Function(x, Return( ( 0.000030526755852842805*(x[0]-Te) + 0.000004777830864787386*I  ),one ) );
        Function m6 = Function(x, Return( ( 0.000030526755852842805*(x[0]-Te) + 0.000004777830864787386*I  ),one ) );


        
                   
        //Function m(x, Return( -x[1], x[0]));
        ivp_ode mode = ivp_ode( m1, 0.0, x0); // Is necessary to use simulation before
        simulation simu = simulation(&mode, period, HEUN, 1e-5);
        plotBox(x0,"black");
        simu.run_simulation();
        for(int i=1;i<period;i++)
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

        for(int i=1;i<period;i++)
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

     // Post operator
    IntervalVector post(const sampledSwitchedSystem& sys, const IntervalVector W, const std::vector<int> pattern)
    {
        Affine2Vector y0 = Affine2Vector(W);
        std::vector<int>::const_iterator it = pattern.begin();
        for (; it != pattern.end(); it++)
        {
            ivp_ode mode = ivp_ode(*(sys.dynamics[*it]), 0.0, y0);
            simulation simu = simulation(&mode, sys.period, HEUN, 1e-5);
            simu.run_simulation();
            y0=*(simu.list_solution_j.back().box_jnh_aff);
        }
        return y0.itv();
    }

    // A process to compute the successor of binary word of a given length 
    bool nextPattern(std::vector<int>& pattern)
    {
        for (int i=pattern.size()-1; i>=0; i--)
        {
            pattern[i] += 1;
            if ( pattern[i] > 15 )
            {
                pattern[i] = 0;
                continue;
            }
            return true;
        }
        return false;
    }

    // Unfolding verifies constraint crossing
    bool constraint(const sampledSwitchedSystem& sys, const IntervalVector W, const IntervalVector B, const IntervalVector S, const std::vector<int> pattern)
    {
        Affine2Vector y1 = Affine2Vector(W);

        std::vector<int>::const_iterator it = pattern.begin();
        for (; it != pattern.end(); it++) {
            ivp_ode mode = ivp_ode(*(sys.dynamics[*it]), 0.0, y1);
            simulation simu = simulation(&mode, sys.period, HEUN, 1e-5);
            simu.run_simulation();
            if (simu.has_crossed(B) ) {
                return false;
            }
            if (!simu.stayed_in(S)) {
                return false;
            }
        }
        return true;
    }

    // Depends on how the interval works.

    // Search for a pattern of maximal length k which can prove the
    // invariance
    bool findPattern (const sampledSwitchedSystem& sys, const IntervalVector W,const IntervalVector R, const IntervalVector B,const IntervalVector S, unsigned int k,
            std::vector<int>&  res_pattern)
    {
        std::cerr << "\tINIT = " << W << std::endl;
        for (unsigned int i = 1; i <= k; i++) {
            std::vector<int> pattern(i, 0);
            do{
                std::vector<int>::const_iterator it = pattern.begin();
                std::cerr << "\tPATTERN = (";
                for (; it != pattern.end(); it++){
                    std::cerr << *it << " ";
                }
                std::cerr << ")" << std::endl;
                IntervalVector res = post(sys, W, pattern);
                std::cerr << "Post(" << W << ") = " << res << " AND R = " << R << std::endl;
                if (res.is_subset(R) && constraint(sys,W,B,S,pattern)){
                    std::cerr << "\tPATTERN FOUND !!!" << std::endl;
                    res_pattern = pattern;
                    return true;
                }
            }while(nextPattern(pattern));
        }
        return false;
    }


    //find a pattern with new algo 
    bool findPattern2 (const sampledSwitchedSystem& sys, const IntervalVector W,
            const IntervalVector R, const IntervalVector B,
            const IntervalVector S, unsigned int k,
            std::vector<int>&  res_pattern)
    {

        LSwitchedSystem::node node_init;
        node_init.Yinit = new IntervalVector(W);
        node_init.Ycurrent = new Affine2Vector(W,true);
        node_init.pattern = std::vector<int>();
        
        std::list<LSwitchedSystem::node> list_node;
        std::list <std::pair <IntervalVector,std::vector<int> > > list_sol;
        
        list_node.push_back(node_init);
        
        int nb_pattern = sys.nb_dynamics;
        
        while(!list_node.empty())
        {   
            //std::cout << "size of list : " << list_node.size() << std::endl; 
            LSwitchedSystem::node node_current = list_node.front();
            list_node.pop_front();
            
            for (int i=0; i < nb_pattern; i++)
            {  
                if (node_current.pattern.empty())
                std::cout << "current pattern : " << i << std::endl;
                else
                std::cout << "current pattern : " << node_current.pattern << " + " << i << std::endl;
                
                ivp_ode mode = ivp_ode(*(sys.dynamics[i]), 0.0, *node_current.Ycurrent);
                simulation simu = simulation(&mode, sys.period, HEUN, 1e-5);
                simu.run_simulation();
                        
                bool fin_R = simu.finished_in(R);
                bool stay_S = simu.stayed_in(S);
                bool cross_B = simu.has_crossed(B);
                bool out_S = simu.go_out(S);
                bool fin_B = simu.finished_in(B);
                
                if (fin_R && stay_S && !cross_B)
                {
                    std::cout << "sol found !" << std::endl;
                    node_current.pattern.push_back(i);
                    
                    res_pattern = node_current.pattern;
                    
                    return true;
                }
                else 
                {
                    if (out_S || fin_B) //not only the last may be in obstacles...
                    {
                        std::cout << "Wrong direction !" << std::endl;
                        //nop
                    }
                    else 
                    {
                        if (stay_S && !cross_B)
                        {
                            if (node_current.pattern.size()+1 < k)
                            {
                                std::cout << "Increment of pattern !" << std::endl;	      

                                LSwitchedSystem::node new_node;
                                new_node.Yinit = new IntervalVector(*node_current.Yinit);
                                new_node.Ycurrent = new Affine2Vector(simu.get_last());
                                
                                std::vector<int> new_pattern (node_current.pattern);
                                new_pattern.push_back(i);
                                new_node.pattern = new_pattern;
                                list_node.push_back(new_node);	      
                            }
                        }
                    }
                }
            }
            
        }
        return false;
    }


    // The main algorithm of minimator
    bool decompose (const sampledSwitchedSystem& sys, const IntervalVector W,
            const IntervalVector R, const IntervalVector B,
            const IntervalVector S, unsigned int k, unsigned int d,
            std::vector<std::pair<IntervalVector, std::vector<int> > >& result)
    {
        std::vector<int> res_pattern;

        // q is a queue of sub-state-space to explore to prove the invariance
        std::queue< IntervalVector > q;
        q.push (W);

        unsigned int nbStep = d;

        while (!q.empty() && nbStep > 0)
        {
            IntervalVector current = q.front ();
            q.pop();
            bool flag = findPattern (sys, current, R, B, S, k, res_pattern);
            if (flag) {
            // Validated result, we keep it in the vector of results
            result.push_back (std::pair< IntervalVector, std::vector<int> > (current, res_pattern));
            }
            else {
            //if (current.diam().max() > 0.5)
            //{
            LargestFirst bbb(0.1,0.5);
            std::pair<IntervalVector,IntervalVector> p = bbb.bisect(current);
            q.push (p.first);
            q.push (p.second);
            nbStep--;
            //}
            }
        }

        if (nbStep <= 0) {
            return false;
        }
        else {
            return true;
        }
    }



      void draw()
    {
        std::vector<std::vector<double>> x, y, z;
        
        for (double i = -5; i <= 5;  i += 0.25) 
        {
            std::vector<double> x_row, y_row, z_row;
            for (double j = -5; j <= 5; j += 0.25) 
            {
                x_row.push_back(i);
                y_row.push_back(j);
                z_row.push_back(::std::sin(::std::hypot(i, j)));
            }
            x.push_back(x_row);
            y.push_back(y_row);
            z.push_back(z_row);
        }

        plt::plot_surface(x, y, z);
        plt::show();
        
    }


}