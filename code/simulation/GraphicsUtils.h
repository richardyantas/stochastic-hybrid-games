#pragma once

#include <queue>
#include <ibex/ibex.h>
#include <vector>
#include <cmath>
#include <cstring>

#include "Matplotlibcpp.h"

using namespace ibex;

namespace plt = matplotlibcpp;

namespace GraphicsUtils
{

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
    Interval sign(Interval x)
    {
        if(x.ub() >= 0.0 && x.lb() <= 0.0)return Interval(0.0,0.2);
        if(x.ub() < 0)return Interval(-1.2,-1.0);
        if(x.lb() > 0)return Interval(1.0,1.2);            
    }
    */




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