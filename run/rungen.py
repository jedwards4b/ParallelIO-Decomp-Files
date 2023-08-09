#!/usr/bin/env python
#
#PBS  -N pioperf
#PBS  -r n
#PBS  -j oe
#PBS  -V
#PBS  -S /bin/bash
#PBS  -l select=16:ncpus=128:mpiprocs=128:ompthreads=1
#PBS  -q main
#PBS  -l walltime=00:30:00
##PBS  -A NDRS0003
import os
import glob
if os.environ.get("PBS_O_WORKDIR"):
    os.chdir(os.environ.get("PBS_O_WORKDIR"))

pioperfpaths = ["/glade/work/jedwards/sandboxes/ParallelIO/bld/tests/performance/"]

#decompdir = os.path.join(os.path.abspath(os.path.join(os.getcwd(),os.pardir)), "32768")
#decompfiles = glob.glob(os.path.join(decompdir,"dof001.dat"))

with open("pioperf.nl","w") as fd:
    fd.write("&pioperf\n")
    fd.write("  decompfile='ROUNDROBIN'\n")
#    for filename in decompfiles:
#        fd.write("   '"+filename+"',\n")
    fd.write(" varsize=18560\n");
    fd.write(" pio_typenames = 'pnetcdf', 'pnetcdf'\n");
    fd.write(" rearrangers = 2\n");
    fd.write(" nframes = 1\n");
    fd.write(" nvars = 64\n");
    fd.write(" niotasks = 16\n");
    fd.write(" /\n")

for pioperfdir in pioperfpaths:
    pioperf = os.path.join(pioperfdir, "pioperf")
    print(f"looking for {pioperf}")
    if os.path.exists(pioperf):
        print(f"starting model run {pioperf}")
        
        os.system(" LD_PRELOAD=$DARSHAN_SHARED_LIB mpiexec --label --line-buffer -n 2048 "+pioperf)
