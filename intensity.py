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
from array import array
# import re
# import matplotlib as ml
# import matplotlib.pyplot as plt
# from PIL import Image

# R.gSystem.Load('libRooFit')

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
    elif '20170817' in fname:
        name += '_20170817'
    elif '20170821' in fname:
        name += '_20170821'
    return name

def get_baseline(hx):
    bl = 0
    x0, x1 = 10, 50
    for i in xrange(x0, x1):
        bl += hx.GetBinContent(i)
    bl /= float( (x1-x0) * 1.1 )
    return bl

def get_baseline_2d(hh, x0=27, y0=867, x1=76, y1=1016):
    bl = 0
    for i in xrange(x0, x1+1):
        for j in xrange(y0, y1+1):
            bl += hh.GetBinContent(i, j)
    bl = bl / (x1-x0+1) / (y1-y0+1)
    return bl

def time_stamp():
    import datetime
    lat = r.TLatex()
    lat.SetTextSize(.03)
    lat.SetTextColor(r.kGray)
    lat.DrawLatexNDC( .01, .01, '{:%Y-%m-%d %H:%M:%S}'.format( datetime.datetime.now() ) )

def get_time(name):
    time = 0.
    if 'sec' in name:
        time = float(name.split('min')[-1].split('sec')[0])/60
    return time + float(name.split('min')[0].split('_')[-1])

def get_distance(name):
    L = -1.
    '''
    if 'L' in name:
        L = float( name.split('L')[-1].split('cm')[0] )
    else:
        if 'cm' in name:
            L = float( name.split('pic')[-1].split('cm')[0] )
    '''
    nam = name.split('/')[-1].split('.root')[0]
    if 'Lm' in nam:
        znak = -1.
    else:
        znak = 1.
    if 'L' in nam:
        na = nam.split('L')[-1]
        if znak < 0:
            na = na[1:]
        if 'cm' in na:
            L = float( na.split('cm')[0] )
        elif 'c' in na:
            L = znak*float( na.split('c')[0] )*.6 + 37.9
    return L

def get_distance_alpha(name):
    d = -1.
    if 'picd' in name:
        d = float( name.split('picd')[-1].split('mm')[0] )
    else:
        print 'get_distance_alpha : problem.', name
    return d

def get_angle(name):
    ang = 90.
    if 'tan' in name:
        nam = name.split('tan')[-1]
        if 'inf' in nam:
            ang = 90
        else:
            na = nam.split('.')[0]
            if 'o' in na:
                n = na.split('o')
                ang = math.atan( float(n[0]) / float(n[1]) ) * 180 / np.pi
            else:
                ang = math.atan( float(na) ) * 180 / np.pi
    return ang

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

clrs = [
        r.kRed,
        r.kBlue,
        r.kGreen,
        r.kCyan,
        r.kMagenta,
        r.kViolet,
        r.kRed+3,
        r.kMagenta+3,
        r.kBlue+3,
        r.kCyan+3,
        r.kGreen+3,
        r.kRed-3,
        r.kMagenta-3,
        r.kBlue-3,
        r.kCyan-3,
        r.kGreen-3,
        r.kRed-1,
        r.kMagenta-1,
        r.kBlue-1,
        r.kCyan-1,
        r.kGreen-1,
        r.kRed-5,
        r.kMagenta-5,
        r.kBlue-5,
        r.kCyan-5,
        r.kGreen-5,
        r.kRed-10,
        r.kMagenta-10,
        r.kBlue-10,
        r.kCyan-10,
        r.kGreen-10,
        r.kGray,
        r.kGray+1,
        r.kGray+2,
        r.kGray+3
        ]
clr_i = 0
def get_projection(fname, y0=600, y1=1100, isDraw=False,
        isRoundAndCenterd=True):
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
    if isRoundAndCenterd:
        down_boring_area(hh, bc0=bl2d)
    if isDraw:
        c1 = r.TCanvas('c1_get_projection', 'c1', 800, 600)
        hh.Draw('colz')
        hh.GetZaxis().SetRangeUser(0, 150)
        c1.Update()
        print fname
        raw_input('Press ENTER to continue, please.')
    hx = hh.ProjectionX('hx_'+get_name(fname), y0, y1)
    set_errors(hx, y1-y0+1, bl)
    global clr_i
    hx.SetLineColor( clrs[clr_i] )
    clr_i += 1
    # bl = get_baseline(hx)
    subtract_baseline(hx, bl)# bl = base line
    return [hx, hh, Fin, bl]

def set_errors(h, l, bl):
    for i in xrange(1, h.GetSize()):
        bc = h.GetBinContent(i)
        Ngamma = (bc-bl) * 2.1 / .223
        if Ngamma > 0:
            sigma_gamma = Ngamma**.5
        else:
            print '{} - {} = {}'.format(bc, bl, bc-bl)
            sigma_gamma = abs(Ngamma)**.5
        sigma_e = sigma_gamma * .223
        sigma_e_ro = 10. * l**.5
        sigma_e_tot = (sigma_e**2 + sigma_e_ro**2)**.5
        # err = ( bc*2.1 )**.5
        # err += 10. * l**.5
        h.SetBinContent(i, bc * 2.1)
        h.SetBinError(i, sigma_e_tot)
        # h.SetBinError(i, err)

my_gp1_4_exposure_xmin = 1600# 1050
my_gp1_4_exposure_xmax = 1600# 1400
def my_gp1_4_exposure(xx, pp):
    ''' 5 parameters '''
    x = xx[0]
    if my_gp1_4_exposure_xmin < x and x < my_gp1_4_exposure_xmax:
        r.TF1.RejectPoint()
        return 0.
    n = pp[0]
    m = pp[1]
    s = pp[2]
    c0 = pp[3]
    c1 = pp[4]
    c2 = pp[5]
    res = 0.3989422804*n/s * math.exp( -((x-m)/s)**2/2 )
    res += c0 + c1*x
    return res
def my_gp2_4_exposure(xx, pp):
    ''' 6 parameters '''
    x = xx[0]
    if my_gp1_4_exposure_xmin < x and x < my_gp1_4_exposure_xmax:
        r.TF1.RejectPoint()
        return 0.
    n = pp[0]
    m = pp[1]
    s = pp[2]
    c0 = pp[3]
    c1 = pp[4]
    c2 = pp[5]
    res = 0.3989422804*n/s * math.exp( -((x-m)/s)**2/2 )
    res += c0 + c1*x + c2*x*x
    return res

def get_gausses(file_names, xmin=200., xmax=1300., mean=750.):
    ff = []
    if isinstance(mean, float) or isinstance(mean, int):
        mea = [mean]*len(file_names)
    elif isinstance(mean, list):
        pass
        mea = mean
    else:
        print 'An erron in get_gausses.'
        return 1
    for i, fname in enumerate(file_names):
        # ff.append( r.TF1('fgp0_'+get_name(fname), 'gausn(0)+pol0(3)', xmin, xmax) )
        # ff.append( r.TF1('fgp0_'+get_name(fname), 'gausn(0)+pol1(3)', xmin, xmax) )
        # ff.append( r.TF1('fgp0_'+get_name(fname), my_gp1_4_exposure, 100, 1600, 5) )
        # ff.append( r.TF1('fgp0_'+get_name(fname), my_gp1_4_exposure, 200, 1300, 5) )
        ff.append( r.TF1('fgp0_'+get_name(fname), my_gp2_4_exposure, 200, 1300, 6) )
        # ff[-1].SetParameters(1e4, mea[i], 100, 200)
        ff[-1].SetParameters(1e4, mea[i], 100, 1e4, .05)
        ff[-1].SetParameters(1e4, mea[i], 100, 1e4, .05, -0.001)
        ff[-1].SetParLimits(0, 0, 1e9)# A
        ff[-1].SetParLimits(1, mea[i]-100, mea[i]+100)# mean
        ff[-1].SetParLimits(2, 50, 400)# sigma
        ff[-1].SetLineColor(clrs[i])
        ff[-1].SetLineWidth(1)
        # ff[-1].SetParNames('A', 'mean', '#sigma', 'c0')
        # ff[-1].SetParNames('A', 'mean', '#sigma', 'c0', 'c1')
        ff[-1].SetParNames('A', 'mean', '#sigma', 'c0', 'c1', 'c2')
    return ff


def my_ggp0(xx, pp):
    ''' 7 parameters '''
    x = xx[0]
    n = pp[0]
    m = pp[1]
    s = pp[2]
    f = pp[3]# fraction
    a = pp[4]# shift
    k = pp[5]# widereness
    c0 = pp[6]# offset
    if f < 0:
        f = 0.
    if f > 1:
        f = 1.
    if s < 0:
        s = 1.e-3
    if n < 0:
        f = 1.
    if k < 1:
        k = 1.
    res = 0.3989422804*n/s*( f*math.exp(-((x-m)/s)**2/2) + (1-f)/k*math.exp(-((x-m-a)/s/k)**2/2) )
    res += c0
    return res

def get_2gausses(file_names, ff1, xmin=200, xmax=1300):
    ff = []
    mmax = np.array([0.])
    mmin = np.array([0.])
    for i, fname in enumerate(file_names):
        ff.append( r.TF1('fggp0_'+get_name(fname), my_ggp0, xmin, xmax, 7) )
        # ff.append( r.TF1('fggp0_'+get_name(fname), 'gausn(0)+gausn(3)+pol0(6)', xmin, xmax) )
        p = ff1[i].GetParameters()
        ff[-1].SetParameters(p[0]/2, p[1], p[2]/2., .8, 0.01, 1.5, p[3])
        ff[-1].SetParNames('N', 'm', 's', 'f', 'a', 'k', 'c0')
        '''
        ff[-1].SetParLimits(0, 0, 1e9)# A1
        # ff[-1].SetParLimits(1, mean-100, mean+100)# m1
        ff1[i].GetParLimits(1, mmin, mmax)
        ff[-1].SetParLimits(1, mmin[0], mmax[0])# m1
        ff[-1].SetParLimits(2, 50, 200)# s1
        ff[-1].SetParLimits(3, 0, 1e9)# A2
        # ff[-1].SetParLimits(4, mean-100, mean+100)# m2
        ff[-1].SetParLimits(4, mmin[0], mmax[0])# m2
        ff[-1].SetParLimits(5, 50, 200)# s2
        ff[-1].SetLineColor(clrs[i])
        ff[-1].SetLineStyle(2)
        ff[-1].SetParNames('A_{1}', 'mean_{1}', '#sigma_{1}',
                'A_{2}', 'mean_{2}', '#sigma_{2}', 'c0')
        '''
    return ff

def get_trend_plot(ff, ip, name):
    gr = r.TGraphErrors()
    for i, f in enumerate(ff):
        if isinstance(ip, int):
            gr.SetPoint(i, get_time(f.GetName()), f.GetParameter(ip))
            gr.SetPointError(i, 0, f.GetParError(ip))
        elif isinstance(ip, list):
            gr.SetPoint(i, get_time(f.GetName()), sum([f.GetParameter(x) for x in ip]))
            err = ( sum([f.GetParError(x)**2 for x in ip]) )**.5
            gr.SetPointError(i, 0, err)
        else:
            print 'The input parameter ip is not integer or list.'
            return 1
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
    #
    c3 = r.TCanvas('c2_hist_'+name, 'hist '+name, 600, 600)
    y = gr.GetY()
    ma, mi = max(y), min(y)
    mami = ma-mi
    h = r.TH1F('hist_'+name, name, 3*len(ff), mi-.5*mami, ma+.5*mami)
    for yy in y:
        h.Fill(yy)
    h.Draw()
    time_stamp()
    c3.Update()
    return [c2, gr, c3, h]

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

def get_intensity_vs_distance(hx):
    x, y, ye = [], [], []
    yerr = np.array([0.])
    for i, h in enumerate(hx):
        name = h[0].GetName()
        x.append(get_distance(name) / get_time(name) )
        # y.append(h[0].Integral(h[0].FindBin(400), h[0].FindBin(1000)))
        y.append(h[0].IntegralAndError(h[0].FindBin(400), h[0].FindBin(1000), yerr))
        ye.append( yerr[0] )
    # gr = r.TGraph(len(x), np.array(x), np.array(y))
    gr = r.TGraphErrors(len(x), np.array(x), np.array(y), np.array([.25]*len(x)), np.array(ye))
    c5 = r.TCanvas('canvas_I_vs_Lot', 'intensity vs distance / t', 600, 600)
    gr.SetMarkerStyle(20)
    gr.Draw('ap')
    gr.GetXaxis().SetTitle('Distance between the foil and lens / time, cm/min')
    gr.GetYaxis().SetTitle('Intensity integral, e^{#minus}')
    gr.GetYaxis().SetTitleOffset(1.3)
    gr.SetTitle('')
    #
    # f = r.TF1('f_pol-1', '[0]/x/x + [1]/x + [2]', 3, 13)
    f = r.TF1('f_pol-1', '[0]/pow(x-[1], 2) + [2]', 3, 13)
    f.SetParameters( 2e7, 2, 0 )
    gr.Fit(f, 'r')
    # gr.Fit('pol1')
    #
    lat = r.TLatex()
    lat.SetTextColor(r.kBlack)
    lat.SetTextSize(.015)
    x = np.array([0.])
    y = np.array([0.])
    gr.SetMarkerStyle(20)
    gr.Draw('ap')
    for i, h in enumerate(hx):
        gr.GetPoint(i, x, y)
        lat.DrawLatex(x[0], y[0], h[0].GetName())
    #
    time_stamp()
    c5.Update()
    return [c5, gr]


def get_tree(hx, ff, ff2):
    t = r.TTree('t', 'intensity')
    time = array('f', [0.])
    d = array('f', [0.])
    date = array('i', [0])
    angle = array('f', [0.])
    L = array('f', [0.])
    integ = array('f', [0., 0.])
    a = array('f', [0., 0.])
    a1 = array('f', [0., 0.])
    a2 = array('f', [0., 0.])
    m = array('f', [0., 0.])
    m1 = array('f', [0., 0.])
    m2 = array('f', [0., 0.])
    s = array('f', [0., 0.])
    s1 = array('f', [0., 0.])
    s2 = array('f', [0., 0.])
    c1_0 = array('f', [0., 0.])
    c1_1 = array('f', [0., 0.])
    f1_lim = array('f', [0., 0.])
    f1_chi = array('f', [0.])
    c2 = array('f', [0., 0.])
    pol1 = array('f', [0., 0.])
    # hbr = r.TH1D('hbr', 'hbr', 1600, 0, 1600)# Histogram BRanch
    hbr = r.TH1D('hbr', 'hbr', 100, 0, 100)# Histogram BRanch
    fbr = r.TF1()
    f2br = r.TF1()
    integ = array('f', [0., 0.])
    arr = array('f', [0.]*100)
    arr2 = array('f', [0.]*10000)
    # t.Branch('hx', 'TH1D', hbr)
    t.Branch('date', date, 'date/I')
    t.Branch('arr', arr, 'arr[100]/F')
    t.Branch('arr2', arr2, 'arr2[10000]/F')
    t.Branch('f', 'TF1', fbr)
    t.Branch('f2', 'TF1', f2br)
    t.Branch('time', time, 'time/F')
    t.Branch('d', d, 'd/F')
    t.Branch('angle', angle, 'angle/F')
    t.Branch('L', L, 'L/F')
    t.Branch('integ', integ, 'integ[2]/F')
    t.Branch('a', a, 'a[2]/F')
    t.Branch('a1', a1, 'a1[2]/F')
    t.Branch('a2', a2, 'a2[2]/F')
    t.Branch('m', m, 'm[2]/F')
    t.Branch('m1', m1, 'm1[2]/F')
    t.Branch('m2', m2, 'm2[2]/F')
    t.Branch('s', s, 's[2]/F')
    t.Branch('s1', s1, 's1[2]/F')
    t.Branch('s2', s2, 's2[2]/F')
    t.Branch('c1_0', c1_0, 'c1_0[2]/F')
    t.Branch('c1_1', c1_1, 'c1_1[2]/F')
    t.Branch('f1_lim', f1_lim, 'f1_lim[2]/F')
    t.Branch('f1_chi', f1_chi, 'f1_chi/F')
    t.Branch('c2', c2, 'c2[2]/F')
    # t.Branch('pol1', pol1, 'pol1[2]/F')
    yerr = np.array([0.])
    xmin, xmax = np.array([0.]), np.array([0.])
    fpol1 = r.TF1('fpol1', 'pol1(0)', 250, 1000)
    for i, h in enumerate(hx):
        # hbr = h[0].Clone()
        name = h[0].GetName()
        ######
        # h500_600 = h[1].ProjectionX(name+'_500_600', 500, 600)
        # h500_600.Fit(fpol1, '', 'goff', 250, 1000)
        # pol1[0], pol1[1] = fpol1.GetParameter(0), fpol1.GetParameter(1)
        ######
        h[1].Rebin2D(16, 12)
        for j in xrange(1, 101):
            arr[j-1] = h[0].GetBinContent(j)
            for jj in xrange(1, 101):
                if (j-1)*100 + jj-1 < 10000:
                    arr2[(j-1)*100 + jj-1] = h[1].GetBinContent(j, jj)
                else:
                    print 'The index %d is out of range.' % ((j-1)*100 + jj-1)
        L[0] = get_distance(name)
        d[0] = get_distance_alpha(name)
        angle[0] = get_angle(name)
        time[0] = get_time(name)
        integ[0] = h[0].IntegralAndError(h[0].FindBin(400), h[0].FindBin(1000), yerr)
        integ[1] = yerr[0]
        p = ff[i].GetParameters()
        pe = ff[i].GetParErrors()
        for j, x in enumerate([a, m, s, c1_0, c1_1]):
            x[0], x[1] = p[j], pe[j]
        ff[i].GetRange(xmin, xmax)
        f1_lim[0], f1_lim[1] = xmin[0], xmax[0]
        f1_chi[0] = ff[i].GetChisquare() / ff[i].GetNDF()
        p = ff2[i].GetParameters()
        pe = ff2[i].GetParErrors()
        for j, x in enumerate([a1, m1, s1, a2, m2, s2, c2]):
            x[0], x[1] = p[j], pe[j]
        # fbr = ff[i]
        # f2br = ff2[i]
        # fbr = ff[i].Clone()
        # f2br = ff2[i].Clone()
        date[0] = int( ff[i].GetName()[-8:] )
        t.Fill()
    return t


def main():
    sett = 'one'
    sett = 'all'
    if sett == 'one':
        file_names = glob.glob('data/2017081?/hot_pixel/*min*40cm2.root')
    elif sett == 'all':
        file_names = glob.glob('data/2017081?/hot_pixel/*min*.root')
        file_names.remove('data/20170817/hot_pixel/5min1pic40cm.root')# light leak
        file_names.remove('data/20170817/hot_pixel/10min1pic40cm.root')# light leak
    else:
        return 1
    #
    hx = []
    for fname in file_names:
        hx.append( get_projection(fname, 400, 800, isDraw=False) )
    for h in hx:
        h[0].Rebin(16)
    ymin = min([x[0].GetMinimum() for x in hx])
    ymax = max([x[0].GetMaximum() for x in hx])
    # Fitting
    ff = get_gausses(file_names)
    for i, f in enumerate(ff):
        hx[i][0].Fit(f, 'r', 'goff')
        # subtract_baseline(hx[i][0], f.GetParameter(3))
        # f.SetParameter(3, 0.)
    ff2 = get_2gausses(file_names, ff)
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
        lat.SetTextColor(clrs[i])
        lat.DrawLatexNDC(.75, .95-.04*i, hh[0].GetName())
    ax, ay = hx[0][0].GetXaxis(), hx[0][0].GetYaxis()
    ay.SetRangeUser(ymin, ymax*1.05)
    for f in ff:
        f.Draw('same')
    for f in ff2:
        f.Draw('same')
    c1.Update()
    # Print results
    c2 = get_trend_plot(ff, 1, 'mean')
    c3 = get_trend_plot(ff, 2, 'sigma')
    c4 = get_trend_plot(ff, 0, 'Amplitude')
    # I vs L
    c_I_vs_L = get_intensity_vs_distance(hx)
    raw_input('Press ENTER to continue, please.')
    c_I_vs_L[0].SaveAs('img/integral_intensity_vs_distance_over_time.png')


if __name__ == '__main__':
    main()
