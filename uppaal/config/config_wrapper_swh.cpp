#include <iostream>
#include <limits>
#include <string>
#include "config_wrapper_swh.h"
#include "config_macros.h"
#include "config.h"
#include "log.h"

//Log log{"libconfig.log"};
config::Config static_config;
config::Config dynamic_config;
bool loaded = false;

void load(){
    if(loaded){return;}
    //static_config.load_from_file("/home/serendipita/Documents/tesis/ucsp-solar/lib/config/static_json.json");    
    //dynamic_config.load_from_file("/home/serendipita/Documents/tesis/ucsp-solar/lib/config/dynamic_json.json");
    
    // dynamic_config.load_from_file("/home/serendipita/Documents/tesis/ucsp-solar/stochastic_hybrid_game/datasets/dynamic_data.json");
    // static_config.load_from_file("/home/serendipita/Documents/tesis/ucsp-solar/stochastic_hybrid_game/datasets/static_data.json");
    dynamic_config.load_from_file("/app/data/solar-water-heating/dynamic_data.json");
    static_config.load_from_file("/app/data/solar-water-heating/static_data.json");

    loaded = true;
}

// static variables
CONFIG_GETTER(int, static_config, tau,get_tau)
CONFIG_GETTER(double, static_config, factorTe,get_factorTe)
CONFIG_GETTER(double, static_config, factorI,get_factorI)
CONFIG_GETTER(double, static_config, factorKe, get_factorKe)
CONFIG_GETTER(double, static_config, rate_water_input, get_rate_water_input)  // Change in Ibex !! 
CONFIG_GETTER(double, static_config, TwaterIn, get_TwaterIn)
CONFIG_GETTER(int, static_config, number_of_array, get_number_of_array)
CONFIG_GETTER(int, static_config, nrSteps, get_number_steps)

CONFIG_GETTER(double, static_config, Tg,get_Tg)
CONFIG_GETTER(double, static_config, alpha,get_alpha)
// dynamic variables
CONFIG_GETTER(double, dynamic_config, T, get_T)      // OK
CONFIG_GETTER(double, dynamic_config, V, get_V)      // OK
CONFIG_GETTER(double, dynamic_config, E, get_E)      // OK
CONFIG_GETTER(int, dynamic_config, t, get_time)      // OK
CONFIG_GETTER(int, dynamic_config, mode, get_mode)   // OK
CONFIG_GETTER(int, dynamic_config, valve, get_valve) // OK

void get_Te(int32_t horizon, double *arr){
    load();
    try {
        static auto tmp = dynamic_config.get<std::vector<double>>("Te");
        for (int i = 0; i < horizon; i++) {
            arr[i] = tmp.at(i);
        }
    }
    catch (const std::exception &e) {
        //log << e.what();        
    }
}

void get_Ti(int32_t horizon, double *arr){
    load();
    try {
        static auto tmp = dynamic_config.get<std::vector<double>>("Ti");
        for (int i = 0; i < horizon; i++) {
            arr[i] = tmp.at(i);
        }
    }
    catch (const std::exception &e) {
        //log << e.what();
    }
}

void get_I(int32_t horizon, double *arr){
    load();
    try {
        static auto tmp = dynamic_config.get<std::vector<double>>("I");
        for (int i = 0; i < horizon; i++) {
            arr[i] = tmp.at(i);
        }
    }
    catch (const std::exception &e) {
        //log << e.what();
    }
}