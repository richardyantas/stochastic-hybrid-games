#define CATCH_CONFIG_MAIN  // This tells Catch to provide a main() - only do this in one cpp file
#include "catch.hpp"

#include <ibex.h>
#include <vector>
#include <queue>
#include <iostream>
#include <sstream>
#include <cmath>

#include "../read.h"
#include "../system.h"
#include "../safeTools.h"

using namespace ibex;
#define e 2.718281828
#define NB_K 3
#define NB_D 20



using namespace std;

unsigned int Factorial( unsigned int number ) {
    return number <= 1 ? number : Factorial(number-1)*number;
}





TEST_CASE( "dynbex is computed", "[ode]")
{
    IntervalVector R(2);
    R[0] = Interval(40.0,41.0);
    R[1] = Interval(0.08,0.32);

    IntervalVector W(2);
    W[0] = Interval(40.0,40.1);  // if you dont define is ENTIRE the second variable:
    W[1] = Interval(0.2,0.21);

    IntervalVector B(2);
    B[0] = Interval(0.0,0.0);
    B[1] = Interval(0.0,0.0);

    IntervalVector S(2);
    S[0] = Interval(0.0, 70.0);
    S[1] = Interval(0.0, 0.4);

    const int n = 2;
	Variable x(n);
    Interval Te(0.0, 30.0);
    Interval Ti(0.0,25.0);
    Interval I(0.0, 900.0);

    //int period = 1*60; // CAMBIOS,  not works with 100

    // -9.34673995175876e-05(x[0]-Ti)/x[1]   ->   (Ti,v = 0,1) -> [Tmin - 0], max added temperature  zero


    //int v = 0,1;
    vector<Function> modes;
    //Function m;

    
    sampledSwitchedSystem sys;
    sys.period = 25;//1*60;
    sys.states.push_back(W);    
    sys.nb_dynamics = 2;
    
    vector<int> pattern;
    
    IntervalVector p = post(sys,W,pattern);


    
}


TEST_CASE( "Factorials are computed", "[factorial]" ) {
    REQUIRE( Factorial(1) == 1 );
    REQUIRE( Factorial(2) == 2 );
    REQUIRE( Factorial(3) == 6 );
    REQUIRE( Factorial(10) == 3628800 );
}

TEST_CASE( "vectors can be sized and resized", "[vector]" ) {

    std::vector<int> v( 5 );

    REQUIRE( v.size() == 4 );
    REQUIRE( v.capacity() >= 5 );

    SECTION( "resizing bigger changes size and capacity" ) {
        v.resize( 10 );

        REQUIRE( v.size() == 10 );
        REQUIRE( v.capacity() >= 10 );
    }
    SECTION( "resizing smaller changes size but not capacity" ) {
        v.resize( 0 );

        REQUIRE( v.size() == 0 );
        REQUIRE( v.capacity() >= 5 );
    }
    SECTION( "reserving bigger changes capacity but not size" ) {
        v.reserve( 10 );

        REQUIRE( v.size() == 5 );
        REQUIRE( v.capacity() >= 10 );
    }
    SECTION( "reserving smaller does not change size or capacity" ) {
        v.reserve( 0 );

        REQUIRE( v.size() == 5 );
        REQUIRE( v.capacity() >= 5 );
    }

     SECTION( "reserving bigger changes capacity but not size" ) {
        v.reserve( 10 );

        REQUIRE( v.size() == 5 );
        REQUIRE( v.capacity() >= 10 );

        SECTION( "reserving smaller again does not change capacity" ) {
            v.reserve( 7 );

            REQUIRE( v.capacity() >= 10 );
        }
    }


}