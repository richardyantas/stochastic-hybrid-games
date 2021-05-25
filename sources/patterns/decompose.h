#pragma once
#include "common.h"
#include "findPattern.h"

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
