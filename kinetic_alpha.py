#! /usr/bin/env python

# from ROOT import RooFit as rf
# from ROOT import *
import ROOT as r
import sys
import os
import glob
# import math as m
# import datetime
import numpy as np
# from array import array
# import re
# import matplotlib as ml
# import matplotlib.pyplot as plt
# from PIL import Image

# R.gSystem.Load('libRooFit')

import intensity as itst


def main():
    file_names = glob.glob('data/20170823/hot_pixel/*min*.root')
    #
    hx = []
    for fname in file_names:
        hx.append( itst.get_projection(fname, 350, 800, isDraw=False) )
    for h in hx:
        h[0].Rebin(16)
    ymin = min([x[0].GetMinimum() for x in hx])
    ymax = max([x[0].GetMaximum() for x in hx])
    # Fitting
    ff = itst.get_gausses(file_names)
    for i, f in enumerate(ff):
        hx[i][0].Fit(f, 'r', 'goff')
    ff2 = itst.get_2gausses(file_names, ff)
    for i, f in enumerate(ff2):
        hx[i][0].Fit(f, 'r +', 'goff')
    # Tree production
    Fout = r.TFile('data/kinetic_alpha.root', 'recreate')
    tout = itst.get_tree(hx, ff, ff2)
    tout.Write()
    Fout.Close()


if __name__ == '__main__':
    print 'Hi!'
    main()
