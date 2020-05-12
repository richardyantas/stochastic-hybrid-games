#include <ibex.h>
#include <string>
#include <vector>
#include <queue>

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
    int NB_D = 20;
    IntervalVector R(2);
    R[0] = Interval(40.0,70.0);
    R[1] = Interval(0.1,0.3);
    IntervalVector W(2);
    W[0] = Interval(40.0,70.0); // if you dont define is ENTIRE the second variable:
    W[1] = Interval(0.1,0.3);
    IntervalVector B(2);
    B[0] = Interval(0.0,0.0);
    B[1] = Interval(0.0,0.0);
    IntervalVector S(2);
    S[0] = Interval(30.0,80.0);
    S[1] = Interval(0.09,0.31);
    Interval Te(0.0,30.0);
    Interval Ti(20.0,25.0);
    Interval I(0.0,900.0);
    double factorI  = 0.05; 
    double factorTe = 5.5; 
    double factorE  = 1.0;
    double rate     = 0.01; // 0.5
    
    const int n = 2;
	  Variable x(n);

    double p,r; 
    p = 1, r = 0; 
    Function m1 = Function(x, Return( -factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p)                                        
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
                                            + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
                                            + factorE*r*0.008801843/(0.1*p)  
                                            ,rate*( 0.1*p - x[1]) ) ); // 10s time to assent
    p = 1, r = 1; 
    Function m2 = Function(x, Return( -factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)                                            
                                            + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
                                            + factorE*r*0.008801843/(0.1*p)  
                                            ,rate*( 0.1*p - x[1]) ) ); // 10s time to assent
    p = 2, r = 0; 
    Function m3 = Function(x, Return( -factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
                                            + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
                                            + factorE*r*0.008801843/(0.1*p)  
                                            ,rate*( 0.1*p - x[1]) ) ); // 10s time to assent
    p = 2, r = 1; 
    Function m4 = Function(x, Return( -factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)                                        
                                            + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
                                            + factorE*r*0.008801843/(0.1*p)  
                                            ,rate*( 0.1*p - x[1]) ) ); // 10s time to assent
    p = 3, r = 0; 
    Function m5 = Function(x, Return( -factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
                                            - 0.001005026*(0.1*p-x[1])*(x[0]-Ti)/(0.1*p)            //  original -> 0.00009346739
                                            + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
                                            + factorE*r*0.008801843/(0.1*p)  
                                            ,rate*( 0.1*p - x[1]) ) ); // 10s time to assent
    p = 3, r = 1; 
    Function m6 = Function(x, Return( -factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
                                            - 0.001005026*(0.1*p-x[1])*(x[0]-Ti)/(0.1*p)            //  original -> 0.00009346739
                                            + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
                                            + factorE*r*0.008801843/(0.1*p)  
                                            ,rate*( 0.1*p - x[1]) ) ); // 10s time to assent
    p = 2, r = 0; 
    Function m7 = Function(x, Return( -factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
                                            - 0.001005026*(0.1*p-x[1])*(x[0]-Ti)/(0.1*p)            //  original -> 0.00009346739
                                            + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p)
                                            + factorE*r*0.008801843/(0.1*p)  
                                            ,rate*( 0.1*p - x[1]) ) ); // 10s time to assent
    p = 2, r = 1;     
    Function m8 = Function(x, Return( -factorTe*2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
                                            - 0.001005026*(0.1*p-x[1])*(x[0]-Ti)/(0.1*p)           //  original -> 0.00009346739
                                            + factorI*0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
                                            + factorE*r*0.008801843/(0.1*p)  
                                            ,rate*( 0.1*p - x[1]) ) ); // 10s time to assent

    sys.dynamics.push_back(m1);
    sys.dynamics.push_back(m2);
    sys.dynamics.push_back(m3);
    sys.dynamics.push_back(m4);
    sys.dynamics.push_back(m5);
    sys.dynamics.push_back(m6);
    sys.dynamics.push_back(m7);
    sys.dynamics.push_back(m8);

    sys.nb_dynamics = sys.dynamics.size();
    list<IntervalVector> list_W;
    list_W.push_back(W);
    ofstream file("../patterns3.py");
    file << "def query(X): \n";

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
        //std::vector< std::pair<IntervalVector, std::vector<int> > > result;
        std::vector<std::pair <IntervalVector, std::list<std::vector<int> >   > > result;
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
    file.close();

    return 0;
}