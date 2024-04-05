#include <iostream>
#include "kdtree.hpp" // Include the header file for the KdTree implementation

int main() {
    using namespace Kdtree;

    // Define a vector of 3D points
    KdNodeVector nodes = {
        { {1.0, 2.0, 3.0} },
        { {4.0, 5.0, 6.0} },
        { {7.0, 8.0, 9.0} },
        // Add more points as needed
    };

    // Create a KdTree instance with the vector of points
    KdTree kd_tree(&nodes);

    // Define the minimum and maximum coordinates of the rectangle
    double x_min = 2.0;
    double x_max = 5.0;
    double y_min = 1.0;
    double y_max = 4.0;
    double z_min = 2.0;
    double z_max = 5.0;

    // Perform a 3D range search using the rectangle
    KdNodeVector result;
    kd_tree.rectangle_range_search(x_min, x_max, y_min, y_max, z_min, z_max, &result);

    // Output the points found within the rectangle
    std::cout << "Points within the specified rectangle:" << std::endl;
    for (const auto& point : result) {
        std::cout << "(" << point.point[0] << ", " << point.point[1] << ", " << point.point[2] << ")" << std::endl;
    }

    return 0;
}
