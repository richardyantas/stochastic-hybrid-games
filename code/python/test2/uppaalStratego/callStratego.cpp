#include <fstream>
#include <iostream>
#include <sstream>
#include <stdio.h>
#include <stdlib.h>
#include <string>
using namespace std;

void createModel(string within, string angle, string prox, string limit, string strategoMasterModel,string strategoFinalModel, string query);
string GetStdoutFromCommand(string cmd);
int getStrategy(string out);

main(int argc, char** argv){ //./callStratego true 0.1 0.0 0.5 controller0.xml query.q
                             //./uppaalStratego/callStratego true 0.1 0.0 0.5 uppaalStratego/controller0.xml uppaalStratego/query.q
    cout.precision(3);
    cout<<fixed;
    
    string strategoMasterModel="uppaalStratego/precontroller0.xml";
    string controllerName = argv[5];
    string query = argv[6];
    string stratego = "~/Downloads/stratego/bin-Linux/verifyta " + controllerName + " " + query;
    int action;
    createModel(argv[1],argv[2],argv[3],argv[4],strategoMasterModel,argv[5],argv[6]);
    //printf("xD0\n");
    string logUppaal = GetStdoutFromCommand(stratego);
    //printf("xD1\n");
    action = getStrategy(logUppaal);
    //cout<<"action: "<<action<<" "<< action+1<<endl;
    //cout<<"logUppaal: \n"<<logUppaal<<endl;
    cout<<action<<endl;
    return 0;
}

void createModel(string within, string angle, string prox, string limit, string strategoMasterModel, string strategoFinalModel, string query){
    ifstream inFile(strategoMasterModel);
    ofstream outFile(strategoFinalModel);

    string line;
    string toReplace0 = "//HOLDER_within";
    string toReplace1 = "//HOLDER_angle";
    string toReplace2 = "//HOLDER_prox";
    string toReplace3 = "//HOLDER_limit";

    //size_t len = toReplace.length();
    bool key0= true;
    bool key1=true;
    bool key2=true;
    bool key3=true;
    while (getline(inFile, line)){
        //cout<<line<<endl;
        outFile<<line<<endl;
        if(key0==true || key1==true || key2==true || key3==true){
            if (key0== true && line.compare(toReplace0) == 0){ 
                outFile<<"bool within = "<<within<<";"<<endl;
                key0=false;
            } 
            else if(key1== true && line.compare(toReplace1) == 0){
                double dangle=atof(angle.c_str())+ 0.01;
                ostringstream buffdangle;
                buffdangle<<dangle;
                outFile<<"double angle = "<<buffdangle.str()<<";"<<endl;
                key1=false;
            }
            else if(key2== true && line.compare(toReplace2) == 0){
                double dprox=atof(prox.c_str())+ 0.0001;
                ostringstream buffdprox;
                buffdprox<<dprox;
                outFile<<"double prox = "<<buffdprox.str()<<";"<<endl;
                key2=false;
            }
            else if(key3== true && line.compare(toReplace3) == 0){
                double dlimit=atof(limit.c_str())+ 0.0001;
                ostringstream buffdlimit;
                buffdlimit<<dlimit;
                outFile<<"double limit = "<<buffdlimit.str()<<";"<<endl;
                key3=false;
            }
        }   
    }
    outFile.close();
    inFile.close();
}

string GetStdoutFromCommand(string cmd) {
    string data;
    FILE * stream;
    const int max_buffer = 256;
    char buffer[max_buffer];
    cmd.append(" 2>&1");

    stream = popen(cmd.c_str(), "r");
    if (stream) {
    while (!feof(stream))
    if (fgets(buffer, max_buffer, stream) != NULL) data.append(buffer);
    pclose(stream);
    }
    return data;
}

int getStrategy(string out){
    string str ="(5,";
    size_t found = out.find(str);
    string target = out.substr(found+3,1);

    return stoi(target);
}
