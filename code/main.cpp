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
		//std::vector<std::pair<IntervalVector, std::vector<int> > >& result) {
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
      //result.push_back (std::pair< IntervalVector, std::vector<int> > (current, res_pattern));
      result.push_back (std::pair< IntervalVector, std::list<std::vector<int> > > (current, res_pattern_list));
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



int main()
{
   // DynIbex Simulation
    int NB_K = 3;
    int NB_D = 20;
    IntervalVector R(2);
    R[0] = Interval(40.0,80.0);
    R[1] = Interval(0.09,0.31);
    IntervalVector W(2);
    //W[0] = Interval(40.0,40.1);  // if you dont define is ENTIRE the second variable:
    //W[1] = Interval(0.2,0.21);
    //W[0] = Interval(40.0,45.1);
    //W[1] = Interval(0.09,0.31);
    W[0] = Interval(44.0,44.1);
    W[1] = Interval(0.1,0.11);
    IntervalVector B(2);
    B[0] = Interval(0.0,0.0);
    B[1] = Interval(0.0,0.0);
    IntervalVector S(2);
    S[0] = Interval(20.0, 100.0);
    S[1] = Interval(0.05, 0.4);

    const int n = 2;
	Variable x(n);
    Interval Te(0.0, 30.0);
    Interval Ti(20.0,25.0);
    Interval I(0.0, 900.0);
    //int period = 1*60; // CAMBIOS,  not works with 100
    // -9.34673995175876e-05(x[0]-Ti)/x[1]   ->   (Ti,v = 0,1) -> [Tmin - 0], max added temperature  zero
    sampledSwitchedSystem sys;
    //sys.period = 15*60;
    sys.period = 5*60; // critical 
    //sys.period = 10*60;
    //sys.period = 25;
    //sys.period = 3*60;
    //sys.period = 2*60;
    
    //sys.states.push_back(W);    

    double p,r;   
    p = 1, r = 0; 
    Function m1 = Function(x, Return( - 2.8811059759131854e-6*(x[0]-Te)/(0.1*p)                                        
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
                                            + 0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
                                            + r*0.008801843/(0.1*p)  
                                            ,0.5*( 0.1*p - x[1]) ) ); // 10s time to assent
    p = 1, r = 1; 
    Function m2 = Function(x, Return( - 2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)                                            
                                            + 0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
                                            + r*0.008801843/(0.1*p)  
                                            ,0.5*( 0.1*p - x[1]) ) ); // 10s time to assent
    p = 2, r = 0; 
    Function m3 = Function(x, Return( - 2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
                                            + 0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
                                            + r*0.008801843/(0.1*p)  
                                            ,0.5*( 0.1*p - x[1]) ) ); // 10s time to assent

    cout << "m3: " << m3 << endl;
    p = 2, r = 1; 
    Function m4 = Function(x, Return( - 2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)                                        
                                            + 0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
                                            + r*0.008801843/(0.1*p)  
                                            ,0.5*( 0.1*p - x[1]) ) ); // 10s time to assent
    p = 3, r = 0; 
    Function m5 = Function(x, Return( - 2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
                                            - 0.001005026*(0.1*p-x[1])*(x[0]-Ti)/(0.1*p)            //  original -> 0.00009346739
                                            + 0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
                                            + r*0.008801843/(0.1*p)  
                                            ,0.5*( 0.1*p - x[1]) ) ); // 10s time to assent
    p = 3, r = 1; 
    Function m6 = Function(x, Return( - 2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
                                            - 0.001005026*(0.1*p-x[1])*(x[0]-Ti)/(0.1*p)            //  original -> 0.00009346739
                                            + 0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
                                            + r*0.008801843/(0.1*p)  
                                            ,0.5*( 0.1*p - x[1]) ) ); // 10s time to assent

    p = 2, r = 0; 
    Function m7 = Function(x, Return( - 2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
                                            - 0.001005026*(0.1*p-x[1])*(x[0]-Ti)/(0.1*p)            //  original -> 0.00009346739
                                            + 0.7*0.7*8.403225763080125e-07*I/(0.1*p)
                                            + r*0.008801843/(0.1*p)  
                                            ,0.5*( 0.1*p - x[1]) ) ); // 10s time to assent
    p = 2, r = 1;     
    Function m8 = Function(x, Return( - 2.8811059759131854e-6*(x[0]-Te)/(0.1*p)
                                            - Interval(0,1)*9.34673995175876e-05*(x[0]-Ti)/(0.1*p)
                                            - 0.001005026*(0.1*p-x[1])*(x[0]-Ti)/(0.1*p)           //  original -> 0.00009346739
                                            + 0.7*0.7*8.403225763080125e-07*I/(0.1*p)       
                                            + r*0.008801843/(0.1*p)  
                                            ,0.5*( 0.1*p - x[1]) ) ); // 10s time to assent

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
    ofstream file("../patterns.py");
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


/*
int main(){

  const int n= 4;
  Variable y(n);

  Interval heat_s(0.0,1.0);
  Interval V1(3.5);
  Interval V2(3);
  Interval V3(3);
  Interval V4(3.5);
  Interval Tu(17.0);
  Interval To(27.0,30.0);
  Interval Tc(27.0,30.0);

  // 0 0 0 0
  Function m01 = Function (y, Return ((2.85*0.0001)*(y[1] - y[0]) + (2.47*0.0001)*(y[3] - y[0])
				      + (7.36*0.00001)*(Tu - y[0]) + (5.78*0.0001)*(To - y[0])
				      + (9.27*0.00001)*(Tc - y[0])
				      + (heat_s*(3.12*0.00000000000000001))*(((3.73*1000)*(3.73*1000))*((3.73*1000)*(3.73*1000)) - y[0]*(y[0]*(y[0]*y[0]))),
				      (7.60*0.00001)*(y[0] - y[1]) + (1.89*0.0001)*(y[2] - y[1])
				      + (7.02*0.00001)*(Tu - y[1]) + (6.21*0.0001)*(To - y[1])
				      + (2.42*0.0001)*(Tc - y[1])
				      + (heat_s*(2.55*0.0000000000000001))*(((1.78*1000)*(1.78*1000))*((1.78*1000)*(1.78*1000)) - (y[1]*y[1])*(y[1]*y[1])),
				     1.79*(0.0001*(y[1] - y[2])) + 3.81*(0.0001*(y[3] - y[2]))
				      + (3.45*0.00001)*(Tu - y[2]) + (5.64*0.0001)*(To - y[2])
				      + (3.21*0.00000001)*(Tc - y[2])
				      + (heat_s*(8.57*0.0000000000001))*(((3.82*100)*(3.82*100))*((3.82*100)*(3.82*100)) - (y[2]*y[2])*(y[2]*y[2])),
				      1.09*(0.0001*(y[0] - y[3])) + 1.07*(0.0001*(y[2] - y[3]))
				      + (3.26*0.00001)*(Tu - y[3]) + (5.99*0.0001)*(To - y[3])
				      + (1.73*0.0001)*(Tc - y[3])
				      + (heat_s*(3.57*0.00000000000000001))*(((3.93*1000)*(3.93*1000))*((3.93*1000)*(3.93*1000)) - (y[3]*y[3])*(y[3]*y[3]))));
  
  sampledSwitchedSystem sys;

  sys.period = 25; 
  sys.dynamics.push_back(&m01);
  sys.dynamics.push_back(&m02);
  sys.dynamics.push_back(&m03);
  sys.dynamics.push_back(&m04);
  sys.dynamics.push_back(&m05);
  sys.dynamics.push_back(&m06);
  sys.dynamics.push_back(&m07);
  sys.dynamics.push_back(&m08);
  sys.dynamics.push_back(&m09);
  sys.dynamics.push_back(&m10);
  sys.dynamics.push_back(&m11);
  sys.dynamics.push_back(&m12);
  sys.dynamics.push_back(&m13);
  sys.dynamics.push_back(&m14);
  sys.dynamics.push_back(&m15);
  sys.dynamics.push_back(&m16);

  sys.nb_dynamics = 16;

   IntervalVector R(4);           // Objectif
  R[0] = Interval(20,22);
  R[1] = Interval(20,22);
  R[2] = Interval(20,22);
  R[3] = Interval(20,22);


#ifdef FIND_PATTERN
  IntervalVector current = v3;

  std::vector<int> res_pattern;
  unsigned int k = NB_K;
  bool flag = findPattern (sys, current, R, B, k, res_pattern);
  if (flag) {
    std::cerr << "pattern found = (";
    std::vector<int>::const_iterator it = res_pattern.begin();
    for (; it != res_pattern.end(); it++) {
      std::cerr << *it << " ";
    }
    std::cerr << ") for " << current << std::endl;
  }
  else {
    std::cerr << "No pattern found for " << current << std::endl;
  }
#endif

#ifdef DECOMPOSE

  IntervalVector W(4);              // ensemble de depart
   W[0]= Interval(20,22);
   W[1]= Interval(20,22);
   W[2]= Interval(20,22);
   W[3]= Interval(20,22);

   IntervalVector B(4);               // zone interdite
  B[0] = Interval(0.0,1.0);
  B[1] = Interval(0.0,1.0);
  B[2] = Interval(0.0,1.0);
  B[3] = Interval(0.0,1.0);

  IntervalVector S(4);
  S[0] = Interval(19,23);
  S[1] = Interval(19,23);
  S[2] = Interval(19,23);
  S[3] = Interval(19,23);
  

  
  std::list<IntervalVector> list_W;
  list_W.push_back(W);
  
  //file for solutions
  std::ofstream file("./result_4_rooms.txt", std::ios::out | std::ios::trunc);

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
	
	std::vector< std::pair<IntervalVector, std::vector<int> > > result;
	unsigned int k = NB_K;
	unsigned int d = NB_D;

	bool flag = decompose(sys, current_W, R, B, S, k, d, result);

	if (result.empty()) {
	  std::cerr << "No solution with k = " << k << " and d = " << d << std::endl;
	  file << current_W << " : no sol" << std::endl;
	}
	else {
	  if (flag) {
	    std::cerr << "Complete result -> PROOF" << std::endl;
	  }
	  else {
	    std::cerr << "Incomplete result" << std::endl;
	  }
	  
	  // Display result
	  std::vector< std::pair<IntervalVector, std::vector<int> > >::const_iterator it = result.begin();
	  for (; it != result.end(); it++) {
	    file << "zon = str2zon2(\"" ;
	    file << it->first << "\"); \n if is_in_zonotope(X,zon) \t \n pattern = [";

	    std::vector<int>::const_iterator it_pat = (it->second).begin();
	    for (; it_pat != (it->second).end(); it_pat++) {
	      file << *it_pat << " ";
	    }
	    file << "]; \n endif" << std::endl;
	  }
	}
  }
  file.close();

#endif
   return 0;
  
}
*/