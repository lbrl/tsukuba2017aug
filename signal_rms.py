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
    if len(sys.argv) > 1:
        file_names = sys.argv[1:]
    else:
        file_names = glob.glob('data/2017081?/hot_pixel/*min*.root')
        file_names.remove('data/20170817/hot_pixel/5min1pic40cm.root')# light leak
        file_names += glob.glob('data/20170821/hot_pixel/*min*.root')
        file_names += glob.glob('data/20170808/hot_pixel/*min*cm*.root')
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
    lat.SetTextSize(.03)
    for i, hh in enumerate(hx):
        lat.SetTextColor(itst.clrs[i])
        lat.DrawLatexNDC(.75, .95-.04*i, hh[0].GetName())
    ax, ay = hx[0][0].GetXaxis(), hx[0][0].GetYaxis()
    ay.SetRangeUser(ymin, ymax*1.05)
    ay.SetTitle('Number of CCD electrons')
    ax.SetTitle('X direction, pixels')
    line = r.TLine()
    line.SetLineWidth(1)
    # Drawing constant lines
    for i, f in enumerate(ff):
        f.Draw('same')
        ff2[i].Draw('same')
        line.SetLineColor(itst.clrs[i])
        line.SetLineStyle(1)
        p = f.GetParameters()
        line.DrawLine(p[1]-3*p[2], p[3], p[1]+3*p[2], p[3])
        line.SetLineStyle(2)
        p = ff2[i].GetParameters()
        line.DrawLine(p[1]-3*(p[2]+p[5]), p[6], p[1]+3*(p[2]+p[5]), p[6])
    #
    itst.time_stamp()
    c1.Update()
    # Print results
    # c2 = itst.get_trend_plot(ff, 1, 'mean')
    # c3 = itst.get_trend_plot(ff, 2, 'sigma')
    c4 = itst.get_trend_plot(ff, 0, 'Amplitude')
    c5 = itst.get_trend_plot(ff2, [0, 3], 'Amplitude2')
    # I vs L
    # c_I_vs_L = itst.get_intensity_vs_distance(hx)
    c_I_vs_t = itst.get_intensity_vs_time(hx)
    c_bl_vs_t = itst.get_baseline_vs_time(hx)
    Fout = r.TFile('data/signal_rms.root', 'recreate')
    tout = itst.get_tree(hx, ff, ff2)
    tout.Write()
    Fout.Close()
    raw_input('Press ENTER to continue, please.')
    # c_I_vs_L[0].SaveAs('img/integral_intensity_vs_distance_over_time.png')


if __name__ == '__main__':
    print 'Hi!'
    main()
