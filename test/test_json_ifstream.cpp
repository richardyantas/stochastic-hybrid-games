#include <iostream>
#include <fstream>
#include "json/json.h"
using namespace std;

// ./test_json ../../test/data.json

int main(int argc, char* argv[])
{
  try{
    Json::Value root;
    std::ifstream file(argv[1]);
    file >> root;
    std::cout << root << std::endl;
    std::cout << root["users"][0]["name"] << std::endl;
  }
  catch(std::exception& e){
    std::cout << "You need to add the path to json: ./test_json path_to_json" << std::endl;
  }
  return 0;
}