#include<iostream>
#include "ibex.h"
#include<json/json.h>
// ./setup.sh build
// ./build/bin/test_ibex_jso
using namespace std;
using namespace ibex;

int main()
{
  Interval x(0,1);
	Interval y=exp(x+1);   
  Json::Value event;   
  Json::Value vec(Json::arrayValue);
  for (int i=0;i<10;i++){vec.append(Json::Value(i));}
  Json::Value vec2(Json::arrayValue);
  for (int i=0;i<2;i++){vec2.append(vec);}
  event["competitors"]["home"]["name"] = "Liverpool";
  event["competitors"]["home"]["Ix"] = x.ub();
  event["competitors"]["away"]["name"] = "Aston Villa";
  event["competitors"]["away"]["code"] = vec2;
  std::cout << event << std::endl;
  std::cout << x << std::endl;
  return 0;
}
