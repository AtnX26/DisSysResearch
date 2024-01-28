import numpy as np
import os
import re
import sys

import openpmd_api as io


def chunk_to_slice(chunk):
    """
    Convert an openPMD_api.ChunkInfo to slice
    """
    stops = [a + b for a, b in zip(chunk.offset, chunk.extent)]
    indices_per_dim = zip(chunk.offset, stops)
    index_tuple = map(lambda s: slice(s[0], s[1], None), indices_per_dim)
    return tuple(index_tuple)

path_to_dir = "/home/cc/big_runs/summit/diags/diagu"
#path_to_dir = "/home/cc/diagk2"
first_file_name = None

is_single_file = os.path.isfile(path_to_dir)
if is_single_file:
    first_file_name = path_to_dir
else:
    for file_name in os.listdir( path_to_dir ):
        if file_name.split(os.extsep)[-1] in io.file_extensions:
            first_file_name = file_name
if first_file_name is None:
    raise RuntimeError(
        "Found no valid files in directory {0}.\n"
        "Please check that this is the path to the openPMD files."
        "(valid files must have one of the following extensions: {1})"
        .format(path_to_dir, io.file_extensions))

if is_single_file:
    file_path = path_to_dir
    series_name = file_path
else:
                # match last occurance of integers and replace with %T wildcards
                # examples: data00000100.h5 diag4_00000500.h5 io12.0.bp
                #           te42st.1234.yolo.json scan7_run14_data123.h5
    file_path = re.sub(r'(\d+)(\.(?!\d).+$)', r'%T\2', first_file_name)
    series_name = os.path.join( path_to_dir, file_path)

    series = io.Series(
                series_name,
                io.Access.read_only )
    print(series)
    print(sys.getsizeof(series))
print(series.iterations[0].particles['electrons']['position'])
record = series.iterations[0].particles['electrons']['position']
if record.scalar:
    component = next(record.items())[1]
else:
    component = record['x']
print(component.shape)
print(next(series.iterations[0].particles['electrons'].items()))
print(len(component.available_chunks()))
chunk = component.available_chunks()[1]
print(chunk)
chunk_slice = chunk_to_slice(chunk)
print(chunk_slice)
