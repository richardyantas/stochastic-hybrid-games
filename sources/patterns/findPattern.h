#pragma once
#include "common.h"

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
  int nb_pattern = sys.nb_dynamics;   // number of ODE's 
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
      //cout << "dev " << endl;
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
      //bool cross_B = simu.has_crossed(B);
      bool out_S = simu.go_out(S);
      //bool fin_B = simu.finished_in(B);
      
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