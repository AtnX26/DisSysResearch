#include <algorithm>
#include <array>
#include <cmath>
#include <iostream>
#include <random>
#include <vector>

#define DIM 3
//currently we are testing 3d points


/*
*   the knode data structure
*   array array of n dimension x: position[0], y: position[1], z: position[2]
*/
template<typename coordinate, std::size_t dimension>
class point{
    public:

	// constructors
        point(std::array<coordinate, dimension> points):
            _points{points} {}
        point(std::initializer_list<coordinate> list){
            std::size_t n = std::min(dimension, list.size());
            std::copy_n(list.begin(), n, _points.begin());
        }

	// getting method
        coordinate get(std::size_t index) const{
            return _points[index];
        }

        // return the x value
        coordinate x() const {return _points[0];}

        // return the y value
        coordinate y() const {return _points[1];}

        std::string save_kpoints(int axis);

	// only using the Euclidean distance for now
	// returning the square distance (CANNOT be directly used!)
        double distance(const point& pt) const {
            double dist = 0;
            for (size_t i = 0; i < dimension; ++i) {
                double d = get(i) - pt.get(i);
                dist += d * d;
            }
            return dist;
        }

    private:
	// the array to store the coordinate
        std::array<coordinate, dimension> _points;
       
};

// overloading output stream
template<typename coordinate, std::size_t dimension>
std::ostream& operator<<(std::ostream& os, const point<coordinate, dimension>& pt) {
    os << '(';
    for (size_t i = 0; i < dimension; ++i) {
        if (i > 0)
            os << ", ";
        os << pt.get(i);
    }
    os << ')';
    return os;
}


template<typename coordinate, std::size_t dimension>
std::string point<coordinate, dimension>::save_kpoints(int axis){
    std::string s ("");
    s += "[";

    for(auto i = 0; i < dimension; i++){
        s += std::to_string(_points[i]);
        s += ",";
    }
    s += ";";
    s += std::to_string(axis);
    s += "]";

    return s;
}
