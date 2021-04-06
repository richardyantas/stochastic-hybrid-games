#pragma once
#include "common.h"

namespace config
{
    sampledSwitchedSystem sys;
    IntervalVector R(2), W(2), B(2), S(2);
    Interval Te, Ti, I;
    int NB_K, NB_D;
    double factorTe, factorI, factorTi, factorE, factorKe, rate, TwaterIn;
    ofstream ofile;
    ifstream ifile;
    Json::CharReaderBuilder reader;
    Json::Value obj;    
    Json::String errors;
    // read the parameter json here
    void readParameters(){
        // https://jsoncpp.docsforge.com/master/home/#code-example
        // https://open-source-parsers.github.io/jsoncpp-docs/doxygen/class_json_1_1_char_reader_builder.html
        ifile = ifstream("./parameters.json");
        bool ok =  parseFromStream(reader, ifile, &obj, &errors);
        //cout << "ok: " << ok << endl;
        ofile = ofstream("./pattern2.json");
        
        //sys.period = 5*60;
        //NB_K = 3;
        //NB_D = 20;
        R[0] = Interval(40.0, 70.0);
        R[1] = Interval(0.1, 0.2); 
        //cout << "erros: " << errors << endl;
        cout << "tau => " << obj["tau"].asDouble();
        sys.period = obj["tau"].asDouble();                    // critical // CAMBIOS,  not works with 100,  5*60
        NB_K = obj["K"].asInt();                         // IMPORTANT BACK TO 3 VALUE  CURRENT VALUE TO TEST
        NB_D = obj["D"].asInt();                        //  NB_D = 20 , 5 IMPORTANT BACK TO 20 VALUE  CURRENT VALUE TO TEST
        //R[0] = Interval(obj["R"][0][0].asFloat(), obj["R"][0][1].asFloat()); //Interval(40.0, 70.0);          // 70
        //R[1] = Interval(obj["R"][1][0].asFloat(), obj["R"][1][1].asFloat());// Interval(0.1, 0.2);            // 0.2
        W[0] = Interval(40.0, 70.0);          // 70 if you dont define is ENTIRE the second variable:
        W[1] = Interval(0.1, 0.2);            // 0.2
        B[0] = Interval(0.0, 0.0);
        B[1] = Interval(0.0, 0.0);    
        S[0] = Interval(30.0, 80.0);
        S[1] = Interval(0.09, 0.31);
        Te   = Interval(0.0, 16.5);
        Ti   = Interval(20.0, 25.0);
        I    = Interval(0.0, 920.0);         // 910
        factorTe = 2.5;
        factorI = 0.8;
        factorE = 1.0;
        factorKe = 1.0;
        rate = 0.01;                        // 0.5
        TwaterIn = (Ti.ub() + Ti.lb())/2;     //22.5;
    }   
}