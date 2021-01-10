#include <iostream>
#include <fstream>
#include "mylib.h"
#include "../lib/jsoncpp/include/json/json.h"
using namespace std;
Json::Value js;

void read_json()
{
  ifstream file("/home/serendipita/Documents/uppaalLibrary/config/static_json.json");
  file >> js;
  // js["get_foo"] = 12.7;
}

// template <typename T>
//     T get(const std::string &key);

// template <>
// double get<double>(const std::string &key)
// {
//   read_json();
//   return js[key].asDouble();
// }

// #define S_CONFIG_GETTER(type, key)                                           \
//    type key() { return get<type>(#key);}

// S_CONFIG_GETTER(double, get_foo);

double get_foo()
{
  read_json();
  return js["get_foo"].asDouble();
}


