#define CATCH_CONFIG_MAIN
#include "catch.hpp"
// #include <json/json.h>
// using namespace Json;
// using namespace std;

TEST_CASE("sd","sd"){
  REQUIRE(1==1);
}

// std::vector<std::vector<double>> convert_from_json(const Json::Value &value)
// {
//     if (value.type() != Json::ValueType::arrayValue) {
//         throw config::InvalidValueException();
//     }
//     std::vector<std::vector<double>> result;
//     for (auto itr = value.begin(); itr != value.end(); itr++) {
//         std::vector<double> tmp;
//         for (auto i = (*itr).begin(); i != (*itr).end(); i++){
//            tmp.push_back(value[i.index()].asDouble());
//         }   
//         result.push_back(tmp);
//     }
//     return result;
// }


// std::vector<std::vector<double>> get(const std::string &key)
// {
//     if (!json.isMember(key)) {
//         throw "invalid";
//     }
//     if (json[key].type() != Json::ValueType::arrayValue) {
//         throw "invalid value";
//     }
//     return convert_from_json<std::vector<std::vector<double>>>(json[key]);
// }

// TEST_CASE("test 2d input", "[2djson]"){
  
//   if (value.type() != Json::ValueType::arrayValue) {
//       throw config::InvalidValueException();
//   }
//   std::vector<std::vector<double>> result;
//   for (auto itr = value.begin(); itr != value.end(); itr++) {
//       std::vector<double> tmp;
//       for (auto i = (*itr).begin(); i != (*itr).end(); i++){
//           tmp.push_back(value[i.index()].asDouble());
//       }   
//       result.push_back(tmp);
//   }
//   REQUIRE( 2 == 2 );
// }