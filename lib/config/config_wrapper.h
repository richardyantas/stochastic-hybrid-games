#pragma once
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif
    //void set_config_path(char *file_path);
    double get_tau();
    double get_taumin(){
        return int(get_tau()/60);
    };
    double get_factorTe();
    double get_factorI();
    double get_factorKe();
    double get_rate_water_input();
    double get_TwaterIn();
    int get_number_of_array();
    int get_horizon();

    // dynamic
    double get_T();
    double get_V();
    double get_E();
    int get_time();
    int get_mode();
    int get_valve();
    //void get_patterns(int32_t number_of_patterns, int32_t *arr);
    //void get_prueba(int32_t *arr);
    void get_array(int number_of_array, int* arr);
    void get_double_array(int number_of_array, double* arr);

    void get_Te(int horizon, double *arr);
    void get_Ti(int horizon, double *arr);
    void get_I(int horizon, double *arr);
#ifdef __cplusplus
}
#endif

// get strategies in json
// get ibex patterns in json
