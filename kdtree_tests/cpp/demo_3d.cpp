//
// Demonstration of typical use cases of the kd-tree library
// Author:  Christoph Dalitz, 2024-01-08
// License: BSD style license (see the file LICENSE)
//

#include <time.h>
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <random>
#include "kdtree.hpp"

using namespace std;

//
// helper function for printing points
//
void print_nodes(const Kdtree::KdNodeVector &nodes) {
  size_t i,j;
  for (i = 0; i < nodes.size(); ++i) {
    if (i > 0)
      cout << " ";
    cout << "(";
    for (j = 0; j < nodes[i].point.size(); j++) {
      if (j > 0)
        cout << ",";
      cout << nodes[i].point[j];
    }
    cout << ")";
  }
  cout << endl;
}

//
// main program demonstrating typical use cases
//
int main(int argc, char** argv) {

  //
  // functionality tests
  //
  cout << "Functionality tests" << endl;
  cout << "-------------------" << endl;
  
  // 1.1) construction of kd-tree
  Kdtree::KdNodeVector nodes;
  constexpr int rows = 6291456;
  constexpr int cols = 3;
  //double points[rows][cols];

  // Create a random number generator
  std::random_device rd;
  std::mt19937 gen(rd());
  std::uniform_real_distribution<double> dis(0.0, 10.0); // Adjust range as needed
  
  cout << "Now testing: tree building time for "<<rows<<"points: "<<endl;
  clock_t begin = clock();
  // Fill the array with random numbers
  for (int i = 0; i < rows; ++i) {
     
          std::vector<double> point(cols);
    	  point[0] = dis(gen);
	  point[1] = dis(gen);
	  point[2] = dis(gen);
    	nodes.push_back(Kdtree::KdNode(point));
      
  }
  
  Kdtree::KdTree tree(&nodes);
  clock_t end = clock();
  double diff = double(end - begin) / CLOCKS_PER_SEC;
  cout << "Time for tree building:\n  " << diff << "s" << endl;
  
  //cout << "Points in kd-tree:\n  ";
  //print_nodes(tree.allnodes);

  Kdtree::KdNodeVector result;
  std::vector<double> test_point(3);
  
  //range query
  cout << "Now testing: range search for "<<rows<<"points: "<<endl;
  begin = clock();
  tree.rectangle_range_search(0, 5, 0, 5, 0, 5, &result);
  //print_nodes(result);
  end = clock();
  diff = double(end - begin) / CLOCKS_PER_SEC;
  cout << "Range search time:\n  " << diff << "s" << endl;
  //print_nodes(result);
  cout << "Success\n";
  }
