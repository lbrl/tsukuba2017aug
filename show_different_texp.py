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

def time_stamp():
    import datetime
    lat = r.TLatex()
    lat.SetTextSize(.03)
    lat.SetTextColor(r.kGray)
    lat.DrawLatexNDC( .01, .01, '{:%Y-%m-%d %H:%M:%S}'.format( datetime.datetime.now() ) )


def main2():
    file_names = glob.glob('data/20170808/converted/*min*.root')
    #
    Fin1 = r.TFile(file_names[0])
    t1 = Fin1.Get('t1')
    hx1 = t1.ProjectionX('hx_1', 600, 1100)
    #
    Fin2 = r.TFile(file_names[1])
    t2 = Fin2.Get('t1')
    hx2 = t2.ProjectionX('hx_2', 600, 1100)
    #
    Fin3 = r.TFile(file_names[2])
    t3 = Fin3.Get('t1')
    hx3 = t3.ProjectionX('hx_3', 600, 1100)
    #
    Fin4 = r.TFile(file_names[3])
    t4 = Fin4.Get('t1')
    hx4 = t4.ProjectionX('hx_4', 600, 1100)
    #
    Fin5 = r.TFile(file_names[4])
    t5 = Fin5.Get('t1')
    hx5 = t5.ProjectionX('hx_5', 600, 1100)
    #
    hx = [hx1, hx2, hx3, hx4, hx5]
    clrs = [r.kBlue, r.kRed, r.kCyan, r.kMagenta, r.kGreen+2,
            r.kViolet, r.kRed+2, r.kRed+4, r.kRed+6, r.kRed+8,
            r.kGreen, r.kBlue+2, r.kBlue+4, r.kBlue+6, r.kBlue+8]
    for i, h in enumerate(hx):
        h.Rebin(16)
        h.SetLineColor(clrs[i])
    #
    ff = []
    for i in xrange(len(file_names)):
        ff.append( r.TF1('f', 'gausn(0)+pol0(3)', 200, 1400) )
        ff[-1].SetParameters(1e4, 750, 100, 200)
        ff[-1].SetParLimits(1, 650, 850)
        ff[-1].SetParLimits(2, 50, 200)
        ff[-1].SetLineColor(clrs[i])
        ff[-1].SetParNames('A', 'mean', '#sigma', 'c0')
    #
    f2g = r.TF1('f', 'gaus(0)+gaus(3)+pol0(6)', 200, 1400)
    f2g.SetParameters(1e4, 750, 100, 1e4, 750, 100, 200)
    f2g.SetParLimits(1, 650, 850)
    f2g.SetParLimits(2, 50, 200)
    f2g.SetParLimits(4, 650, 850)
    f2g.SetParLimits(5, 50, 200)
    f2g.SetLineColor(r.kBlack)
    #
    c1 = r.TCanvas('c1', 'c1', 800, 600)
    hx4.Draw()
    # hx4.GetYaxis().SetRangeUser(0, hx4.GetMaximum()*1.05)
    hx2.Draw('same')
    hx1.Draw('same')
    hx3.Draw('same')
    hx5.Draw('same')
    #
    gr_m = r.TGraphErrors()
    gr_s = r.TGraphErrors()
    for i, f in enumerate(ff):
        hx[i].Fit(f, 'rl', 'goff')
        f.Draw('same')
        gr_m.SetPoint(i, i+.5, f.GetParameter(1))
        gr_m.SetPointError(i, 0, f.GetParError(1))
        gr_s.SetPoint(i, i+.5, f.GetParameter(2))
        gr_s.SetPointError(i, 0, f.GetParError(2))
    bw, A = hx[3].GetBinWidth(10), ff[3].GetParameter(0)
    print 'bw = {}   A = {}   A / bw = {}'.format(bw, A, A/bw)
    # hx4.Fit(f2g, 'rl', 'goff')
    # f2g.Draw('same')
    lat = r.TLatex()
    for i, name in enumerate(file_names):
        lat.SetTextColor(clrs[i])
        lat.DrawLatexNDC(.6, .8-.05*i, name.split('/')[-1])
    time_stamp()
    c1.Update()
    #
    c2 = r.TCanvas('c2', 'mean', 600, 600)
    lat.SetTextColor(r.kBlack)
    lat.SetTextSize(.03)
    x = np.array([0.])
    y = np.array([0.])
    gr_m.SetMarkerStyle(20)
    gr_m.Draw('ap')
    for i, name in enumerate(file_names):
        gr_m.GetPoint(i, x, y)
        lat.DrawLatex(x[0], y[0], name.split('/')[-1].split('.root')[0])
    time_stamp()
    c2.Update()
    #
    c3 = r.TCanvas('c3', 'sigma', 600, 600)
    gr_s.SetMarkerStyle(20)
    gr_s.Draw('ap')
    for i, name in enumerate(file_names):
        gr_s.GetPoint(i, x, y)
        lat.DrawLatex(x[0], y[0], name.split('/')[-1].split('.root')[0])
    time_stamp()
    c3.Update()
    #
    raw_input('Press ENTER to exit.')


if __name__ == '__main__':
    main2()
