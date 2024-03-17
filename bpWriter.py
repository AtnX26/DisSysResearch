#from mpi4py import MPI
import numpy as np
import sys
sys.path.append('/home/dxu03/adiosnewbuild/lib/python3/dist-packages')
import adios2

# uncomment if using MPI
#comm = MPI.COMM_WORLD
#rank = comm.Get_rank()
#size = comm.Get_size()

basepath = "/data/%T/"


# ADIOS MPI Communicator
adios = adios2.Adios(config_file=None)

# ADIOS IO
bpIO = adios.declare_io("BPFile_N2N")

bpIOParams = {}
bpIOParams["Threads"] = "2"
bpIOParams["ProfileUnits"] = "Microseconds"
bpIOParams["InitialBufferSize"] = "17Kb"
bpIO.set_parameters(bpIOParams)

bpIO.add_transport("File", {"Library": "fstream"})
bpIO.set_engine("BPFile")
a = bpIO.adios()

#size=1
#rank=1
#Nx=10
#myArray=[1,2,3,4,5,6,7,8,9,10]
# ADIOS output stream
from tqdm import tqdm
pbar = tqdm(total=123)

print("writing attributes...")
with adios2.Stream(bpIO, "bpWriter-py.bp", "w") as fh:
    fh.write_attribute("/basePath", "/data/%T/") 
    pbar.update(1)
    fh.write_attribute("/data/0/dt", np.array(1, dtype=np.double))
    pbar.update(1)
    print("writing attributes for fields...")
    for i in ["B","E","j"]:
        fh.write_attribute("/data/0/fields/"+i+"/axisLabels", ["z","y","x"])
        pbar.update(1)
        fh.write_attribute("/data/0/fields/"+i+"/dataOrder", "C")
        pbar.update(1)
        fh.write_attribute("/data/0/fields/"+i+"/fieldSmoothing", "none")
        pbar.update(1)
        fh.write_attribute("/data/0/fields/"+i+"/geometry", "cartesian")
        pbar.update(1)
        fh.write_attribute("/data/0/fields/"+i+"/gridGlobalOffset", np.array([-2e-05, -2e-05, -2e-05], dtype=np.double))
        pbar.update(1)
        fh.write_attribute("/data/0/fields/"+i+"/gridSpacing", np.array([4.16667e-07, 3.125e-07, 3.125e-07], dtype=np.double))
        pbar.update(1)
        fh.write_attribute("/data/0/fields/"+i+"/gridUnitSI", np.array(1, dtype=np.double))
        pbar.update(1)
        fh.write_attribute("/data/0/fields/"+i+"/timeOffset", 0.0)
        pbar.update(1)
        fh.write_attribute("/data/0/fields/"+i+"/x/position", np.array([0.5, 0.5, 0.5], dtype=np.double))
        pbar.update(1)
        fh.write_attribute("/data/0/fields/"+i+"/x/unitSI", np.array(1, dtype=np.double))
        pbar.update(1)
        fh.write_attribute("/data/0/fields/"+i+"/y/position", np.array([0.5, 0.5, 0.5], dtype=np.double))
        pbar.update(1)
        fh.write_attribute("/data/0/fields/"+i+"/y/unitSI", np.array(1, dtype=np.double))
        pbar.update(1)
        fh.write_attribute("/data/0/fields/"+i+"/z/position", np.array([0.5, 0.5, 0.5], dtype=np.double))
        pbar.update(1)
        fh.write_attribute("/data/0/fields/"+i+"/z/unitSI", np.array(1, dtype=np.double))
        pbar.update(1)
    fh.write_attribute("/data/0/fields/B/unitDimension", np.array([0, 1, -2, -1, 0, 0, 0], dtype=np.double))
    pbar.update(1)
    fh.write_attribute("/data/0/fields/E/unitDimension", np.array([1, 1, -3, -1, 0, 0, 0], dtype=np.double))
    pbar.update(1)
    fh.write_attribute("/data/0/fields/j/unitDimension", np.array([-2, 0, 0, 1, 0, 0, 0], dtype=np.double))
    pbar.update(1)
    fh.write_attribute("/data/0/fields/chargeCorrection", "none")
    pbar.update(1)
    fh.write_attribute("/data/0/fields/currentSmoothing", "Binomial")
    pbar.update(1)
    fh.write_attribute("/data/0/fields/currentSmoothingParameters", "period=1;compensator=false;numPasses_x=1;numPasses_y=1;numPasses_z=1")
    pbar.update(1)
    fh.write_attribute("/data/0/fields/fieldBoundary", ["open", "open", "open", "reflecting", "reflecting", "reflecting"])
    pbar.update(1)
    fh.write_attribute("/data/0/fields/fieldSolver", "Yee")
    pbar.update(1)
    fh.write_attribute("/data/0/fields/particleBoundary", ["absorbing", "absorbing", "absorbing", "absorbing", "absorbing", "absorbing"])
    pbar.update(1)

    print("writing particles attributes...")
    for i in ["electrons"]:
        prefix="/data/0/particles/"+i+"/"
        for t in ["charge","id", "mass", "momentum", "position", "positionOffset", "weighting"]:
            if (t=="weighting"):
                fh.write_attribute(prefix+t+"/macroWeight", np.array(1, dtype=np.uint32))
                pbar.update(1)
            else:
                fh.write_attribute(prefix+t+"/macroWeight", np.array(0, dtype=np.uint32))
                pbar.update(1)
            #fh.write_attribute(prefix+i+"/shape", np.array([12582912], dtype=np.uint64_t))
            #pbar.update(1)
            fh.write_attribute(prefix+t+"/timeOffset", np.array(0, dtype=float))
            pbar.update(1)
            #fh.write_attribute(prefix+i+"/unitDimension", np.array([0, 0, 1, 1, 0, 0, 0], dtype=np.double))
            #pbar.update(1)
            if (t in ("charge", "id", "mass", "weighting")):
                #fh.write_attribute(prefix+i+"/shape", np.array([12582912], dtype=np.uint64_t))
                #pbar.update(1)
                fh.write_attribute(prefix+t+"/unitSI", np.array(1, dtype=np.double))
                pbar.update(1)
            else:
                fh.write_attribute(prefix+t+"/x/unitSI", np.array(1, dtype=np.double))
                pbar.update(1)
                fh.write_attribute(prefix+t+"/y/unitSI", np.array(1, dtype=np.double))
                pbar.update(1)
                fh.write_attribute(prefix+t+"/z/unitSI", np.array(1, dtype=np.double))
                pbar.update(1)
                #fh.write_attribute(prefix+i+"/x/shape", np.array([12582912], dtype=np.uint64_t))
                #pbar.update(1)
                #fh.write_attribute(prefix+i+"/y/shape", np.array([12582912], dtype=np.uint64_t))
                #pbar.update(1)
                #fh.write_attribute(prefix+i+"/z/shape", np.array([12582912], dtype=np.uint64_t))
                #pbar.update(1)
            #fh.write_attribute(prefix+i+"/value", np.array(-1.60218e-19, dtype=np.double))
            #pbar.update(1)
            if (t in ("charge", "mass", "momentum", "weighting")):
                fh.write_attribute(prefix+t+"/weightingPower", np.array(1, dtype=np.double))
                pbar.update(1)
            else:
                fh.write_attribute(prefix+t+"/weightingPower", np.array(0, dtype=np.double))
                pbar.update(1)
        prefix="/data/0/particles/"+i
        fh.write_attribute(prefix+"/currentDeposition", "Esirkepov")
        pbar.update(1)
        fh.write_attribute(prefix+"/charge/unitDimension", np.array([0, 0, 1, 1, 0, 0, 0], dtype=np.double))
        pbar.update(1)
        fh.write_attribute(prefix+"/id/unitDimension", np.array([0, 0, 0, 0, 0, 0, 0], dtype=np.double))
        pbar.update(1)
        fh.write_attribute(prefix+"/mass/unitDimension", np.array([0, 1, 0, 0, 0, 0, 0], dtype=np.double))
        pbar.update(1)
        fh.write_attribute(prefix+"/momentum/unitDimension", np.array([1, 1, -1, 0, 0, 0, 0], dtype=np.double))
        pbar.update(1)
        fh.write_attribute(prefix+"/position/unitDimension", np.array([1, 0, 0, 0, 0, 0, 0], dtype=np.double))
        pbar.update(1)
        fh.write_attribute(prefix+"/positionOffset/unitDimension", np.array([1, 0, 0, 0, 0, 0, 0], dtype=np.double))
        pbar.update(1)
        fh.write_attribute(prefix+"/weighting/unitDimension", np.array([0, 0, 0, 0, 0, 0, 0], dtype=np.double))
        pbar.update(1)
        fh.write_attribute(prefix+"/charge/value", np.array(-1.60218e-19, dtype=np.double))
        pbar.update(1)
        fh.write_attribute(prefix+"/mass/value", np.array(9.10938e-31, dtype=np.double))
        pbar.update(1)
        fh.write_attribute(prefix+"/positionOffset/x/value", np.array(0, dtype=np.double))
        pbar.update(1)
        fh.write_attribute(prefix+"/positionOffset/y/value", np.array(0, dtype=np.double))
        pbar.update(1)
        fh.write_attribute(prefix+"/positionOffset/z/value", np.array(0, dtype=np.double))
        pbar.update(1)
        fh.write_attribute(prefix+"/charge/shape", np.array([12582912], dtype=np.uint64))
        pbar.update(1)
        fh.write_attribute(prefix+"/mass/shape", np.array([12582912], dtype=np.uint64))
        pbar.update(1)
        fh.write_attribute(prefix+"/positionOffset/x/shape", np.array([12582912], dtype=np.uint64))
        pbar.update(1)
        fh.write_attribute(prefix+"/positionOffset/y/shape", np.array([12582912], dtype=np.uint64))
        pbar.update(1)
        fh.write_attribute(prefix+"/positionOffset/z/shape", np.array([12582912], dtype=np.uint64))
        pbar.update(1)
        fh.write_attribute(prefix+"/particleInterpolation", "energyConserving")
        pbar.update(1)
        fh.write_attribute(prefix+"/particlePush", "Boris")
        pbar.update(1)
        fh.write_attribute(prefix+"/particleShape", np.array(3, dtype=np.double))
        pbar.update(1)
        fh.write_attribute(prefix+"/particleShapes", np.array([3, 3, 3], dtype=np.double))
        pbar.update(1)
        fh.write_attribute(prefix+"/particleSmoothing", "none")
        pbar.update(1)
        #for t in ["id", "mass", "momentum", "position", "positionOffset", "weighting"]:
        fh.write_attribute("/data/0/time", 0.0)
        pbar.update(1)
        fh.write_attribute("/data/0/timeUnitSI", 1.0)
        pbar.update(1)
        fh.write_attribute("/date", "2024-03-11 19:35:09 +0000")
        pbar.update(1)
        fh.write_attribute("/iterationEncoding", "fileBased")
        pbar.update(1)
        fh.write_attribute("/iterationFormat", "openpmd_%06T")
        pbar.update(1)
        fh.write_attribute("/meshesPath", "fields/")
        pbar.update(1)
        fh.write_attribute("/openPMD", "1.1.0")
        pbar.update(1)
        fh.write_attribute("/openPMDextension", np.array(1, dtype=np.uint32))
        pbar.update(1)
        fh.write_attribute("/particlesPath", "particles/")
        pbar.update(1)
        fh.write_attribute("/software", "WarpX")
        pbar.update(1)
        fh.write_attribute("/softwareVersion", "24.03-1-ge38acc4da155")
        pbar.update(1)
        fh.write_attribute("__openPMD_internal/openPMD2_adios2_schema", np.array(0, dtype=np.uint64))
        pbar.update(1)
        fh.write_attribute("__openPMD_internal/useSteps", np.array(0, dtype=np.uint8))
        pbar.update(1)
    pbar.close()
    print("writing field data...")
    pb = tqdm(total=9)
    x = int(4096/16)
    y = x
    z = int(3072/16)
    f_shape = (x, y, z)
    p_shape = x*y*z*8
    #f_array = np.random.rand(*f_shape)

    for i in ["B", "E", "j"]:
        for t in ["x", "y", "z"]:
            f_array = np.random.rand(*f_shape)
            fh.write('/data/0/fields/'+i+"/"+t,np.copy(f_array),f_array.shape,[0,0,0],f_array.shape)
            pb.update(1)

    pb.close()

    print("writing particle data...")
    pb_pa = tqdm(total=8)
    for i in ["id", "momentum/x", "momentum/y", "momentum/z", "position/x", "position/y", "position/z", "weighting"]:
        p_array = np.random.rand(p_shape)
    #with adios2.Stream(bpIO, "bpWriter-py.bp", "w") as fh:
        fh.write('/data/0/particles/electrons/'+i,np.copy(p_array),[p_shape],[p_shape],[p_shape])
        pb_pa.update(1)
    pb_pa.close()
#with adios2.Stream(bpIO, "bpWriter-py.bp", "w") as fh:
#    fh.write('asdf', 123)
#with adios2.Stream(bpIO, "bpWriter-py.bp", "w") as fh:
#    fh.write('/qwer', 324)
    #
    #fh.write("bpArray", myArray, [size * Nx], [rank * Nx], [Nx])
    #fh.write("Nx", Nx)
    #fh.write_attribute("size", Nx, "bpArray")
    #fh.write_attribute("dimensions", ["Nx"], "bpArray")
    #fh.write_attribute("dim", 2)
#pbar.close()
# Read content:
# bpls -la bpWriter-py.bp
# bpls -la bpWriter-py.bp -d bpArray -n 10
# bpls -la bpWriter-py.bp -d bpArray -n 10 -D
