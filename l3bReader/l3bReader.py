import netCDF4 as nc
import numpy as np
import argparse
import logging

# Class/function to parse command line

# Class/function to open/process L3b file
    # facilities incl.:
        # opening file
        # accessing data
        # options for combining data in a number of ways
        # writing data in a number of format
        # plotting?

class CReadL3b():
    def __init__(self,fpath,prods):
        with nc.Dataset(fpath) as ds:
            gvl3b = ds.groups['level-3_binned_data'].variables

# Main
