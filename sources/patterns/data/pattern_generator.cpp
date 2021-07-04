#include <ibex.h>
#include <string>
#include <vector>
#include <queue>
#include <cmath>
<<<<<<< HEAD:sources/patterns/data/pattern_generator.cpp
//#include <json/json.h>
//#include "jsonUtils.h"
=======
#include <json/json.h>
#include "jsonUtils.h"
>>>>>>> 41e7d3da9e19f511ef6e75f5618eab835fc102c7:sources/patterns/data/pattern_generator.cpp
using namespace std;
using namespace ibex;
// Macro variables to set the values of the maximal length of a
// pattern (NB_K) and the maximal number of splittings of the
// state-space (NB_D)
// #define NB_K 3
// #define NB_D 20

<<<<<<< HEAD:sources/patterns/data/pattern_generator.cpp
// g++ -frounding-math -ffloat-store -I/usr/local/include -I/usr/local/include/ibex  -O3 -DNDEBUG -Wno-deprecated -frounding-math  pattern_generator.cpp -o pattern_generator -L/usr/local/lib -libex -lprim -lClp -lCoinUtils
=======
>>>>>>> 41e7d3da9e19f511ef6e75f5618eab835fc102c7:sources/patterns/data/pattern_generator.cpp
typedef struct {
  double period;
  //vector<Function*> dynamics;
  vector<Function> dynamics;
  int nb_dynamics;
} sampledSwitchedSystem;

typedef struct {
  IntervalVector *Yinit;
  Affine2Vector *Ycurrent;
  vector<int> pattern;  
} node;

//find a pattern with new algo 
bool findPattern2 (const sampledSwitchedSystem& sys, const IntervalVector W,
		  const IntervalVector R, const IntervalVector B,
		  const IntervalVector S, unsigned int k,
		  list<vector<int> >& res_pattern_list) {

  node node_init;
  node_init.Yinit = new IntervalVector(W);
  node_init.Ycurrent = new Affine2Vector(W,true);
  node_init.pattern = vector<int>();
  list<node> list_node;
  list<pair <IntervalVector,vector<int> > > list_sol;
  list_node.push_back(node_init);
  //int nb_pattern = NB_M;
  int nb_pattern = sys.nb_dynamics;
  bool res = false;
  //bool res_temp = false;
  while(!list_node.empty())
  {    
    //cout << "size of list : " << list_node.size() << endl;    
    node node_current = list_node.front();
    list_node.pop_front();     
    for (int i=0; i < nb_pattern && node_current.pattern.size() < k; i++)
    {   
      if( node_current.pattern.size() > 0 )
      {
        int l = node_current.pattern.back();
        if( (l == 4  && i == 6) || //
            (l == 0  && i == 2) || //
            (l == 5  && i == 7) || //
            (l == 1  && i == 3) || //
            (l == 4  && i == 7) || //
            (l == 5  && i == 6) || //
            (l == 1  && i == 2) || //          
            (l == 0  && i == 3)    //
        )
        {
          cout << "forbidden pattern" << node_current.pattern << " + " << i << endl;
          continue;
        } 
      }
      //res_temp = false;
      if (node_current.pattern.empty())
	      cout << "current pattern : " << i << endl;
      else
      	cout << "current pattern : " << node_current.pattern << " + " << i << endl;           
      //ivp_ode mode = ivp_ode(*(sys.dynamics[i]), 0.0, *node_current.Ycurrent);
      ivp_ode mode = ivp_ode( (sys.dynamics[i]), 0.0, *node_current.Ycurrent);
      simulation simu = simulation(&mode, sys.period, HEUN, 1e-5);
      simu.run_simulation();
      bool fin_R = simu.finished_in(R);
      bool stay_S = simu.stayed_in(S);
      bool cross_B = simu.has_crossed(B);
      bool out_S = simu.go_out(S);
      bool fin_B = simu.finished_in(B);
      
      if (fin_R && stay_S)// && !cross_B)
      {       
        cout << "sol found !" << endl;
        node_current.pattern.push_back(i);        
        res_pattern_list.push_back(node_current.pattern);        
        res = true;
        //res_temp = true;                          
      }
      else
      {
        if (out_S)// || fin_B) //not only the last may be in obstacles...
        {
          cout << "Wrong direction !" << endl;
          //nop
        }
        else
        {
          
          if (stay_S)// && !cross_B)
          {
            if (node_current.pattern.size() < k)
            {
              // In this part add  the filter
              cout << "Increment of pattern !" << endl;	      
              node new_node;
              new_node.Yinit = new IntervalVector(*node_current.Yinit);
              new_node.Ycurrent = new Affine2Vector(simu.get_last());     

              // i dont understand         
              vector<int> new_pattern (node_current.pattern);
              new_pattern.push_back(i);
              new_node.pattern = new_pattern;
              list_node.push_back(new_node);	                                             
            }
          }
        }
      }
    }
    
  }
  return res;
}

// The main algorithm of minimator
bool decompose (const sampledSwitchedSystem& sys, const IntervalVector W,
		const IntervalVector R, const IntervalVector B,
		const IntervalVector S, unsigned int k, unsigned int d,
    vector<pair<IntervalVector, list<vector<int> >   > >& result) { 
  list<vector<int> > res_pattern_list;  
  queue<IntervalVector> q;
  q.push (W);
  unsigned int nbStep = d;
  while (!q.empty() && nbStep > 0) {
    IntervalVector current = q.front ();
    q.pop();
    bool flag = findPattern2(sys, current, R, B, S, k, res_pattern_list);
    if (flag) {
      // Validated result, we keep it in the vector of results
      cout << "found it" << endl;
      result.push_back (pair< IntervalVector, list<vector<int> > > (current, res_pattern_list));
    }
    else {
      if (current.diam().max() > 0.5)
      {
        cout << "not found" << endl;
        LargestFirst bbb(0.1,0.5);
        pair<IntervalVector,IntervalVector> p = bbb.bisect(current);
        q.push (p.first);
        q.push (p.second);
        nbStep--;
      }
    }
  }

  if (nbStep <= 0) {
    return false;
  }
  else {
    return true;
  }
}

int main()
{
    sampledSwitchedSystem sys;
    sys.period = 5*60; // critical // CAMBIOS,  not works with 100
    // DynIbex Simulation
    int NB_K = 3; // IMPORTANT BACK TO 3 VALUE  CURRENT VALUE TO TEST
    int NB_D = 20;   //  NB_D = 20 , 5 IMPORTANT BACK TO 20 VALUE  CURRENT VALUE TO TEST
    IntervalVector R(2);
    R[0] = Interval(40.0,70.0); // 70
    R[1] = Interval(0.1,0.2);   // 0.2
    IntervalVector W(2);
    W[0] = Interval(40.0,70.0); // 70 if you dont define is ENTIRE the second variable:
    W[1] = Interval(0.1,0.2);   // 0.2
    IntervalVector B(2);
    B[0] = Interval(0.0,0.0);
    B[1] = Interval(0.0,0.0);
    IntervalVector S(2);
    S[0] = Interval(30.0,80.0);
    S[1] = Interval(0.09,0.31);

    Interval Te(0.0,16.5);  // According to Data
    Interval Ti(20.0,25.0);
    Interval I(0.0,920.0); // 910

    double factorTe = 2.5;
    double factorI  = 0.8; 
    double factorE  = 1.0;
    double factorKe = 1.0;
    double rate     = 0.01; // 0.5
    double TwaterIn = (Ti.ub()+Ti.lb())/2;//22.5; 
  
    ofstream file("./patterns_test.json");
<<<<<<< HEAD:sources/patterns/data/pattern_generator.cpp
    // Json::StyledWriter styledWriter;
    // Json::Value event;   

    // event["R"] = jBox(R);
    // event["S"] = jBox(S);
    // event["tau"] = sys.period;
    // event["factorTe"] = factorTe;
    // event["factorI"] = factorI;
    // event["factorKe"] = factorKe;
    // event["rate"] = rate;
    // event["TwaterIn"] = TwaterIn;
=======
    Json::StyledWriter styledWriter;
    Json::Value event;   

    event["R"] = jBox(R);
    event["S"] = jBox(S);
    event["tau"] = sys.period;
    event["factorTe"] = factorTe;
    event["factorI"] = factorI;
    event["factorKe"] = factorKe;
    event["rate"] = rate;
    event["TwaterIn"] = TwaterIn;
>>>>>>> 41e7d3da9e19f511ef6e75f5618eab835fc102c7:sources/patterns/data/pattern_generator.cpp
    
    const int n = 2;
	  Variable x(n);

    double p,r; 
    p = 1, r = 0; 
    Function m0 = Function(x, Return( -factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
                                            + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
                                            + factorE*r*0.008801843/(0.1*p)  
                                            ,rate*( 0.1*p - x[1]) ) ); // 10s time to assent
    p = 1, r = 1; 
    Function m1 = Function(x, Return( -factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)                                            
                                            + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
                                            + factorE*r*0.008801843/(0.1*p)  
                                            ,rate*( 0.1*p - x[1]) ) ); // 10s time to assent
    p = 2, r = 0; 
    Function m2 = Function(x, Return( -factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
                                            + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
                                            + factorE*r*0.008801843/(0.1*p)  
                                            ,rate*( 0.1*p - x[1]) ) ); // 10s time to assent
    p = 2, r = 1; 
    Function m3 = Function(x, Return( -factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)                                        
                                            + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
                                            + factorE*r*0.008801843/(0.1*p)  
                                            ,rate*( 0.1*p - x[1]) ) ); // 10s time to assent
    p = 3, r = 0; 
    Function m4 = Function(x, Return( -factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
                                            - 0.001005026*(0.1*p-x[1])*(x[0]-Ti)/(0.1*p)            //  original -> 0.00009346739
                                            + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
                                            + factorE*r*0.008801843/(0.1*p)  
                                            ,rate*( 0.1*p - x[1]) ) ); // 10s time to assent
    p = 3, r = 1; 
    Function m5 = Function(x, Return( -factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
                                            - 0.001005026*(0.1*p-x[1])*(x[0]-Ti)/(0.1*p)            //  original -> 0.00009346739
                                            + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
                                            + factorE*r*0.008801843/(0.1*p)  
                                            ,rate*( 0.1*p - x[1]) ) ); // 10s time to assent
    p = 2, r = 0; 
    Function m6 = Function(x, Return( -factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
                                            - 0.001005026*(0.1*p-x[1])*(x[0]-Ti)/(0.1*p)            //  original -> 0.00009346739
                                            + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p)
                                            + factorE*r*0.008801843/(0.1*p)  
                                            ,rate*( 0.1*p - x[1]) ) ); // 10s time to assent
    p = 2, r = 1;     
    Function m7 = Function(x, Return( -factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
                                            - 0.001005026*(0.1*p-x[1])*(x[0]-Ti)/(0.1*p)           //  original -> 0.00009346739
                                            + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
                                            + factorE*r*0.008801843/(0.1*p)  
                                            ,rate*( 0.1*p - x[1]) ) ); // 10s time to assent

    sys.dynamics.push_back(m0);
    sys.dynamics.push_back(m1);    
    sys.dynamics.push_back(m2);
    sys.dynamics.push_back(m3);
    sys.dynamics.push_back(m4);
    sys.dynamics.push_back(m5);
    sys.dynamics.push_back(m6);
    sys.dynamics.push_back(m7);
    
    sys.nb_dynamics = sys.dynamics.size();
    list<IntervalVector> list_W;
    list_W.push_back(W);
    
    vector< vector<pair <IntervalVector, list<vector<int> >   > > > result_total;

    while(!list_W.empty())
    {
        IntervalVector current_W = list_W.front();
        list_W.pop_front();
        if (current_W.diam().max() > 0.6)  // IMPORTANT BACK FROM 10 to 6
        //if (current_W.diam().max() > 10.0)
        {
            cout << ":)" <<current_W << endl;
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
            //file << current_W << " : no sol" << endl;
        }
        else{
            if (flag)
            {
                cerr << "Complete result -> PROOF" << endl;
                result_total.push_back(result);
            }
            else
            {
                cerr << "Incomplete result" << endl;
            }                      
            vector< pair<IntervalVector,list<vector<int> >  > >::const_iterator it = result.begin();
<<<<<<< HEAD:sources/patterns/data/pattern_generator.cpp
            // for (; it != result.end(); it++)
            // {              
            //     event["zonotope"].append(jBox(it->first));              
            //     list< vector<int> >::const_iterator it_pat = (it->second).begin();
            //     Json::Value tmp;
            //     for (; it_pat != (it->second).end(); it_pat++) {
            //         tmp.append(jvec1D(*it_pat));
            //     }
            //     event["patterns"].append(tmp);            
            // }            
        }        
    }
    // file << styledWriter.write(event);
    // file.close();
=======
            for (; it != result.end(); it++)
            {              
                event["zonotope"].append(jBox(it->first));              
                list< vector<int> >::const_iterator it_pat = (it->second).begin();
                Json::Value tmp;
                for (; it_pat != (it->second).end(); it_pat++) {
                    tmp.append(jvec1D(*it_pat));
                }
                event["patterns"].append(tmp);            
            }            
        }        
    }
    file << styledWriter.write(event);
    file.close();
>>>>>>> 41e7d3da9e19f511ef6e75f5618eab835fc102c7:sources/patterns/data/pattern_generator.cpp
    return 0;
}