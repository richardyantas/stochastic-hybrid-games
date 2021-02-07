
// #if __has_include("json/json.h")
// #include <json/json.h>
// #else
// #include <jsoncpp/json/json.h>
// #endif
#include "../lib/jsoncpp/include/json/json.h"

struct JsonConversionException : public std::exception {
    const char *what() const noexcept override { return "Cannot convert json to object"; }
};

