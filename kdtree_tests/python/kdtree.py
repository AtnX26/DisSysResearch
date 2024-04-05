import numpy as np
import sys
sys.path.append('/home/dxu03/adiosnewbuild/lib/python3/dist-packages')
from adios2 import Stream, FileReader
import time
tic = time.perf_counter()
with FileReader("/home/dxu03/warpx_run/diags/diagu1/openpmd_000000.bp") as ibpFile:
        # scalar variables are read as a numpy array with 0 dimension
        x = ibpFile.read("/data/0/particles/electrons/position/x")
        y = ibpFile.read("/data/0/particles/electrons/position/y")
        z = ibpFile.read("/data/0/particles/electrons/position/z")
        #print(x[0:10])
toc = time.perf_counter()
print("finished reading data: "+str(len(x))+" particles")
print("Time elapsed for importing data with ADIOS2:", toc-tic)
tic = time.perf_counter()
result_array = list(zip(x,y,z))
#print(result_array[1:10])
toc = time.perf_counter()
print("Time elapsed for zipping xyz :", toc-tic)
from scipy.spatial import KDTree

def rectangular_range_query(kd_tree, lower_bounds, upper_bounds):
    lower_bounds = np.array(lower_bounds)
    upper_bounds = np.array(upper_bounds)
    assert len(lower_bounds) == kd_tree.m
    assert len(upper_bounds) == kd_tree.m

    # Perform query
    indices = kd_tree.query_ball_point(lower_bounds, np.linalg.norm(upper_bounds - lower_bounds))
    
    # Filter out points that are outside the rectangle
    filtered_indices = []
    for idx in indices:
        point = kd_tree.data[idx]
        if np.all((point >= lower_bounds) & (point <= upper_bounds)):
            filtered_indices.append(idx)
    
    return filtered_indices

# Example usage:
#points = np.random.rand(1000, 3)  # Generate random 3D points
print("Inserting into kd_tree...")
tic = time.perf_counter()
kd_tree = KDTree(result_array)
toc = time.perf_counter()
print("Time elapsed for building the kd_tree: ", toc-tic)
lower_bounds = [0, 0, 0]
upper_bounds = [0.5, 0.6, 0.7]
print("lower_bounds: "+str(lower_bounds))
print("upper_bounds: "+str(upper_bounds))
print("Querying...")
tic = time.perf_counter()
indices = rectangular_range_query(kd_tree, lower_bounds, upper_bounds)
toc = time.perf_counter()
print("Time elapsed for range querying the kd_tree: ", toc-tic)
print("Indices of points within the rectangular range:", indices[:10])
print("points: "+str(len(indices)))
