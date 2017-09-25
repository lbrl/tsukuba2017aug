#! /usr/bin/env python

# from ROOT import RooFit as rf
# from ROOT import *
import ROOT as R
import sys
# import os
# import glob
# import math as m
# import datetime
import numpy as np
from array import array
# import re

# R.gSystem.Load('libRooFit')


def main(finname, foutname=-1, isDraw=True):
    print 'The input file : ', finname
    print 'The output file : ', foutname
    Fin = R.TFile(finname)
    pixelmode = -1
    if '2by2' in finname:
        pixelmode = 2
    elif '1by1' in finname:
        pixelmode = 1
    else:
        print 'The binning is unknown.'
        ans = raw_input('Please, input a pixel mode. [1|2]: ')
        if ans in ['1', '2']:
            pixelmode = int(ans)
        else:
            return
    if pixelmode == 1:
        print '1x1 pixel mode.'
        h = R.TH2F('hm', 'hm', 1600, 0, 1600, 1200, 0, 1200)
    elif pixelmode == 2:
        print '2x2 pixel mode.'
        h = R.TH2F('hm', 'hm', 800, 0, 800, 600, 0, 600)
    else:
        print 'The binning is unknown.'
        return
    if 'rot' in finname or '_r.root' in finname:
        isRaw = False
        t = Fin.Get('t')
        print 'The data is rotated.'
    else:
        isRaw = True
        t = Fin.Get('tree')
        print 'The data is not rotated.'
    if isDraw:
        c1 = R.TCanvas('c1', 'c1', 400, 400)
    if foutname == -1:
        Fout = R.TFile('merged.root', 'recreate')
        print 'Output file :  merged.root'
    else:
        Fout = R.TFile(foutname, 'recreate')
        print 'Output file : ', foutname
    count = 0
    for y in t:
        if count % 50 == 0:
            print count
        count += 1
        if isRaw:
            h.Add(y.t1)
        else:
            h.Add(y.h)
    h.Scale( 1./t.GetEntries() )
    if isDraw:
        h.Draw('colz')
        c1.Update()
        raw_input('Press ENTER to continue, please.')
    h.Write()
    Fout.Close()
    Fin.Close()


if __name__ == '__main__':
    argv = []
    isDraw = True
    for arg in sys.argv:
        if arg == '-b':
            isDraw = False
        if arg in ['-q', '-b']:
            continue
        argv.append(arg)
    if len(argv) == 2:
        main(argv[1], isDraw=isDraw)
    elif len(argv) == 3:
        main(argv[1], argv[2], isDraw=isDraw)
    else:
        print 'Usage:'
        print '\t{} path/to/input/file.root'.format(sys.argv[0])
        print '\t{} path/to/input/file.root path/to/output/file.root'.format(sys.argv[0])
