#include <iostream>
#include <fstream>
#include "json/json.h"
using namespace std;

// make && ./bin/pattern_generator
// 
// ./test_json ../../test/data.json
// ./bin/test_json_ifstream ./bin/data.json

int main(int argc, char* argv[])
{
  cout << argv[1] << endl;
  try{ 
    
    //Json::Value root;
    string json = "",line;
    std::ifstream ifile(argv[1]);
    while(getline(ifile,line)){
      json += line;
    }
    cout << json << endl;   
    Json::CharReaderBuilder builder;
    Json::CharReader * reader = builder.newCharReader();
    Json::Value root;
    string errors;
    //string json = "{\"call\": \"KF6GPE\",\"type\":\"l\",\"time\":\"1399371514\",\"lasttime\":\"1418597513\",\"lat\": 37.17667,\"lng\": -122.14650,\"result\":\"ok\"}";
    //cout << json << endl;
    bool parseSuccess = reader->parse(json.c_str(),json.c_str()+json.size(), &root, &errors);

    if (parseSuccess)
    {
      const Json::Value resultValue = root["a"]["aa"][0];
      cout << "Result is " << resultValue.asString() << "\n";
    }
  }
  catch(std::exception& e){
    std::cout << "You need to add the path to json: ./test_json path_to_json" << std::endl;
  }
  return 0;
}