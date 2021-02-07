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
    if(loaded)
    {
        return;
    }
    static_config.load_from_file("/home/serendipita/Documents/uppaalLibrary/config/static_json.json");
    dynamic_config.load_from_file("/home/serendipita/Documents/uppaalLibrary/config/dynamic_json.json");
    loaded = true;
}

//CONFIG_GETTER(double, static_config, get_tau)
CONFIG_GETTER(int, static_config, get_number_of_patterns)
//LIST_GETTER(int, int, dynamic_config, get_patterns)

void get_patterns(int32_t number_of_patterns, int32_t *arr)
//void get_patterns(int number_of_patterns, int* arr)
{
    load();
    try {
        static auto tmp = dynamic_config.get<std::vector<int>>("get_patterns");
        for (int i = 0; i < number_of_patterns; i++) {
            arr[i] = tmp.at(i);
        }
    }
    catch (const std::exception &e) {
        log << e.what();
    }
}


void get_prueba(int32_t *arr)
{
    //int arreglo[2] = {9,9};
    arr[0] = 7;
    arr[1] = 6;  
}