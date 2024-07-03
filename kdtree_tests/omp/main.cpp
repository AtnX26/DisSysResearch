#include "kd_tree.hpp"

int main(int argc, char * argv[]) {

    // the main could take two tipe of knode data structure: float and integer
    // both take as input a file from a folder choose by the user in the terminal
    // if the user does not pass any file from default the functions takes the default one

    const std::string filename = "/home/dxu03/warpx_run/diags/diagu1/openpmd_000000.bp";
    double start_time = omp_get_wtime();    
    kdtree<double, 3> tree(filename);
        //#ifdef double_data_DEBUG
    double end_time = omp_get_wtime();        
    
    double elapsed_time = end_time - start_time;  // Calculate elapsed time
    printf("Elapsed time: %f seconds\n", elapsed_time);

    knode<double> * root = tree.get_root();
	    
    point<double, 3> n = tree.nearest({{0.361, 0.674}});
        	
    std::cout << filename << "\n";

    std::cout << "nearest point: " << n << '\n';

    std::cout << "distance: " << tree.distance() << '\n';

    std::cout << "nodes visited: " << tree.visited() << '\n';

        //#endif
    //#endif

    return 0;

}
