#pragma once

#include<ibex.h>
#include<iostream>
#include<vector>
using namespace std;
using namespace ibex;

// Data type for sampled switched systems
typedef struct {
  double period;
  std::vector< Function > dynamics;
  std::vector<IntervalVector> states;
  int nb_dynamics;

} sampledSwitchedSystem;

typedef struct {
  IntervalVector *Yinit;
  Affine2Vector *Ycurrent;
  std::vector<int> pattern;  
} node;

// Post operator
IntervalVector post(sampledSwitchedSystem& sys, const IntervalVector W,
		    const std::vector<int> pattern) {

  Affine2Vector y0 = Affine2Vector(W);
  std::vector<int>::const_iterator it = pattern.begin();
  for (; it != pattern.end(); it++) {
    ivp_ode mode = ivp_ode( (sys.dynamics[*it]), 0.0, y0);
    simulation simu = simulation(&mode, sys.period, HEUN, 1e-5);
    simu.run_simulation();
    y0=*(simu.list_solution_j.back().box_jnh_aff);
  }
  //sys.states.push_back( y0.itv() );
  return y0.itv();
}


bool nextPattern(const sampledSwitchedSystem& sys, std::vector<int>& pattern) {
  int numModes = sys.dynamics.size();

  for (int i = pattern.size() - 1; i >= 0; i-- )
  {
    pattern[i] += 1 ;
    if ( pattern[i] > (numModes-1) ) // 5 -> it depends of number of modes.
    { 
      pattern[i] = 0 ;
      continue ;
    } 
    return true ;
  }
  return false;
}


bool constraint(const sampledSwitchedSystem& sys, const IntervalVector W, const IntervalVector B,
		const IntervalVector S, const std::vector<int> pattern) {

  Affine2Vector y1 = Affine2Vector(W);

  std::vector<int>::const_iterator it = pattern.begin();
  for (; it != pattern.end(); it++) {
    ivp_ode mode = ivp_ode((sys.dynamics[*it]), 0.0, y1);
    simulation simu = simulation(&mode, sys.period, HEUN, 1e-5);
    simu.run_simulation();
    if (simu.has_crossed(B) ) {
      return false;
    }
    if (!simu.stayed_in(S)) {
      return false;
    }
  }
  return true;
}


bool isforbidden(const vector<int>& pattern)
{ 
  for(int i=0;i<pattern.size()-1;i++)
  {
    if( 
      (pattern[i] == 4) && (pattern[i+1] == 6 ) ||
      (pattern[i] == 0) && (pattern[i+1] == 2 ) ||
      (pattern[i] == 5) && (pattern[i+1] == 7 ) ||
      (pattern[i] == 1) && (pattern[i+1] == 3 ) ||
      (pattern[i] == 4) && (pattern[i+1] == 7 ) ||
      (pattern[i] == 5) && (pattern[i+1] == 6 ) ||
      (pattern[i] == 1) && (pattern[i+1] == 2 ) ||
      (pattern[i] == 0) && (pattern[i+1] == 3 ) 
    )
    return true;
  }

  return false;
}
// Search for a pattern of maximal length k which can prove the
// invariance
bool findPattern (sampledSwitchedSystem& sys, const IntervalVector W,
		  const IntervalVector R, const IntervalVector B,
		  const IntervalVector S, unsigned int k,
		  std::vector<int>&  res_pattern) {

  std::cerr << "\tINIT = " << W << std::endl;
  for (unsigned int i = 1; i <= k; i++) {
    std::vector<int> pattern(i, 0);

    do {  
      while( isforbidden(pattern))
      {
        nextPattern(sys, pattern);
      }      
      std::vector<int>::const_iterator it = pattern.begin();
      std::cerr << "\tPATTERN = (";
      for (; it != pattern.end(); it++)
      {
        std::cerr << *it << " " ;
      }
      std::cerr << ")" << std::endl;      
      IntervalVector res = post(sys, W, pattern);
      std::cerr << "Post(" << W << ") = " << res << " AND R = " << R << std::endl;
      if (res.is_subset(R) && constraint(sys,W,B,S,pattern)) {
          std::cerr << "\tPATTERN FOUND !!!" << std::endl;
          res_pattern = pattern;
          return true;
      }
    } while (nextPattern(sys,pattern));            
  }
  return false;
}




// The main algorithm of minimator
bool decompose (sampledSwitchedSystem& sys, const IntervalVector W,
		const IntervalVector R, const IntervalVector B,
		const IntervalVector S, unsigned int k, unsigned int d,
		std::vector<std::pair<IntervalVector, std::vector<int> > >& result) {
  std::vector<int> res_pattern;

  // q is a queue of sub-state-space to explore to prove the invariance
  std::queue<IntervalVector> q;
  q.push (W);

  unsigned int nbStep = d;

  while (!q.empty() && nbStep > 0) {
    IntervalVector current = q.front ();
    q.pop();
    bool flag = findPattern (sys, current, R, B, S, k, res_pattern);
    if (flag) {
      // Validated result, we keep it in the vector of results
      result.push_back (std::pair< IntervalVector, std::vector<int> > (current, res_pattern));
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


