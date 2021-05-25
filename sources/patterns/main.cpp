#include <ibex.h>
#include <string>
#include <vector>
#include <queue>
#include <cmath>
#include <json/json.h>
#include "common.h"
#include "jsonUtils.h"
#include "findPattern.h"
#include "decompose.h"
#include "config.h"
#include "model.h"

using namespace std;
using namespace ibex;
using namespace config;

void parseResultsToJson(vector<pair <IntervalVector, list<vector<int> > > > result){
    vector< pair<IntervalVector, list<vector<int> >  > >::const_iterator it = result.begin();
    for (; it != result.end(); it++){              
        event["zonotope"].append(jBox(it->first));              
        list< vector<int> >::const_iterator it_pat = (it->second).begin();
        Json::Value tmp;
        for (; it_pat != (it->second).end(); it_pat++) {
            tmp.append(jvec1D(*it_pat));
        }
        event["patterns"].append(tmp);            
    }
}

void decomposeBoxes(IntervalVector current_W){
    cout << "taille list_W : " << list_W.size() << endl;
    vector<pair <IntervalVector, list<vector<int> >   > > result;
    unsigned int k = NB_K, d = NB_D;
    bool flag = decompose(sys, current_W, R, B, S, k, d, result);
    if (result.empty()) {
        cerr << "No solution with k = " << k << " and d = " << d << endl;
        //file << current_W << " : no sol" << std::endl;
    }
    else{
        if (flag){
            cerr << "Complete result -> PROOF" << endl;
            result_total.push_back(result);
        }
        else
            cerr << "Incomplete result" << endl;
        // this part
        parseResultsToJson(result);
    }
}

// running from build directory
// make && ./bin/pattern_generator ../sources/patterns/parameters.json ../sources/patterns/pattern.json

int main(int argc, char* argv[]){
    readParameters(argv[1], argv[2]);
    setModel();
    
    // setFunction();
    list<IntervalVector> list_W;
    
    list_W.push_back(W);
    while(!list_W.empty()){
        IntervalVector current_W = list_W.front();
        list_W.pop_front();        
        if (current_W.diam().max() > 0.6){
            // cout << current_W << endl;
            LargestFirst bbb(0.1,0.5);
            pair<IntervalVector, IntervalVector> p = bbb.bisect(current_W);
            list_W.push_back(p.first);
            list_W.push_back(p.second);
            continue;
        }
        //decomposeBoxes(current_W); 

        cout << "taille list_W : " << list_W.size() << endl;
        vector<pair <IntervalVector, list<vector<int> >   > > result;
        unsigned int k = NB_K, d = NB_D;
        bool flag = decompose(sys, current_W, R, B, S, k, d, result);
        if (result.empty()) {
            cerr << "No solution with k = " << k << " and d = " << d << endl;
            //file << current_W << " : no sol" << std::endl;
        }
        else{
            if (flag){
                cerr << "Complete result -> PROOF" << endl;
                result_total.push_back(result);
            }
            else                
                cerr << "Incomplete result" << endl;   
            // this part
            parseResultsToJson(result);
        }
    }
    // //file << jsonWriter.write(event); 
    ofile << writeString(jsonWriter,event); // ?
    ofile.close();
    return 0;
}