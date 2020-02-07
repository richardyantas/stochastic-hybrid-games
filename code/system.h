#pragma once
#include<iostream>
#include<vector>
#include<utility>
using namespace std;


class state
{
    public:

    double t;
    double T;
    double V;
    double E;

    
        state(){};
        state(double t, double T, double V, double E)
        {
            this->t = t;
            this->T = T;
            this->V = V;
            this->E = E;
        };
        
};


class action
{
    public:

    int r;
    int v;
    int p;
        action(){}
        action(double r, double v, double p)
        {
            this->r = r;
            this->v = v;
            this->p = p;
        }
};


class systemModel
{

    public:

    vector<state> states;
    vector<action> actions;
    double period;
    double horizont;
    state x0;
    state target;
    map< string,vector<double> > d;    

        // The goal is to optimize the function

        systemModel(double period, double horizont, state x0, map< string,vector<double> > d)
        {
            this->period = period;
            this->horizont = horizont;
            this->x0 = x0;
            this->d = d;
        };


        void run()
        {
            state s = x0;
            for(int i=0;i<horizont;i++)
            {
                action a = controller(s);
                s = post(a,x0);
            }
            
        }


        state post(action a, state x0)
        {
            // This post method is defined junt for a oen casem it should be improved
            double T = x0.T;
            double V = x0.V;
            double E = x0.E;
            double t = x0.t;
            double v = a.v;
            double r = a.r;
            double p = a.p;

            vector<double> Te = d["Temperature"];
            int s = d["Temperature"].size();
            vector<double> Ti;
            Ti.assign(s,35);
            vector<double> I  = d["GHI"];


            double dt = 1; //distance beetwen noise data 1s after to interpolation;
            int num = period/dt;

            for(int i=0; i<num; i++)  // period in seconds
            {
                t = t + dt;

                T = T + dt*( 
                        
                        -2.8811059759131854e-06*(T-Te[i])/V
                        -v*9.34673995175876e-05*(T-Ti[i])/V
                        -1/(1+100*exp(0.1*p-V))*-9.34673995175876e-05*(T-Ti[i])/V
                        +0.7*0.7*8.403225763080125e-07*I[i]/V    
                        +r*0.008801843/V 

                        );

                V = V + dt*(0.5*( 0.1*p - V));

                E = E + dt*0.1*r*0.008801843;

                //tube.push_back(state(t,V,T,E));          
                states.push_back(state(t,V,T,E));      
            }

            return state(t,T,V,E);
        }


        action controller(state s)
        {
            action a; // p, r,  v
            if( s.T < 20 )
            {               
                a.r = 1; 
                if( s.V < 0.1 )
                {
                    a.p = 1;
                }else
                {
                    a.p = -1;
                }
            }else
            {
                a.r = 0;
                if(s.V >= 0.3)
                {
                    a.p = 0;
                }else
                {
                    a.p = 1;
                }                
            }

            a.v = 0;
            /*
                s = 0;
                s = v(k) + s; 
                r(k)-p(k)
            */
            return a;
        }

};