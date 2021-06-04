
project (SAFE)
set(CMAKE_CXX_STANDARD 14)

include_directories(${PROJECT_SOURCE_DIR}/config
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

add_subdirectory(src)

#enable_testing()
#add_subdirectory(test)

