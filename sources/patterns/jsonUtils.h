#pragma once
#include <json/json.h>

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
