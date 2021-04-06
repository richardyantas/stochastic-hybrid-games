//#include <ibex.h>
#include <iostream>
#include <json/json.h>
#include <fstream>
using namespace std;
//using namespace ibex;

// template<class T>
// Json::Value jvec1D(vector<T> in)
// {
//   Json::Value jvec;
//   for (int i = 0; i < in.size(); i++)
//   {
//     jvec.append(in[i]);
//   }
//   return jvec;
// }

// template<class T>
// Json::Value jvec2D(vector<vector<T>> in)
// {
//   Json::Value jvec;
//   for (int i = 0; i < in.size(); i++)
//   {
//     jvec.append( jvec1D<T>(in[i]));
//   }
//   return jvec;
// }

// Json::Value jBox(IntervalVector box)
// {
//   Json::Value jvec;
//   for(int i=0;i<box.size();i++)
//   {
//     jvec.append(jvec1D<float>(vector<float> {float(box[i].lb()), float(box[i].ub())}));
//   }
//   return jvec;
// }

 int main()
 {
//   Interval x(0, 1);
//   Interval y = exp(x + 1);
//   IntervalVector R(2);
//   R[0] = Interval(40.0,70.0); // 70
//   R[1] = Interval(0.1,0.2);   // 0.2

//   ofstream file;
//   file.open("jsonTestIbex.json");
//   Json::StyledWriter styledWriter;
//   // Json::Value R = jvec2D(vector<vector<int>>{{1, 2}, {1, 1}});
//   Json::Value event;
//   //Json::Value jR = jBox(R);
//   event["competitors"]["home"]["name"] = "Liverpool";
//   event["competitors"]["home"]["Ix"] = x.ub();
//   event["competitors"]["away"]["name"] = "Aston Villa";
//   //event["competitors"]["away"]["R"] = jR;
//   event["competitors"]["away"]["R"] = jBox(R);
//   event["competitors"]["away"]["listX"] = jBox(R);
//   event["competitors"]["away"]["listX"].append(jBox(R));
//   event["competitors"]["away"]["listX"].append(jBox(R));
//   file << styledWriter.write(event);
//   //std::cout << event << std::endl;
//   //std::cout << x << std::endl;
   return 0;
 }
