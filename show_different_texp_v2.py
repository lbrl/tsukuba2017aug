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


def get_name(fname):
    fnam = fname.rstrip('\n').split('/')
    name = fnam[-1].split('.root')[0]
    if 'hot_pixel' in fname:
        name = 'hot_' + name
    elif 'merged' in fname:
        name = 'mrgd_' + name
    elif 'converted' in fname:
        name = 'cnvrtd_' + name
    if '20170808' in fname:
        name += '_20170808'
    elif '20170809' in fname:
        name += '_20170809'
    return name


def get_baseline(hx):
    bl = 0
    for i in xrange(1, 101):
        bl += hx.GetBinContent(i)
    bl /= 100.
    return bl


def get_baseline_2d(hh, x0=27, y0=867, x1=76, y1=1016):
    bl = 0
    for i in xrange(x0, x1+1):
        for j in xrange(y0, y1+1):
            bl += hh.GetBinContent(i, j)
    bl = bl / (x1-x0+1) / (y1-y0+1)
    return bl


def subtract_baseline(hx, bl):
    for i in xrange(0, 1602):
        bc = hx.GetBinContent(i)# bc = bin content
        hx.SetBinContent(i, bc-bl)


def down_boring_area(h, x=737, y=595, r=580, bc0=0):
    nx, ny = 1600, 1200
    rr = r**2
    for i in xrange(1, nx+1):
        for j in xrange(1, ny+1):
            if (i-x)**2+(j-y)**2 > rr:
                h.SetBinContent(i, j, bc0)


def get_projection(fname, y0=600, y1=1100, isDraw=False):
    Fin = r.TFile(fname)
    if 'converted' in fname:
        hname = 't1'
    elif 'merged' in fname:
        hname = 'hm'
    elif 'hot_pixel':
        hname = 'hh'
    else:
        print 'The histogram stage is unknown. Use the default name "t1".'
        hname = 't1'
    hh = Fin.Get(hname)
    hx0 = hh.ProjectionX('hx_'+get_name(fname)+'_tmp', y0, y1)
    bl = get_baseline(hx0)
    bl2d = get_baseline_2d(hh, 400, 200, 600, 400)
    down_boring_area(hh, bc0=bl2d)
    if isDraw:
        c1 = r.TCanvas('c1_get_projection', 'c1', 800, 600)
        hh.Draw('colz')
        hh.GetZaxis().SetRangeUser(0, 150)
        c1.Update()
        raw_input('Press ENTER to continue, please.')
    hx = hh.ProjectionX('hx_'+get_name(fname), y0, y1)
    # bl = get_baseline(hx)
    subtract_baseline(hx, bl)# bl = base line
    return [hx, hh, Fin, bl]


def get_gausses(file_names):
    ff = []
    for i, fname in enumerate(file_names):
        ff.append( r.TF1('fgp0_'+get_name(fname), 'gausn(0)+pol0(3)', 100, 1400) )
        ff[-1].SetParameters(1e4, 750, 100, 200)
        ff[-1].SetParLimits(1, 650, 850)
        ff[-1].SetParLimits(2, 50, 200)
        # ff[-1].SetLineColor(clrs[i])
        ff[-1].SetParNames('A', 'mean', '#sigma', 'c0')
    return ff

def get_2gausses(file_names, ff1):
    ff = []
    for i, fname in enumerate(file_names):
        ff.append( r.TF1('fggp0_'+get_name(fname), 'gausn(0)+gaus(3)+pol0(6)', 100, 1400) )
        p = ff1[i].GetParameters()
        ff[-1].SetParameters(p[0]/2, p[1], p[2]/2., p[0]/2, p[1], p[2], p[3])
        ff[-1].SetParLimits(1, 650, 850)
        ff[-1].SetParLimits(2, 50, 200)
        ff[-1].SetParLimits(4, 650, 850)
        ff[-1].SetParLimits(5, 50, 200)
        # ff[-1].SetLineColor(clrs[i])
        ff[-1].SetParNames('A_{1}', 'mean_{1}', '#sigma_{1}',
                'A_{2}', 'mean_{2}', '#sigma_{2}', 'c0')
    return ff

def get_trend_plot(ff, ip, name):
    gr = r.TGraphErrors()
    for i, f in enumerate(ff):
        gr.SetPoint(i, get_time(f.GetName()), f.GetParameter(ip))
        gr.SetPointError(i, 0, f.GetParError(ip))
    c2 = r.TCanvas('c2'+name, name, 600, 600)
    lat = r.TLatex()
    lat.SetTextColor(r.kBlack)
    lat.SetTextSize(.015)
    x = np.array([0.])
    y = np.array([0.])
    gr.SetMarkerStyle(20)
    gr.Draw('ap')
    for i, f in enumerate(ff):
        gr.GetPoint(i, x, y)
        lat.DrawLatex(x[0], y[0], f.GetName())
    time_stamp()
    c2.Update()
    return [c2, gr]


def get_time(name):
    time = 0.
    if 'sec' in name:
        time = float(name.split('min')[-1].split('sec')[0])/60
    return time + float(name.split('min')[0].split('_')[-1])


def get_intensity_vs_time(hx):
    x, y, ye = [], [], []
    yerr = np.array([0.])
    for i, h in enumerate(hx):
        x.append(get_time(h[0].GetName()))
        # y.append(h[0].Integral(h[0].FindBin(200), h[0].FindBin(1200)))
        y.append(h[0].IntegralAndError(h[0].FindBin(400), h[0].FindBin(1000), yerr))
        ye.append( yerr[0] )
    # gr = r.TGraph(len(x), np.array(x), np.array(y))
    gr = r.TGraphErrors(len(x), np.array(x), np.array(y), np.array([.0]*len(x)), np.array(ye))
    c5 = r.TCanvas('c5_I_vs_t', 'intensity vs time', 600, 600)
    gr.SetMarkerStyle(20)
    gr.Draw('ap')
    gr.GetXaxis().SetTitle(r'Exposure time #tau_{exp}, min')
    gr.GetYaxis().SetTitle('Intensity integral, CCD counts')
    gr.GetXaxis().SetTitleOffset(1.1)
    gr.GetYaxis().SetTitleOffset(1.5)
    gr.SetTitle('')
    f = r.TF1('f_p1', '[0]+x*[1]', .5, 40.5)
    f.SetParameters(-6e4, 1e5)
    gr.Fit(f, 'r')
    time_stamp()
    c5.Update()
    return [c5, gr]

def get_baseline_vs_time(hx):
    x, y, = [], []
    for i, h in enumerate(hx):
        x.append(get_time(h[0].GetName()))
        y.append(h[3])
    gr = r.TGraph(len(x), np.array(x), np.array(y))
    c5 = r.TCanvas('c6_baseline_vs_t', 'baseline vs time', 600, 600)
    gr.SetMarkerStyle(20)
    gr.Draw('ap')
    gr.Fit('pol1')
    time_stamp()
    c5.Update()
    return [c5, gr]


def main():
    # r.gStyle.SetOptFit()
    #
    file_names = glob.glob('data/2017080?/hot_pixel/*min*.root')
    #
    hx = []
    for fname in file_names:
        hx.append( get_projection(fname, isDraw=False) )
        # hx.append( get_projection(fname, 850, 900, isDraw=False) )
    # print hx
    #
    for h in hx:
        h[0].Rebin(16)
    ymin = min([x[0].GetMinimum() for x in hx])
    ymax = max([x[0].GetMaximum() for x in hx])
    # Fitting
    ff = get_gausses(file_names)
    ff2 = get_2gausses(file_names, ff)
    for i, f in enumerate(ff):
        hx[i][0].Fit(f, 'r', 'goff')
        # subtract_baseline(hx[i][0], f.GetParameter(3))
        # f.SetParameter(3, 0.)
    # Drawing
    c1 = r.TCanvas('c1', 'x projections', 800, 600)
    hx[0][0].Draw()
    for h in hx[1:]:
        h[0].Draw('same')
    ax, ay = hx[0][0].GetXaxis(), hx[0][0].GetYaxis()
    ay.SetRangeUser(ymin, ymax*1.05)
    for f in ff:
        f.Draw('same')
    c1.Update()
    # Print results
    c2 = get_trend_plot(ff, 1, 'mean')
    c3 = get_trend_plot(ff, 2, 'sigma')
    c4 = get_trend_plot(ff, 0, 'Amplitude')
    # Intensity vs exposure time
    c5 = get_intensity_vs_time(hx)
    c6 = get_baseline_vs_time(hx)
    #
    raw_input()
    c5[0].SaveAs('img/intensity_vs_exposure_time.png')
    c4[0].SaveAs('img/gaus_amplitude_vs_time.png')
    return 0
    ################################


if __name__ == '__main__':
    main()
