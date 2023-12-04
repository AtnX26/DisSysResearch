from openpmd_viewer import OpenPMDTimeSeries
ts = OpenPMDTimeSeries('./diagk2')

import time

tic = time.perf_counter()
z_selected, uz_selected = ts.get_particle( ['z', 'uz'], species='electrons', iteration=0)
toc = time.perf_counter()

print("time elapsed without selection:", toc-tic)
print("z particles in total:", len(z_selected))
print("uz in total:", len(uz_selected))

tic = time.perf_counter()
z_selected, uz_selected = ts.get_particle( ['z', 'uz'], species='electrons', iteration=0, select={'uz':[-10, 10],'z':[-10,10]} )
toc = time.perf_counter()

print("time elapsed with selection:", toc-tic)
print("z particles selected:", len(z_selected))
print("uz selected:", len(uz_selected))
