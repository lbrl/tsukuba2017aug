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


def get_hot():
    nx, ny = 1600, 1200
    n = nx*ny
    fin = open('hot_pixel_map.dat')
    hot = []
    for line in fin:
        x = int(line.split()[0])
        hot.append([x])
        raw = (x-1)/nx + 1
        column = (x-1)%nx + 1
        if 1 < column and column < nx:
            if 1 < raw and raw < ny:
                a = 1
                hot[-1].extend([x-a, x+a, x-a-a*nx, x-a*nx, x+a-a*nx, x-a+a*nx, x+a*nx, x+a+a*nx])
            elif raw == 1:
                hot[-1].extend([x-1, x+1, x-1-nx, x-nx, x+1-nx])
            elif raw == ny:
                hot[-1].extend([x-1, x+1, x-1+nx, x+nx, x+1+nx])
        elif column == 1:
            if 1 < raw and raw < ny:
                hot[-1].extend([x+1, x-nx, x+1-nx, x+nx, x+1+nx])
            elif raw == 1:
                hot[-1].extend([x+1, x-nx, x+1-nx])
            elif raw == ny:
                hot[-1].extend([x+1, x+nx, x+1+nx])
        elif column == nx:
            if 1 < raw and raw < ny:
                hot[-1].extend([x-1, x-nx, x-1-nx, x+nx, x-1+nx])
            elif raw == 1:
                hot[-1].extend([x-1, x-nx, x-1-nx])
            elif raw == ny:
                hot[-1].extend([x-1, x+nx, x-1+nx])
    fin.close()
    return hot


def main():
    hot = get_hot()
    for fname in sys.argv[1:]:
        if not os.path.isfile(fname):
            print '{} is not a file.'.format(fname)
        Fin = r.TFile(fname, 'read')
        if Fin.IsZombie():
            print 'A problem with the file.'
        #
        if 'merged' in fname:
            print 'Work with a mergred histogram.'
            hh = Fin.Get('hm')
            foutname = fname.replace('merged', 'hot_pixel')
        elif 'splitted' in fname:
            print 'Work with a splitted histogram.'
            hh = Fin.Get('hm')
            foutname = fname.replace('splitted', 'hot_pixel')
        elif 'converted' in fname:
            print 'Work with single converted histogram.'
            hh = Fin.Get('t1')
            foutname = fname.replace('converted', 'hot_pixel')
        elif 'hot_pixel' in fname:
            print 'Skip this old fashion input.'
            continue
        else:
            print 'Don not understand where this file comes from. Skip it.'
            continue
        hh0 = hh.Clone('hh0')
        for ho in hot:
            ave = 0
            # bc_old = hh.GetBinContent(h)
            for h in ho[1:]:
                ave += hh.GetBinContent(h)
            ave /= len(ho[1:])
            hh.SetBinContent(ho[0], ave)
            # print bc_old, ave, hh.GetBinContent(h)
        #
        Fout = r.TFile(foutname, 'recreate')
        nx, ny = 1600, 1200
        n = nx*ny
        hhout = r.TH2I('hh', 'hh', nx, 0, nx, ny, 0, ny)
        for i in xrange(1, n+1):
            hhout.SetBinContent(i, hh.GetBinContent(i))
        hhout.Write()
        Fout.Close()


if __name__ == '__main__':
    main()
