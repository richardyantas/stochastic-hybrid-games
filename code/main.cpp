#include <ibex.h>
#include <string>
#include <vector>
#include <queue>
#include <cmath>

using namespace std;
// some variables to test the different algorithms
//#define POST 1
//#define FIND_PATTERN 1
#define DECOMPOSE 1
// Macro variables to set the values of the maximal length of a
// pattern (NB_K) and the maximal number of splittings of the
// state-space (NB_D)
// #define NB_K 3
// #define NB_D 20
using namespace ibex;
// Data type for sampled switched systems
typedef struct {
  double period;
  //std::vector<Function*> dynamics;
  std::vector<Function> dynamics;
  int nb_dynamics;
} sampledSwitchedSystem;

typedef struct {
  IntervalVector *Yinit;
  Affine2Vector *Ycurrent;
  std::vector<int> pattern;  
} node;


//find a pattern with new algo 
bool findPattern2 (const sampledSwitchedSystem& sys, const IntervalVector W,
		  const IntervalVector R, const IntervalVector B,
		  const IntervalVector S, unsigned int k,
		  std::list<std::vector<int> >& res_pattern_list) {

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
    //std::cout << "size of list : " << list_node.size() << std::endl;    
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
          std::cout << "forbidden pattern" << node_current.pattern << " + " << i << std::endl;
          continue;
        } 
      }
      //res_temp = false;
      if (node_current.pattern.empty())
	      std::cout << "current pattern : " << i << std::endl;
      else
      	std::cout << "current pattern : " << node_current.pattern << " + " << i << std::endl;           
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
        std::cout << "sol found !" << std::endl;
        node_current.pattern.push_back(i);        
        res_pattern_list.push_back(node_current.pattern);        
        res = true;
        //res_temp = true;                          
      }
      else
      {
        if (out_S)// || fin_B) //not only the last may be in obstacles...
        {
          std::cout << "Wrong direction !" << std::endl;
          //nop
        }
        else
        {
          
          if (stay_S)// && !cross_B)
          {
              //std::cout << "plop !" << std::endl;
            if (node_current.pattern.size() < k)
            {
              // In this part add  the filter
              std::cout << "Increment of pattern !" << std::endl;	      
              node new_node;
              new_node.Yinit = new IntervalVector(*node_current.Yinit);
              new_node.Ycurrent = new Affine2Vector(simu.get_last());     

              // i dont understand         
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
  return res;
}


// The main algorithm of minimator
bool decompose (const sampledSwitchedSystem& sys, const IntervalVector W,
		const IntervalVector R, const IntervalVector B,
		const IntervalVector S, unsigned int k, unsigned int d,
    std::vector<std::pair<IntervalVector, std::list<std::vector<int> >   > >& result) {
  // std::vector<int> res_pattern;
  std::list<std::vector<int> > res_pattern_list;
  // std::vector< std::pair<IntervalVector, std::vector<int> > > result;
  // std::list<std::vector<int> >& res_pattern_list
  // q is a queue of sub-state-space to explore to prove the invariance
  std::queue<IntervalVector> q;
  q.push (W);
  unsigned int nbStep = d;
  while (!q.empty() && nbStep > 0) {
    IntervalVector current = q.front ();
    q.pop();
    bool flag = findPattern2(sys, current, R, B, S, k, res_pattern_list);
    if (flag) {
      // Validated result, we keep it in the vector of results
      cout << "found it" << endl;
      result.push_back (std::pair< IntervalVector, std::list<std::vector<int> > > (current, res_pattern_list));
    }
    else {
      if (current.diam().max() > 0.5)
      {
        cout << "not found" << endl;
        LargestFirst bbb(0.1,0.5);
        std::pair<IntervalVector,IntervalVector> p = bbb.bisect(current);
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
    int NB_K = 3;
    int NB_D = 20;   //  NB_D = 20 , 5
    IntervalVector R(2);
    R[0] = Interval(40.0,70.0); // 70
    R[1] = Interval(0.1,0.3);   // 0.2
    IntervalVector W(2);
    W[0] = Interval(40.0,70.0); // 70 if you dont define is ENTIRE the second variable:
    W[1] = Interval(0.1,0.3);   // 0.2
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
      
    ofstream file("../patterns6.py");

    file << "\nR = [ ["   <<  R[1].lb()  << "," <<  R[1].ub() <<  "], [" <<  R[0].lb() <<  "," <<  R[0].ub() << "]] \n";
    file << "S = [ ["     <<  S[1].lb()  << "," <<  S[1].ub() <<  "], [" <<  S[0].lb() <<  "," <<  S[0].ub() << "]] \n";
    file << "tau = "      << sys.period << " # " << sys.period/60 << "min" <<"\n";
    file << "factorTe = " << factorTe << "\n";
    file << "factorI  = " << factorI << "\n";
    file << "factorKe = " << factorKe << "\n";
    file << "rate     = " << rate << "\n";
    file << "TwaterIn = " << TwaterIn << "\n\n";
    /*
    Interval Te(0.0,30.0);\n \
    Interval Ti(20.0,25.0);\n \
    Interval I(0.0,900.0);\n \ 
    */ 

    file << "def query(X): \n";

    
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

    /*
    const area_t zonotopes[128] = {
      {40.0,40.3125,0.09,0.31},
      {40.3125,40.625,0.09,0.31},
      {40.625,40.9375,0.09,0.31},
      {40.9375,41.25,0.09,0.31}
    }
    */
    
    std::vector< std::vector<std::pair <IntervalVector, std::list<std::vector<int> >   > > > result_total;

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
        std::vector<std::pair <IntervalVector, std::list<std::vector<int> >   > > result;
        //result.clear();
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
                result_total.push_back(result);
            }
            else
            {
                std::cerr << "Incomplete result" << std::endl;
            }                      
            std::vector< std::pair<IntervalVector,std::list<std::vector<int> >  > >::const_iterator it = result.begin();
            for (; it != result.end(); it++)
            {
                file << "\tif " << "(" << it->first[0].lb() << "<= X.T and X.T <= " << it->first[0].ub() << ") and (" << it->first[1].lb() << "<= X.V and X.V <= " << it->first[1].ub() << "):\n\t\treturn [";
                std::list< std::vector<int> >::const_iterator it_pat = (it->second).begin();
                for (; it_pat != (it->second).end(); it_pat++) {
                    std::vector<int>::const_iterator it_it_pat = it_pat->begin();
                    file << "[";
                    for(;it_it_pat != it_pat->end(); it_it_pat++)
                    {
                        file << *it_it_pat << ",";
                    }
                    file.seekp(-1, std::ios_base::end);
                    file << "], ";
                } 
                file.seekp(-2, std::ios_base::end);
                file << "]" << std::endl;
            }            
        }        
    }

    file << "\tprint(\"Not Found\") \n";
    file << "\treturn [[-1,-1,-1]]";

    int mx=0;
    
    file << "\n\n{";
    for(int i=0;i<result_total.size();i++)
    {
      for(int j=0;j<result_total[i].size();j++)
      {
        file << "{" << result_total[i][j].first[0].lb() << "," << result_total[i][j].first[0].ub() << "," << result_total[i][j].first[1].lb() << "," << result_total[i][j].first[1].ub() << "},\n";
      
        int y = result_total[i][j].second.size();
        mx = max( y , mx);
      }

    }
    file.seekp(-2, std::ios_base::end);
    file << "\n}\n";


    file << "\n\n{\n";
    for(int i=0;i<result_total.size();i++)
    {
      std::vector< std::pair<IntervalVector,std::list<std::vector<int> >  > >::const_iterator i3 = result_total[i].begin();
      file << "{";
      for (; i3 != result_total[i].end(); i3++)
      {   
          std::list< std::vector<int> >::const_iterator i4 = (i3->second).begin();
          int g = 0;
          for (; i4 != (i3->second).end(); i4++,g++)
          {
              std::vector<int>::const_iterator i5 = i4->begin();
              file << "{";
              int c=0;
              for(;i5 != i4->end(); i5++,c++) 
              {
                file << *i5 << ",";                   // Add -1 ,-2
              }
              for(int i=0;i<3-c;i++)
              {
                file << "-1" << ",";
              }
              file.seekp(-1, std::ios_base::end);
              file << "}, ";
          } 
          for(int i=0;i<mx-g;i++)
          {
            file << "{-2,-2,-2}, ";
          }
          //file.seekp(-2, std::ios_base::end);
          //file << "},\n";
      } 
      file.seekp(-2, std::ios_base::end);
      file << "},\n";                     
    }
    file.seekp(-1, std::ios_base::end);
    file << "}\n";
    

    file.close();
    return 0;
}