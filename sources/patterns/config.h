#pragma once
#include "common.h"
#include "iostream"
#include "fstream"
#include "json/json.h"

// ./bin/test_json_ifstream ./bin/data.json
// from build
// ./bin/pattern_generator ../sources/patterns/parameters.json 

namespace config
{
    using namespace std;
    sampledSwitchedSystem sys;
    IntervalVector R(2), W(2), B(2), S(2);
    Interval Te, Ti, I;
    int NB_K, NB_D;
    double factorTe, factorI, factorTi, factorE, factorKe, rate, TwaterIn;
    Json::Value root;
    //Json::String errors;
    std::ofstream ofile;
    std::ifstream ifile;
    Json::CharReaderBuilder builder;
    Json::CharReader * reader = builder.newCharReader();
    string errors;

    string jsonToString(string filename){
        string json = "",line;
        ifile.open(filename);
        while(getline(ifile,line)){
            json += line;
        }
        return json;
    }
    void readParameters(char* inputFileName, char* outputFileName){    
        ofile.open(outputFileName);
        try{
            string json = jsonToString(inputFileName);
            bool parseSuccess = reader->parse(json.c_str(),json.c_str()+json.size(), &root, &errors);
            if (parseSuccess)
            {                                
                sys.period = root["tau"].asDouble();               // critical // CAMBIOS,  not works with 100,  5*60
                NB_K = root["K"].asInt();                          // IMPORTANT BACK TO 3 VALUE  CURRENT VALUE TO TEST
                NB_D = root["D"].asInt();                         //  NB_D = 20 , 5 IMPORTANT BACK TO 20 VALUE  CURRENT VALUE TO TEST
                R[0] = Interval(root["R"][0][0].asFloat(), root["R"][0][1].asFloat()); //Interval(40.0, 70.0);          // 70
                R[1] = Interval(root["R"][1][0].asFloat(), root["R"][1][1].asFloat());// Interval(0.1, 0.2);            // 0.2
                W[0] = Interval(root["W"][0][0].asFloat(), root["W"][0][1].asFloat());          // 70 if you dont define is ENTIRE the second variable:
                W[1] = Interval(root["W"][1][0].asFloat(), root["W"][1][1].asFloat());            // 0.2
                B[0] = Interval(root["B"][0][0].asFloat(), root["B"][0][1].asFloat());
                B[1] = Interval(root["B"][1][0].asFloat(), root["B"][1][1].asFloat());
                S[0] = Interval(root["S"][0][0].asFloat(), root["S"][0][1].asFloat());
                S[1] = Interval(root["S"][1][0].asFloat(), root["S"][1][1].asFloat());
                Te   = Interval(root["Te"][0].asFloat(),root["Te"][1].asFloat());     //Interval(0.0, 16.5);
                Ti   = Interval(root["Ti"][0].asFloat(),root["Ti"][1].asFloat());     //Interval(20.0, 25.0);
                I    = Interval(root["I"][0].asFloat(),root["I"][1].asFloat());       //Interval(0.0, 920.0);         // 910
                factorTe = root["factorTe"].asFloat();  //2.5;
                factorI = root["factorI"].asFloat();    //0.8;
                factorE = root["factorE"].asFloat();    //1.0;
                factorKe = root["factorKe"].asFloat();  //1.0;
                rate = root["rate"].asFloat();          //0.01;                        // 0.5
                TwaterIn = root["TwaterIn"].asFloat();  //TwaterIn = (Ti.ub() + Ti.lb())/2;     //22.5;
            }            
            //ifile.close();
        }
        catch(std::exception& e){
            cout << "File was not found or ocurred issues during parsing .. " << endl;
        }
    }   
}