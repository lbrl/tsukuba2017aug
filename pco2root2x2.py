#! /usr/bin/env python

# from ROOT import RooFit as rf
# from ROOT import *
# import ROOT as r
import sys
import os
# import glob
# import math as m
# import datetime
# import numpy as np
# from array import array
# import re
# import matplotlib as ml
# import matplotlib.pyplot as plt
# from PIL import Image

# R.gSystem.Load('libRooFit')


def main():
    fin = sys.argv[1]
    fout = sys.argv[2]
    if not os.path.isfile(fin):
        print 'Threre is no such a file as : ', fin
        return
    os.system( '''root -b -q 'pco2root2x2.C+("{}", "{}")' '''.format(fin, fout) )


if __name__ == '__main__':
    main()
