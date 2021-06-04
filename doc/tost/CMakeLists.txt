# target_include_directories(${PROJECT_SOURCE_DIR}/build/lib)
set(CMAKE_CXX_STANDARD 14)
include_directories(${PROJECT_SOURCE_DIR}/lib/config
                    ${PROJECT_SOURCE_DIR}/lib/jsoncpp/include
                    
                    ${PROJECT_SOURCE_DIR}/lib/dynibex
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/arithmetic
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/bisector
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/cliquer
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/combinatorial
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/contractor
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/function
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/geometry
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/integrate
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/java
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/numeric
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/parser
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/predicate
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/set
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/strategy
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/symbolic
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/system
                    ${PROJECT_SOURCE_DIR}/lib/dynibex/tools
                    )
file(GLOB SOURCES "*.cpp")
# target_link_libraries(config)
add_executable(test_libconfig test_libconfig.cpp)
# add_executable(test_json_ofstream test_json_ofstream.cpp)
# add_executable(test_json_ifstream test_json_ifstream.cpp)
# add_executable(test_ibex_json test_ibex_json.cpp)


# target_link_libraries(test_json_ifstream ${PROJECT_SOURCE_DIR}/build/lib/libjsoncpp.so)
# target_link_libraries(test_json_ofstream ${PROJECT_SOURCE_DIR}/build/lib/libjsoncpp.so)
target_link_libraries(test_libconfig PUBLIC config ${PROJECT_SOURCE_DIR}/build/lib/libjsoncpp.so)
# target_link_libraries(test_ibex_json ${PROJECT_SOURCE_DIR}/lib/dynibex/libibex.a prim ${PROJECT_SOURCE_DIR}/build/lib/libjsoncpp.so)
