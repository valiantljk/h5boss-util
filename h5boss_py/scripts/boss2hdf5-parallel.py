import sys, os
import numpy as np
from astropy.io import fits
from astropy.table import Table
import h5boss.io
import h5boss.boss2hdf5
import time
import optparse
import traceback
from mpi4py import MPI

datapath = "/global/projecta/projectdirs/sdss/data/sdss/dr12/boss/spectro/redux/v5_7_0/"
outputpath= "/global/cscratch1/sd/jialin/h5boss/"

def listfiles():
     ldir=os.listdir(datapath)
     lldir=[fn for fn in ldir if fn.isdigit()]
     return lldir

def findseed(x):
     fitsfiles = [os.path.join(root, name)
       for root, dirs, files in os.walk(x)
       for name in files
        if name.startswith("spPlate") and name.endswith(".fits")]
     return fitsfiles

def parallel_convert():
    rank = MPI.COMM_WORLD.Get_rank()
    mpi_info = MPI.Info.Create()
    nproc = MPI.COMM_WORLD.Get_size()
    plateslist=listfiles()
    plateslist_for_each_process = [fname for fname in plateslist[:nproc]]
    platepath_for_current_rank = datapath+plateslist_for_each_process[rank]
    fitspath_name_for_current_rank = findseed(platepath_for_current_rank)
    hdf5file=fitspath_name_for_current_rank[0].split('/')[-1].replace('spPlate-','',1).replace('fits','hdf5',1)
    try:
     h5boss.boss2hdf5.serial_convert(fitspath_name_for_current_rank,outputpath+hdf5file)
    except Exception, e:
       print "Error:%s"%e, fitspath_name_for_current_rank
       traceback.print_exc()
if __name__ == '__main__':
    parallel_convert()
