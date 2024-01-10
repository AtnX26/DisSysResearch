from openpmd_viewer import OpenPMDTimeSeries
import time
ts = OpenPMDTimeSeries('/home/cc/diagk2')
'''tic = time.perf_counter()
ts = OpenPMDTimeSeries('/home/cc/diagk2')
toc = time.perf_counter()
print("time elapsed for OpenPMDTimeSeries:", toc-tic)

tic = time.perf_counter()
z_selected, uz_selected = ts.get_particle( ['z', 'uz'], species='electrons', iteration=0)
toc = time.perf_counter()

print("time elapsed without selection:", toc-tic)
print("z particles in total:", len(z_selected))
print("uz in total:", len(uz_selected))

#tic = time.perf_counter()
#z_selected, uz_selected = ts.get_particle( ['z', 'uz'], species='electrons', iteration=0, select={'uz':[-30, 10],'z':[-10,10]} )
#toc = time.perf_counter()

#print("time elapsed with selection:", toc-tic)
#print("z particles selected:", len(z_selected))
#print("uz selected:", len(uz_selected))
'''
from openpmd_viewer import ParticleTracker
# Select particles to be tracked, at iteration 300
tic = time.perf_counter()
pt = ParticleTracker(ts, iteration=0, select={'uz':[-30, 10],'z':[-10,10]}, species='electrons')
toc = time.perf_counter()
t1 = toc-tic
print("time elapsed for ParticleTracker that selects all the points:", t1)
tic = time.perf_counter()
z_selected, uz_selected = ts.get_particle( ['z', 'uz'], species='electrons', iteration=0, select=pt )
toc = time.perf_counter()
t2 = toc-tic
print("time elapsed for get_particle that selects the points from pt:", t2)
print("Total time:", t1+t2)

