#pragma once

#include<fstream>
#include<iostream>
#include<vector>
#include<string>
#include<algorithm>
#include<boost/algorithm/string.hpp>
#include <queue>
#include <sstream>
#include <cmath>
#include <map>
#include <cstdio>

#include <utility>

using namespace std;

class CVSReader
{
    vector<double> data;
    string path;
    string delm;
    public:
        CVSReader(){};
        CVSReader(string path, string delm = ",")
        {
            this->path = path;
            this->delm = delm;
        }

        map<string,vector<double>> getFeatures();
        
        pair<bool, double> string2double(string s)
        {
            stringstream ss;
            double value;
            ss << s;
            ss >> value; 

            pair<bool, double> p;


            if(ss.fail())
            {
                cout << "Error "<< endl;
                p = make_pair(false,1.0);
            }
            else
            {
                p = make_pair(true,value);
            }
            return p;
        }
        
};

// 30 minutes;

map<string,vector<double>> CVSReader::getFeatures()
{
    
    //cout << path << endl;

    cout << path << endl;
    ifstream file(path.c_str()); // important to call from executable
    vector<vector<string>> dataList;
    std::string line;
    //getline(file,line);
    while( getline(file,line) )
    {
        vector<string> vec;
        boost::algorithm::split(vec,line, boost::is_any_of(delm));
        dataList.push_back(vec);
        
    }
    file.close();
    int n = dataList[0].size();
    vector<vector<double>> table(n);

    for(int i=0;i<dataList[0].size();i++)
    {
        for(int j=1;j<dataList.size();j++)
        {
            pair<bool, double> t = string2double(dataList[j][i]);
            table[i].push_back( t.second );   
        }
    }

    
    map<string,vector<double>> features;

    for(int i=0;i<dataList[0].size();i++)
    {
        features[ dataList[0][i] ] = table[i];
    }
    
    return features;

}