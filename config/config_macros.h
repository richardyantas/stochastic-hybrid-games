    #pragma once

#define CONFIG_GETTER(type, from, key)                               \
    type key() { load(); return from.get<type>(#key); }  

#define LIST_GETTER(p_type, list_type, from, key)                            \
    void key(p_type* arr)                                            \
    {                                                                \
        load();                                                      \
        auto tmp = from.get<std::vector<list_type>>(#key);           \
        for (unsigned int i = 0; i < tmp.size(); i++) { arr[i] = tmp.at(i); } \
    };

// #define LIST2_GETTER(p_type, list_type, from, key)                                                  \
//     void key(int32_t num, p_type* arr)                                                              \
//     {                                                                                              \
//         if (!loaded) {                                                                             \
//             load();                                                                                \
//         }                                                                                          \
//         try {                                                                                \
//             auto tmp = from.get<std::vector<list_type>>(#key);                           \
//             for (int i = 0; i < num; i++) {                                                        \
//                  arr[i] = tmp.at(i);                                                                \
//             }                                                                                      \
//         }                                                                                          \
//         catch (const std::exception &e) {                                                          \
//             log << e.what();                                                                       \
//         }                                                                                          \
//     };
