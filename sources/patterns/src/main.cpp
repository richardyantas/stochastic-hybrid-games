#include <ibex.h>
#include <string>
#include <vector>
#include <queue>
#include <cmath>
#include <json/json.h>
#include "common.h"
#include "utils.h"
#include "decompose.h"
#include "config.h"
#include "model.h"

using namespace std;
using namespace ibex;
using namespace config;

// running from build directory
// make && ./bin/pattern_generator ../sources/data/parameters.json ../sources/data/pattern.json
// task: 1: does not work the full code, 2:  we also need to check the interval in the model  "Interval(0,1)"*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
// strategies install on other computers and run 

int main(int argc, char* argv[]){
    readParameters(argv[1], argv[2]);
    cout <<"R: "<<R << endl;
    cout <<"W: "<<W << endl;
    cout <<"B: "<<B << endl;
    cout <<"S: "<<S << endl;
    cout <<"Te: "<< Te << endl;
    setModel();
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