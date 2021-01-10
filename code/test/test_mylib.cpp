#include<iostream>
#define CATCH_CONFIG_MAIN 
#include "catch.hpp"
#include "mylib.h"
using namespace std;

// double get_foo();

TEST_CASE("Testing get_foo method")
{
  cout << "valor de valores => " << get_foo() << endl;
  REQUIRE(get_foo() == 12.7);
}