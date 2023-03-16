#include <ibex.h>
#include <string>
#include <vector>
#include <queue>
#include <cmath>
#include <json/json.h>
#include "Lswitched_system.h"
#include "Ldecompose.h"
#include "Lread_write_json.h"
using namespace std;
using namespace ibex;

// make && ./bin/generator ../stochastic_hybrid_game/datasets/static_data.json ../stochastic_hybrid_game/datasets/pattern2.json
// make && ./bin/generator ../sources/patterns/data/parameters.json ../sources/patterns/data/pattern2.json
// g++ -frounding-math -ffloat-store -I/usr/local/include -I/usr/local/include/ibex  -O3 -DNDEBUG -Wno-deprecated -frounding-math  pattern_generator.cpp -o pattern_generator -L/usr/local/lib -libex -lprim -lClp -lCoinUtils

int main(int argc, char* argv[]){

    sampledSwitchedSystem sys;
    Json::StreamWriterBuilder jsonWriter;    
    IntervalVector R(2), W(2), B(2), S(2);
    Interval Te, Ti, I;
    int NB_K, NB_D;
    double factorTe, factorI, factorTi, factorE, factorKe, rate, TwaterIn;
    readParameters(sys,  R, B, S, W, Te, Ti, I, NB_K, NB_D, factorTe, factorI, factorTi, factorE, factorKe, rate, TwaterIn, argv[1], argv[2]);
    int modes[8][3] = {{1,0,0}, {1,1,0}, {2,0,0}, {2,1,0}, {3,0,1}, {3,1,1}, {2,0,1}, {2,1,1}};
    int p,r,f;
    const int n = 2;
    Variable x(n);
    for(int i=0;i<8;i++){
        p = modes[i][0];r = modes[i][1];f = modes[i][2];
        Function mode = Function(x, Return( // TASKKKKKKKKKKKKKKKKKKKKKKK cambiar a Interval(0,5) para el nuevo set de perturbaciones 50 100 200, ademas agregar un tabla H 75 150 300, numero de perturbacion filas, columnas tiempos de asentamiento, ahorro energetico paara cada uno greedy y uppaal
            - factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p) - Interval(0,2)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
            - f*0.001005026*(0.1*p-x[1])*(x[0]-Ti)/(0.1*p)            //  original -> 0.00009346739
            + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p) + 1*factorE*r*0.008801843/(0.1*p) , rate*( 0.1*p - x[1]) ) 
        );
        sys.dynamics.push_back(mode);
    }             
    sys.nb_dynamics = sys.dynamics.size();

    list<IntervalVector> list_W;
    vector< vector<pair <IntervalVector, list<vector<int> >   > > > result_total;
    list_W.push_back(W);
    while(!list_W.empty()){
        IntervalVector current_W = list_W.front();
        list_W.pop_front();
        if (current_W.diam().max() > 0.6){
            cout <<current_W << endl;
            LargestFirst bbb(0.1,0.5);
            pair<IntervalVector,IntervalVector> p = bbb.bisect(current_W);
            list_W.push_back(p.first);
            list_W.push_back(p.second);
            continue;
        }
        cout << "taille list_W : " << list_W.size() << endl;
        vector<pair <IntervalVector, list<vector<int> >   > > result;
        unsigned int k = NB_K;
        unsigned int d = NB_D;
        bool flag = decompose(sys, current_W, R, B, S, k, d, result);
        if (result.empty()) {
            cerr << "No solution with k = " << k << " and d = " << d << endl;            
        }
        else{
            if (flag){
                cerr << "Complete result -> PROOF" << endl;
                result_total.push_back(result);
            }
            else                
                cerr << "Incomplete result" << endl;
            parse_to_json(result);
        }        
    }
    ofile << writeString(jsonWriter,event); // ?
    ofile.close();
    return 0;
}