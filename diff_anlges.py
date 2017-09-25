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


def get_mean(name):
    a = { 'inf' : 800, '1' : 1050, '2' : 1100, '1o2' : 900, '3' : 1050,
            '6o5' : 950}
    for key, val in a.iteritems():
        if 'tan'+key in name:
            return val
    return 750


def main():
    file_names = glob.glob('data/20170824/hot_pixel/*min*.root')
    #
    hx = []
    mean = []
    for fname in file_names:
        hx.append( itst.get_projection(fname, 350, 800, isDraw=False,
            isRoundAndCenterd=False) )
        mean.append(get_mean(fname))
    for h in hx:
        h[0].Rebin(16)
    ymin = min([x[0].GetMinimum() for x in hx])
    ymax = max([x[0].GetMaximum() for x in hx])
    # Fitting
    ff = itst.get_gausses(file_names, mean=mean)
    for i, f in enumerate(ff):
        hx[i][0].Fit(f, 'r', 'goff')
    ff2 = itst.get_2gausses(file_names, ff)
    for i, f in enumerate(ff2):
        hx[i][0].Fit(f, 'r +', 'goff')
    # Tree production
    Fout = r.TFile('data/diff_angles.root', 'recreate')
    tout = itst.get_tree(hx, ff, ff2)
    print 'The tree contains {} entries.'.format(tout.GetEntries())
    tout.Write()
    Fout.Close()


if __name__ == '__main__':
    print 'Hi!'
    main()
