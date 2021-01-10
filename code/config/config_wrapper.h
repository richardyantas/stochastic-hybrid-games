#pragma once
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif
    //void set_config_path(char *file_path);
    double get_tau();
    int get_number_of_patterns();
    void get_patterns(int32_t number_of_patterns, int32_t *arr);

    void get_prueba(int32_t *arr);
    //void get_patterns(int number_of_patterns, int* arr);
#ifdef __cplusplus
}
#endif

// get strategies in json
// get ibex patterns in json
