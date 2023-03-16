#pragma once

#define CONFIG_GETTER(type, from, key, func)                               \
    type func() { load(); return from.get<type>(#key); }

#define LIST_GETTER(p_type, list_type, from, key)                            \
    void key(p_type* arr)                                            \
    {                                                                \
        load();                                                      \
        auto tmp = from.get<std::vector<list_type>>(#key);           \
        for (unsigned int i = 0; i < tmp.size(); i++) { arr[i] = tmp.at(i); } \
    };

