#pragma once
#include <iostream>
#include <ibex.h>
#include <string>
#include <vector>
#include <queue>
#include <cmath>
#include <json/json.h>

using namespace std;
using namespace ibex;


typedef struct {
    double period;
    //std::vector<Function*> dynamics;
    std::vector<Function> dynamics;
    int nb_dynamics;
} sampledSwitchedSystem;


typedef struct {
    IntervalVector *Yinit;
    Affine2Vector *Ycurrent;
    std::vector<int> pattern;  
} node;