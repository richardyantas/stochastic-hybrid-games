#cmake_minimum_required(VERSION 3.10)
cmake_minimum_required(VERSION 3.20.3)
#set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "-g -fno-omit-frame-pointer -Wall")
project (ucsp-solar)
add_subdirectory(lib/jsoncpp/)
add_subdirectory(lib/config/)
add_subdirectory(sources/patterns/)


# Corregir los test 
# Corregir el pattern file and refactorize§