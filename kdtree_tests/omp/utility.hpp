#pragma once
#ifndef FUNCTIONS_H_INCLUDED
#define FUNCTIONS_H_INCLUDED
#include <chrono>
#include <cstring>
#include <math.h>
#include <fstream>
#include <string>
#include <sstream>
#include <filesystem>
#include <omp.h>
#include "knode.hpp"

int getMedianPosition(std::size_t begin, std::size_t end){
    int size = end - begin;
    int median_idx = size / 2 * 1 * ((size + 1) % 2);
    return median_idx;
}

int getDataRows(std::string filename){
    int rows=0;
    std::ifstream file(filename);
    std::string line;

    while (getline(file, line)){ 
        rows++;
    }

    return rows;
}


#endif
