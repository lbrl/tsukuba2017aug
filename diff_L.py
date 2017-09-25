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
    if '20170828' in name:
        return 950
    return 900


def main():
    file_names = glob.glob('/Users/liberulo/kek/csibpm/data/20170825/hot_pixel/L_foc/*.root')
    # file_names += glob.glob('/Users/liberulo/kek/csibpm/data/20170828/hot_pixel/*.root')
    print '{} files are found.'.format( len(file_names) )
    #
    hx = []
    mean = []
    for fname in file_names:
        hx.append( itst.get_projection(fname, 250, 700, isDraw=False,
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
    Fout = r.TFile('~/kek/csibpm/data/diff_L.root', 'recreate')
    tout = itst.get_tree(hx, ff, ff2)
    print 'The tree contains {} entries.'.format(tout.GetEntries())
    tout.Write()
    Fout.Close()


def mkgrer(t, n):
    x = t.GetV2()
    y = t.GetV1()
    xe = t.GetV4()
    ye = t.GetV3()
    npa = np.array
    for xx in [x, y, xe, ye]:
        xx.SetSize(n)
    gr = r.TGraphErrors(n, npa(x), npa(y), npa(xe), npa(ye))
    return gr

def draw():
    Fin = r.TFile('~/kek/csibpm/data/diff_L.root')
    t = Fin.Get('t')
    # n = t.Draw('a1[0]+a2[0]:L:sqrt(a1[1]**2+a2[1]**2):.1', '', 'goff')
    # n = t.Draw('(a1[0]+a2[0])/time:L:sqrt(a1[1]**2+a2[1]**2)/time:.1', '', 'goff')
    n = t.Draw('a1[0]/time:L:a1[1]/time:.1', '', 'goff')
    # n = t.Draw('(a1[0]+a2[0])/time:L:sqrt(a1[1]**2+a2[1]**2)/time:.1', '!(28<L&&L<30||32<L&&L<34)', 'goff')
    # n = t.Draw('integ[0]:L:integ[1]:.1', '', 'goff')
    # n = t.Draw('a[0]:L:a[1]:.1', '', 'goff')
    gr = mkgrer(t, n)
    c1 = r.TCanvas('c1', 'c1', 600, 600)
    c1.SetGrid()
    r.gStyle.SetOptFit()
    gr.SetMarkerStyle(7)
    gr.Draw('ap')
    gr.GetXaxis().SetTitle('Lens to CsI(Tl) distance, cm')
    gr.GetYaxis().SetTitle('Signal intensity, a.u.')
    gr.GetYaxis().SetTitleOffset(.9)
    ########
    f = r.TF1('f', '[0]/(x-[1])/(x-[1])+[2]', 30, 50)
    f.SetParLimits(0, 0, 1e12)
    f.SetParLimits(1, -20, 20)
    # f.SetParLimits(2, -1e9, 1e9)
    f.SetParameters(4e10, 1, 5e5)
    f.SetParNames('A', 'x_{0}', 'y_{0}')
    # f = r.TF1('f', 'pol1(0)', 30, 50)
    gr.Fit(f, '', 'goff')
    f.Draw('same')
    ########
    c1.Update()
    raw_input()
    c1.SaveAs('~/Desktop/integral_intensity_vs_distance_over_time.png')


def test():
    Fin = r.TFile('~/kek/csibpm/data/diff_L.root', 'read')
    t = Fin.Get('t')
    c1 = r.TCanvas('c1', 'c1', 600, 600)
    c1.Divide(5, 4)
    hh = [r.TH1F('h%d' % i, '', 100, 0, 1600) for i in xrange(50)]
    hh2 = [r.TH2F('hh%d' % i, '', 100, 0, 1600, 100, 0, 1200) for i in xrange(50)]
    ff = [r.TF1('f%d' % i, 'gausn(0)+pol0(3)', 0, 1600) for i in xrange(50)]
    # ff2 = [r.TF1('f2%d' % i, 'gausn(0)+gausn(3)+pol0(6)', 0, 1600) for i in xrange(50)]
    ff2 = [r.TF1('f2%d' % i, itst.my_ggp0, 0, 1600, 7) for i in xrange(50)]
    f2p0 = [r.TF1('fp0_%d' % i, 'pol0(0)', 0, 1600) for i in xrange(50)]
    for i in xrange(50):
        ff[i].SetLineWidth(1)
        ff2[i].SetLineWidth(1)
        ff[i].SetLineColor(r.kCyan)
        ff2[i].SetLineColor(r.kMagenta)
        f2p0[i].SetLineWidth(1)
        f2p0[i].SetLineStyle(2)
        f2p0[i].SetLineColor(r.kMagenta)
    i = 0
    lat = r.TLatex()
    lat.SetTextFont(12)
    lat.SetTextSize(.075)
    for y in t:
        i += 1
        c1.cd(i)
        for j in xrange(100):
            hh[i-1].SetBinContent(j+1, y.arr[j])
            for jj in xrange(100):
                hh2[i-1].SetBinContent(j+1, jj+1, y.arr2[j*100+jj])
        hh[i-1].Draw()
        hh[i-1].GetXaxis().SetNdivisions(4)
        hh[i-1].GetYaxis().SetNdivisions(4)
        hh[i-1].GetXaxis().SetLabelSize(.075)
        hh[i-1].GetYaxis().SetLabelSize(.075)
        ff[i-1].SetParameters(y.a[0], y.m[0], y.s[0], y.c1[0])
        ff[i-1].Draw('same')
        ff2[i-1].SetParameters(y.a1[0], y.m1[0], y.s1[0], y.a2[0], y.m2[0], y.s2[0], y.c2[0])
        ff2[i-1].Draw('same')
        f2p0[i-1].SetParameter(0, y.c2[0])
        f2p0[i-1].Draw('same')
        lat.DrawLatexNDC(.15, .8, '%.2f' % (y.L))
        print y.a[0], y.a1[0], y.a2[0]
        if i > 20:
            break
    c1.cd()
    c1.Update()
    ########################################################
    c2 = r.TCanvas('c2', 'c2', 600, 600)
    c2.Divide(5, 4)
    for j in xrange(i):
        c2.cd(j+1)
        hh2[j].Draw('colz')
    c2.cd()
    c2.Update()
    ########################################################
    raw_input('Press ENTER to continue, please.')
    Fin.Close()


if __name__ == '__main__':
    print 'Hi!'
    if 'draw' in sys.argv:
        draw()
    elif 'test' in sys.argv:
        test()
    else:
        main()
