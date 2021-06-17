#pragma once
#include <stdint.h>
//void set_config_path(char *file_path);
#ifdef __cplusplus
extern "C" {
#endif
    // static file
    //double get_tau();
    int get_tau();
    // double get_taumin(){
    //     return int(get_tau()/60);
    // };
    double get_factorTe();
    double get_factorI();
    double get_factorKe();
    double get_rate_water_input();
    double get_TwaterIn();    
    int get_number_steps();

    // dynamic file
    double get_T();
    double get_V();
    double get_E();
    int get_time();
    int get_mode();
    int get_valve();    
    void get_Te(int horizon, double *arr);
    void get_Ti(int horizon, double *arr);
    void get_I(int horizon, double *arr);
#ifdef __cplusplus
}
#endif

