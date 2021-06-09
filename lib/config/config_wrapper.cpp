#include <iostream>
#include <limits>
#include <string>
#include "config_wrapper.h"
#include "config_macros.h"
#include "config.h"
#include "log.h"

Log log{"libconfig.log"};
config::Config static_config;
config::Config dynamic_config;
bool loaded = false;

void load(){
    if(loaded){return;}
    //static_config.load_from_file("/home/serendipita/Documents/tesis/ucsp-solar/lib/config/static_json.json");    
    //dynamic_config.load_from_file("/home/serendipita/Documents/tesis/ucsp-solar/lib/config/dynamic_json.json");
    dynamic_config.load_from_file("/home/serendipita/Documents/tesis/ucsp-solar/sthocastic_hybrid_game/datasets/dynamic_data.json");
    static_config.load_from_file("/home/serendipita/Documents/tesis/ucsp-solar/sthocastic_hybrid_game/datasets/static_data.json");
    loaded = true;
}

//CONFIG_GETTER(double, static_config, tau,get_taumin)

CONFIG_GETTER(double, static_config, tau,get_tau)
CONFIG_GETTER(double, static_config, factorTe,get_factorTe)
CONFIG_GETTER(double, static_config, factorI,get_factorI)
CONFIG_GETTER(double, static_config, factorKe, get_factorKe)
CONFIG_GETTER(double, static_config, rate_water_input, get_rate_water_input)  // Change in Ibex !! 
CONFIG_GETTER(double, static_config, TwaterIn, get_TwaterIn)
CONFIG_GETTER(int, static_config, number_of_patterns, get_number_of_patterns)
CONFIG_GETTER(int, static_config, horizon, get_horizon)
//CONFIG_GETTER(int, static_config, get_number_of_patterns)
//LIST_GETTER(int, int, dynamic_config, get_patterns)
CONFIG_GETTER(double, dynamic_config, T, get_T)
CONFIG_GETTER(double, dynamic_config, V, get_V)
CONFIG_GETTER(double, dynamic_config, E, get_E)
CONFIG_GETTER(int, dynamic_config, t, get_time)
CONFIG_GETTER(int, dynamic_config, mode, get_mode)
CONFIG_GETTER(int, dynamic_config, valve, get_valve)

//void get_patterns(int number_of_patterns, int* arr)
void get_patterns(int32_t number_of_patterns, int32_t *arr){
    load();
    try{
        static auto tmp = dynamic_config.get<std::vector<int>>("get_patterns");
        for (int i = 0; i < number_of_patterns; i++) {
            arr[i] = tmp.at(i);
        }
    }
    catch (const std::exception &e) {
        log << e.what();
    }
}

void get_Te(int32_t horizon, double *arr){
    load();
    try {
        static auto tmp = dynamic_config.get<std::vector<double>>("Te");
        for (int i = 0; i < horizon; i++) {
            arr[i] = tmp.at(i);
        }
    }
    catch (const std::exception &e) {
        log << e.what();
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
        log << e.what();
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
        log << e.what();
    }
}

void get_prueba(int32_t *arr){
    //int arreglo[2] = {9,9};
    arr[0] = 7;
    arr[1] = 6;  
}