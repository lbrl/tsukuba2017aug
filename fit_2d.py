#! /usr/bin/env python

# from ROOT import RooFit as rf
# from ROOT import *
import ROOT as r
import sys
import os
import glob
import math
# import datetime
import numpy as np
# from array import array
# import re
# import matplotlib as ml
# import matplotlib.pyplot as plt
# from PIL import Image

# R.gSystem.Load('libRooFit')

import intensity as itst


def myg2(xx, pp):
    ''' 5 parameters '''
    x, y = xx[0], xx[1]
    n = pp[0]
    mx, my = pp[1], pp[2]
    sx, sy = pp[3], pp[4]
    if sx < 0:
        sx = abs(sx)
    if sy < 0:
        sy = abs(sy)
    if n < 0:
        n = 1.
    rx = ((x-mx)/sx)**2 / 2.
    ry = ((y-my)/sy)**2 / 2.
    g = 0.15915494309*n/sx/sy * math.exp( - rx - ry )
    return g

def myg2g2p0(xx, pp):
    ''' 9 parameters '''
    g1 = myg2(xx, pp[0:5])
    g2 = myg2(xx, [pp[5], pp[1], pp[2], pp[6], pp[7]])
    c0 = pp[8]
    return g1 + g2 + c0


def myg2p0(xx, pp):
    ''' 6 parameters '''
    # g1 = myg2(xx, pp[0:5])
    g1 = myg2(xx, [pp[0], pp[1], pp[2], pp[3], pp[4]])
    c0 = pp[5]
    return g1 + c0


def main():
    Fin = r.TFile('~/kek/csibpm/data/diff_exp_time.root')
    t = Fin.Get('t')
    c1 = r.TCanvas('c1', 'c1', 600, 600)
    # c1.Divide(5, 4)
    hh2 = r.TH2F('hh2', '', 100, 0, 1600, 100, 0, 1200)
    for y in t:
        if y.time != 40.:
            continue
        print 'Find the one.'
        for j in xrange(100):
            for jj in xrange(100):
                hh2.SetBinContent(j+1, jj+1, y.arr2[j*100+jj])
    ########################################################
    f2 = r.TF2('f2', myg2p0, 300, 1100, 500, 1100, 6)
    f2.SetParameters(1e4, 750, 850, 50, 60, 8000)
    f2.SetParNames('N', 'm1', 'm2', 's1', 's2', 'c0')
    f2.SetParLimits(1, 650, 850)
    f2.SetParLimits(2, 750, 950)
    f2.SetParLimits(3, 5, 1000)
    f2.SetParLimits(4, 5, 1000)
    ########################################################
    # f2 = r.TF2('f2', myg2g2p0, 300, 1100, 500, 1100, 9)
    # f2.SetParameters(1e4, 750, 850, 50, 50, 1e4, 30, 30, 18000)
    # f2.SetParNames('N1', 'm1x', 'm1y', 's1x', 's1y', 'N2', 's2x', 's2y', 'c0')
    ########################################################
    hh2.GetZaxis().SetRangeUser(18e3, 35e3)
    # hh2.Fit(f2, 'r', 'goff', 300, 1100, 500, 1100)
    hh2.Fit(f2, 'r', '')
    hh2.Draw('lego')
    ########################################################
    c1.Update()
    raw_input('Press ENTER to continue, please.')
    Fin.Close()


if __name__ == '__main__':
    print 'Hi!'
    main()
