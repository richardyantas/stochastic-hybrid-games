#include <ibex.h>
#include <string>
#include <vector>
#include <queue>
#include <cmath>
#include <json/json.h>
#include "switched_system.h"
#include "utils.h"
#include "decompose.h"
#include "read_json.h"

using namespace std;
using namespace ibex;

// make && ./bin/generator ../stochastic_hybrid_game/datasets/static_data.json ../stochastic_hybrid_game/datasets/pattern2.json
// make && ./bin/generator ../sources/patterns/data/parameters.json ../sources/patterns/data/pattern2.json

Json::StreamWriterBuilder jsonWriter;
//list<IntervalVector> list_W;
vector< vector< pair <IntervalVector, list< vector<int> > > > > result_total;
sampledSwitchedSystem sys;
IntervalVector R(2), W(2), B(2), S(2);
Interval Te, Ti, I;
int NB_K, NB_D;
double factorTe, factorI, factorTi, factorE, factorKe, rate, TwaterIn;

int main(int argc, char* argv[]){
    readParameters(sys,  R, B, S, W, Te, Ti, I, NB_K, NB_D, factorTe, factorI, factorTi, factorE, factorKe, rate, TwaterIn, argv[1], argv[2]);    
    //IntervalVector P(2);
    //P[0] = Interval(40.0,70.0); // 70
    //P[1] = Interval(0.1,0.2);   // 0.
    //cout << "P: "<< P << endl;
    cout << "R: " << R << endl;
    cout << "B: " << B << endl;
    cout << "S: " << S << endl;
    cout << "W: " << W << endl;
    cout << "Te: " << Te << endl;
    cout << "Ti: " << Ti << endl;
    cout << "I: " << I << endl;
    cout << "NB_K: " << NB_K << endl;
    cout << "NB_D: " << NB_D << endl;
    cout << "factorTe: " << factorTe << endl;
    cout << "factorTi: " << factorTe << endl;
    cout << "factorI: " << factorTe << endl;
    cout << "factorE: " << factorE << endl;
    cout << "factorKe: " << factorKe << endl;
    cout << "rate: " << rate << endl;
    cout << "TwaterIn: " << TwaterIn << endl;
    int modes[8][3] = {{1,0,0}, {1,1,0}, {2,0,0}, {2,1,0}, {3,0,1}, {3,1,1}, {2,0,1}, {2,1,1}};
    const int n = 2;
    Variable x(n);
    double p,r,f;

    // for(int i=0;i<8;i++){
    //     p = modes[i][0];r = modes[i][1];f = modes[i][2];
    //     Function mode = Function(x, Return( 
    //         - factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p) - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p) - f*0.001005026*(0.1*p-x[1])*(x[0]-Ti)/(0.1*p)            //  original -> 0.00009346739
    //         + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p) + factorE*r*0.008801843/(0.1*p) , rate*( 0.1*p - x[1]) ) 
    //     );
    //     sys.dynamics.push_back(mode);
    // }             
    // sys.nb_dynamics = sys.dynamics.size();

    list<IntervalVector> list_W;
    list_W.push_back(W);
    while(!list_W.empty()){
        IntervalVector current_W = list_W.front();
        list_W.pop_front();
        if (current_W.diam().max() > 0.6){
            cout << "current W: " << current_W << endl;
            LargestFirst bbb(0.1,0.5);
            pair<IntervalVector, IntervalVector> p = bbb.bisect(current_W);
            list_W.push_back(p.first);
            list_W.push_back(p.second);
            continue;
        }        
        cout << "taille list_W : " << list_W.size() << endl;
        vector<pair <IntervalVector, list<vector<int> >   > > result;
        unsigned int k = NB_K, d = NB_D;
        bool flag = decompose(sys, current_W, R, B, S, k, d, result);
        if (result.empty()) {
            cerr << "No solution with k = " << k << " and d = " << d << endl;            
            cout << current_W << ": no sol" << std::endl;
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

/*


    cout << NB_K << endl;
    cout << NB_D << endl;
    cout << R << endl;
    cout << W << endl;
    cout << B << endl;
    cout << S << endl;
    cout << Te << endl;
    cout << Ti << endl;
    cout << I << endl;
    cout << sys.period << endl;
    cout << factorTe << endl;
    cout << factorI << endl;
    cout <<  factorKe << endl;
    cout << factorE << endl;
    cout << rate << endl;
    cout << TwaterIn << endl;

*/