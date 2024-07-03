#include "utility.hpp"
#include <adios2.h>
#include <iostream>


template<typename coordinate, std::size_t dimension>
class kdtree{

    public:

        /**
        *@brief the constructor takes in input a filename and save in a vector of type
        *       knode the values of the filename to be processed
        *@param filename
        */

        kdtree(std::string filename):
        _knodes{getValues(filename)} {
            double start = omp_get_wtime();
            _root = make_tree_parallel(0, _knodes.size(), 0);
            double stop = omp_get_wtime();
            double duration = stop - start;
            std::cout << omp_get_max_threads() << ", " << duration << std::endl;
        }

        knode<coordinate> * make_tree(std::size_t begin, std::size_t end, std::size_t index);
        knode<coordinate> * get_root() {return _root;}
        knode<coordinate> * make_tree_parallel(std::size_t begin, std::size_t end, std::size_t index);

        std::vector<knode<coordinate>> getValues(std::string filename);

        void nearest(knode<coordinate> * root, const point<coordinate, dimension>& point, size_t index);
        const point<coordinate, dimension>& nearest(const point<coordinate, dimension>& pt);

        std::size_t get_size() {return _knodes.size();}

        bool empty() const {return _knodes.empty();}
        std::size_t visited() const {return _visited;}
        double distance() const {return std::sqrt(_best_dist);}
        int depth;
    private:
        knode<coordinate> * _root = nullptr;
        std::vector<knode<coordinate>> _knodes;
        knode<coordinate> * _best = nullptr;
        std::size_t _visited;
        double _best_dist = 0;
};

/**
*   @brief main function to produce the tree in parallel. 
*   @param begin the beginnin of the dataset
*   @param end the end of the dataset
*   @param index the index axis of the node
*   @return the kdtree
*/

template<typename coordinate, std::size_t dimension>
knode<coordinate> * kdtree<coordinate, dimension>::make_tree(std::size_t begin, std::size_t end, std::size_t index){
    if(end <= begin) return nullptr;

    std::size_t med = begin + (end - begin) / 2;
    auto i = _knodes.begin();
    std::nth_element(i + begin, i + med, i + end, knode_cmp<coordinate>(index));
    _knodes[med]._axis = index;
    index = (index + 1) % DIM;

    #pragma omp task firstprivate(index)
    {
        _knodes[med]._left = make_tree(begin, med, index);
    }
    #pragma omp task firstprivate(index)
    {
        _knodes[med]._right = make_tree(med + 1, end, index);
    }

    return &_knodes[med];
}

/**
*   @brief this function create a parallel region for the function make_tree for the execution in parallel. 
*   @param begin the beginnin of the dataset
*   @param end the end of the dataset
*   @param index the index axis of the node
*   @return the kdtree
*/

template<typename coordinate, std::size_t dimension>
knode<coordinate> * kdtree<coordinate, dimension>::make_tree_parallel(std::size_t begin, std::size_t end, std::size_t index){
    knode<coordinate> * root;
    #pragma omp parallel shared(root)
    { 
        #pragma omp single 
        {
            root = make_tree(begin, end, index);
        }
    }
    return root;
}

template<typename coordinate, std::size_t dimension>
void kdtree<coordinate, dimension>::nearest(knode<coordinate> * root, const point<coordinate, dimension>& point, 
                                    size_t index) {
    if (root == nullptr)
        return;
    ++_visited;
    double d = root->distance(point);
    if (_best == nullptr || d < _best_dist) {
        _best_dist = d;
        _best = root;
    }
    if (_best_dist == 0)
        return;
    double dx = root->get(index) - point.get(index);
    index = (index + 1) % dimension;
    nearest(dx > 0 ? root-> _left : root-> _right, point, index);
    if (dx * dx >= _best_dist)
        return;
    nearest(dx > 0 ? root->_right : root->_left, point, index);
}

template<typename coordinate, std::size_t dimension>
const point<coordinate, dimension>& kdtree<coordinate, dimension>::nearest(const point<coordinate, dimension>& pt) {
    if (_root == nullptr)
        throw std::logic_error("tree is empty");
    _best = nullptr;
    _visited = 0;
    _best_dist = 0;
    nearest(_root, pt, 0);
    return _best->_point;
}

/**
*   this function get the values from the filename and stores it to a vector of knode.
*          the function is templated so can store both integer and floating point numbers
*   filename
*   @return knodes vector of integers or floating point numbers
*/

template<typename coordinate, std::size_t dimension>
std::vector<knode<coordinate>> kdtree<coordinate, dimension>::getValues(std::string filename){
    adios2::ADIOS adios;

    adios2::IO bpIO = adios.DeclareIO("BPFile_N2N");

    adios2::Engine bpReader = bpIO.Open(filename, adios2::Mode::Read);

	bpReader.BeginStep();

    //todo: add timer for data loading
        adios2::Variable<double> bpx = bpIO.InquireVariable<double>("/data/0/particles/electrons/position/x");
        adios2::Variable<double> bpy = bpIO.InquireVariable<double>("/data/0/particles/electrons/position/y");
        adios2::Variable<double> bpz = bpIO.InquireVariable<double>("/data/0/particles/electrons/position/z");

    std::vector<double> x;
    std::vector<double> y;
    std::vector<double> z;
    bpReader.Get(bpx, x, adios2::Mode::Sync);

    bpReader.Get(bpy, y, adios2::Mode::Sync);
    bpReader.Get(bpz, z, adios2::Mode::Sync);
    bpReader.EndStep();

    bpReader.Close();

    std::vector<knode<coordinate>> data;
    
    size_t rows = x.size();
    //#pragma omp parallel for
    for (int i = 0; i < rows; ++i) {

        {
          data.push_back(knode<coordinate>(point<coordinate, dimension>{{x[i], y[i], z[i]}}));
	}
  }
    std::cout<<x.size()<<data.size()<<std::endl;
    return data;
}


template<typename T>
void print_tree(knode<T> * node, const std::string &prefix, bool isLeft) {
                    
    if(node != nullptr){

        std::cout << prefix;
         std::cout << (isLeft ? "├──" : "└──" );

        // print the value of the node
        std::cout << "(" << node->_point.x() << ", " << node->_point.y() << ")" << std::endl;

        // enter the next tree level - left and right branch
        if (node->_left) print_tree(node->_left, prefix + (isLeft ? "│   " : "    "), true);

        if (node->_right) print_tree(node->_right, prefix + (isLeft ? "│   " : "    "), false);
    }
}

template<typename T>
void print_tree(knode<T> * node) {
    print_tree(node, "", false);
}
