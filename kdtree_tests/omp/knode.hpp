#include "point.hpp"

// this is the header of the actual node. Will add bounds and other query methods to make it complete later


template<typename coordinate>
struct knode{
 
    typedef point<coordinate, DIM> point_type;
	
    // constructor 
    knode(const point_type& pt):
        _point{pt}, _left{nullptr}, _right{nullptr}, _axis{-1} {}

    // return the point at axis index
    coordinate get(std::size_t index) const{
        return _point.get(index);
    }

    // return the distance
    double distance(const point_type& pt) const{
        return _point.distance(pt);
    }

    point_type _point;
    int _axis;
    knode<coordinate> * _left;
    knode<coordinate> * _right;


};

/**
*  Similar comparator in the original version
*/
template<typename T>
struct knode_cmp{
    knode_cmp(std::size_t index): 
        _index{index} {}
    bool operator()(const knode<T>& n1, const knode<T>& n2) const{
        return n1._point.get(_index) < n2._point.get(_index);
    }

    std::size_t _index;
};
