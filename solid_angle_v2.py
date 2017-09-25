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
    sett = 'one'
    sett = 'all'
    if sett == 'one':
        file_names = glob.glob('data/2017081?/hot_pixel/*min*40cm2.root')
    elif sett == 'all':
        file_names = glob.glob('data/201708[12]?/hot_pixel/*min*.root')
        file_names.remove('data/20170817/hot_pixel/5min1pic40cm.root')# light leak
        file_names.remove('data/20170817/hot_pixel/10min1pic40cm.root')# light leak
    else:
        return 1
    #
    hx = []
    for fname in file_names:
        hx.append( itst.get_projection(fname, 400, 800, isDraw=False) )
    for h in hx:
        h[0].Rebin(16)
    ymin = min([x[0].GetMinimum() for x in hx])
    ymax = max([x[0].GetMaximum() for x in hx])
    # Fitting
    ff = itst.get_gausses(file_names)
    for i, f in enumerate(ff):
        hx[i][0].Fit(f, 'r', 'goff')
        # subtract_baseline(hx[i][0], f.GetParameter(3))
        # f.SetParameter(3, 0.)
    ff2 = itst.get_2gausses(file_names, ff)
    for i, f in enumerate(ff2):
        hx[i][0].Fit(f, 'r +', 'goff')
    # Drawing
    c1 = r.TCanvas('c1', 'x projections', 800, 600)
    hx[0][0].Draw('e')
    for h in hx[1:]:
        h[0].Draw('e same')
    lat = r.TLatex()
    lat.SetTextSize(.025)
    for i, hh in enumerate(hx):
        lat.SetTextColor(itst.clrs[i])
        lat.DrawLatexNDC(.65, .95-.04*i, hh[0].GetName())
    ax, ay = hx[0][0].GetXaxis(), hx[0][0].GetYaxis()
    ay.SetRangeUser(ymin, ymax*1.05)
    for f in ff:
        f.Draw('same')
    for f in ff2:
        f.Draw('same')
    c1.Update()
    # Print results
    # c2 = itst.get_trend_plot(ff, 1, 'mean')
    # c3 = itst.get_trend_plot(ff, 2, 'sigma')
    # c4 = itst.get_trend_plot(ff, 0, 'Amplitude')
    # I vs L
    c_I_vs_L = itst.get_intensity_vs_distance(hx)
    raw_input('Press ENTER to continue, please.')
    # c_I_vs_L[0].SaveAs('img/integral_intensity_vs_distance_over_time.png')


if __name__ == '__main__':
    main()
