#include <iostream>
#include <fstream>
#include "json/json.h"
using namespace std;

// ./test_json ../../test/data.json

int main(int argc, char* argv[])
{
  try{
    std::ofstream file_id;
    file_id.open("file.txt");

    Json::Value event;   

    Json::Value vec(Json::arrayValue);
    for (int i=0;i<10;i++){vec.append(Json::Value(i));}
  
    Json::Value vec2(Json::arrayValue);
    for (int i=0;i<2;i++){for (int j=0;j<2;j++){vec2.append(Json::Value(i));}}

    event["competitors"]["home"]["name"] = "Liverpool";
    //event["competitors"]["away"]["code"] = 89223;
    event["competitors"]["away"]["name"] = "Aston Villa";
    event["competitors"]["away"]["code"] = vec;
    //event["competitors"]["away"]["code2"] = [4,4,4];
    std::cout << event << std::endl;
    Json::StyledWriter styledWriter;
    file_id << styledWriter.write(event);
    file_id.close();
  }
  catch(std::exception& e){
    std::cout << "You need to2 add the path to json: ./test_json path_to_json" << std::endl;
  }
  return 0;
}