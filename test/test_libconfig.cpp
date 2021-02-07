#include<iostream>
#include<functional>
#include<vector>
#define CATCH_CONFIG_MAIN 
#include "catch.hpp"
#include "config_wrapper.h"
using namespace std;

// BDD and TDD Development
// TEST_CASE( "Exported functions are computed",  )

TEST_CASE("Testing get_number_of_patterns method")
{
  REQUIRE(get_number_of_patterns() == 4);
}

TEST_CASE("Testing get_pattern method")
{
  //int8_t* my_array;
  int32_t* my_array;
  int32_t num_of_patterns = 5;
  //int *my_array;
  //int num_of_patterns = 5;
  cout << endl <<  "Filling the data" << endl;
  get_patterns(num_of_patterns, my_array); // get_patterns(num,my_array);
  cout << "total size: " << sizeof(my_array) <<endl;
  cout << "individual size: " << sizeof(my_array[0]) <<endl;
  int n = sizeof(my_array) / sizeof(my_array[0]);
  cout << "size: " << n;
  //std::vector<int> a(my_array,my_array+4);
  std::vector<int> b = {1,2,3,4,1};
  for (int i=0;i<5;i++)
  {
    REQUIRE(my_array[i] == b[i]);
  }
}

