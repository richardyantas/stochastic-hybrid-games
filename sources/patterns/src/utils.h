#pragma once
#include <json/json.h>
#include <ibex.h>
using namespace std;
using namespace ibex;
using namespace Json;

Json::Value event;   

template<class T>
Json::Value jvec1D(vector<T> in)
{
  Json::Value jvec;
  for (unsigned int i = 0; i < in.size(); i++)
  {
    jvec.append(in[i]);
  }
  return jvec;
}

template<class T>
Json::Value jvec2D(vector<vector<T>> in)
{
  Json::Value jvec;
  for (unsigned int i = 0; i < in.size(); i++)
  {
    jvec.append( jvec1D<T>(in[i]));
  }
  return jvec;
}

Json::Value jBox(IntervalVector box)
{
  Json::Value jvec;
  for(int i=0;i<box.size();i++)
  {
    jvec.append(jvec1D<float>(vector<float> {float(box[i].lb()), float(box[i].ub())}));
  }
  return jvec;
}


void parse_to_json(vector<pair <IntervalVector, list<vector<int> > > > result){
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


