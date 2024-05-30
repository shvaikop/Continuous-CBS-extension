cmake_minimum_required(VERSION 2.8)

project(CCBS)

set(Boost_USE_STATIC_LIBS OFF)

# Find Boost components
find_package(Boost 1.71.0 REQUIRED COMPONENTS log log_setup thread system)
find_package(Boost COMPONENTS multi_index)

# Manually include multi_index headers (if necessary)
include_directories(${Boost_INCLUDE_DIRS})
include_directories(/usr/include)

# Include project headers
include_directories(".")

# Set compilation flags
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++2a -O2 -Wall -Wextra")

# Source files
set(SOURCE_FILES 
    main.cpp  
    config.cpp
    tinyxml2.cpp
    xml_logger.cpp 
    map.cpp 
    heuristic.cpp 
    sipp.cpp 
    task.cpp
    cbs.cpp 
    simplex/columnset.cpp
    simplex/constraint.cpp
    simplex/matrix.cpp
    simplex/objectivefunction.cpp
    simplex/simplex.cpp
    simplex/variable.cpp)

# Header files
set(HEADER_FILES
	logger.h
	logger_macros.h
    const.h  
    tinyxml2.h
    config.h
    xml_logger.h 
    map.h 
    heuristic.h 
    sipp.h 
    task.h
    cbs.h
    structs.h
    simplex/columnset.h
    simplex/constraint.h
    simplex/datamismatchexception.h
    simplex/divisionbyzeroexception.h
    simplex/indexoutofboundexception.h
    simplex/matrix.h
    simplex/matrixissingularexception.h
    simplex/matrixnotsquareexception.h
    simplex/memoryreachedoutexception.h
    simplex/notavectorexception.h
    simplex/objectivefunction.h
    simplex/pilal.h
    simplex/pilalexceptions.h
    simplex/simplex.h
    simplex/simplexexceptions.h
    simplex/sizemismatchexception.h
    simplex/variable.h)

# Add executable target
add_executable(CCBS ${SOURCE_FILES} ${HEADER_FILES})

# Link Boost libraries
target_link_libraries(CCBS 
    ${Boost_LIBRARIES} 
    Boost::log 
    Boost::log_setup 
    Boost::thread 
    Boost::system 
    pthread
	fmt)

# sudo apt-get install libfmt-dev
