#! /usr/bin/env python

# from ROOT import RooFit as rf
# from ROOT import *
import ROOT as r
import sys
import os
# import glob
# import math as m
# import datetime
import numpy as np
# from array import array
# import re
# import matplotlib as ml
# import matplotlib.pyplot as plt
# from PIL import Image

# R.gSystem.Load('libRooFit')


def main():
    Fin = r.TFile('data/20170809/converted/dark10min1pic3.root')
    hh = Fin.Get('t1')
    nx, ny = 1600, 1200
    n = nx*ny
    '''
    h = r.TH1I('h', 'h', 1000, 0, 16384)
    for i in xrange(n+1):
        h.Fill( hh.GetBinContent(i) )
    c1 = r.TCanvas('c1', 'c1', 600, 600)
    h.Draw()
    c1.Update()
    '''
    fout = open('hot_pixel_map.dat', 'w')
    for i in xrange(n+1):
        bin_con = hh.GetBinContent(i)
        if bin_con > 200 and bin_con < 16383:
            # print i, bin_con
            fout.write('{} {}\n'.format(i, bin_con))
    fout.close()
    # raw_input('')


if __name__ == '__main__':
    main()
