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
    return 800.

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


px_y_min = 650
px_y_max = 1050
def main():
    # file_names = glob.glob('/Users/liberulo/kek/csibpm/data/20170808/hot_pixel/*.root')
    # file_names += glob.glob('/Users/liberulo/kek/csibpm/data/20170809/hot_pixel/*.root')
    file_names = glob.glob('data/20170808/hot_pixel/*.root')
    file_names += glob.glob('data/20170809/hot_pixel/*.root')
    print '{} files are found.'.format( len(file_names) )
    #
    hx = []
    mean = []
    for fname in file_names:
        # hx.append( itst.get_projection(fname, 500, 1100, isDraw=False,
        hx.append( itst.get_projection(fname, px_y_min, px_y_max, isDraw=False,
            isRoundAndCenterd=True) )
            # isRoundAndCenterd=False) )
        mean.append(get_mean(fname))
    for h in hx:
        h[0].Rebin(16)
    ymin = min([x[0].GetMinimum() for x in hx])
    ymax = max([x[0].GetMaximum() for x in hx])
    # Fitting
    ff = itst.get_gausses(file_names, mean=mean)
    for i, f in enumerate(ff):
        print bcolors.HEADER + 'Fit', f.GetName(), bcolors.ENDC
        hx[i][0].Fit(f, 'r', 'goff')
    ff2 = itst.get_2gausses(file_names, ff)
    for i, f in enumerate(ff2):
        hx[i][0].Fit(f, 'r +', 'goff')
    # Tree production
    # Fout = r.TFile('~/kek/csibpm/data/diff_exp_time.root', 'recreate')
    Fout = r.TFile('data/diff_exp_time.root', 'recreate')
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
    gr.SetMarkerStyle(24)
    return gr

def draw():
    # Fin = r.TFile('~/kek/csibpm/data/diff_exp_time.root')
    Fin = r.TFile('data/diff_exp_time.root')
    t = Fin.Get('t')
    # n = t.Draw('a1[0]/time:time:a1[1]/time:0.', '', 'goff')
    n = t.Draw('a[0]/time:time:a[1]/time:0.', '', 'goff')
    # n = t.Draw('integ[0]/time:time:integ[1]/time:0.', '', 'goff')
    gr = mkgrer(t, n)
    gr.SetTitle('')
    #################################################################
    # 2017-08-08 data #
    n20170808 = t.Draw('a[0]/time:time:a[1]/time:0.', 'date==20170808', 'goff')
    gr20170808 = mkgrer(t, n20170808)
    gr20170808.SetMarkerColor(r.kRed)
    gr20170808.SetLineColor(r.kRed)
    #################################################################
    # 2017-08-09 data #
    n20170809 = t.Draw('a[0]/time:time:a[1]/time:0.', 'date==20170809', 'goff')
    gr20170809 = mkgrer(t, n20170809)
    gr20170809.SetMarkerColor(r.kBlue)
    gr20170809.SetLineColor(r.kBlue)
    #################################################################
    c1 = r.TCanvas('c1', 'c1', 800, 800)
    c1.SetGrid()
    # r.gStyle.SetOptFit()
    gr.Draw('ap')
    gr.GetXaxis().SetTitle('Exposure time, min')
    gr.GetYaxis().SetTitle('Signal intensity, e^{#minus} / min')
    gr.GetYaxis().SetTitleOffset(1.5)
    gr20170808.Draw('p same')
    gr20170809.Draw('p same')
    #################################################################
    f = r.TF1('f', '[0]', 0, 50)
    f.SetLineColor(r.kBlack)
    f.SetParameter(0, 4)
    f.SetParName(0, 'k')
    f20170808 = r.TF1('f20170808', '[0]', 0, 50)
    f20170808.SetLineColor(r.kRed)
    f20170808.SetParName(0, 'k')
    f20170809 = r.TF1('f20170809', '[0]', 0, 50)
    f20170809.SetLineColor(r.kBlue)
    f20170809.SetParName(0, 'k')
    # f = r.TF1('f', 'pol1(0)', 30, 50)
    gr.Fit(f, '', 'goff')
    f.Draw('same')
    gr20170808.Fit(f20170808, '', 'goff')
    f20170808.Draw('same')
    gr20170809.Fit(f20170809, '', 'goff')
    f20170809.Draw('same')
    #################################################################
    lat = r.TLatex()
    lat.SetTextFont(12)
    lat.SetTextSize(.03)
    lat.DrawLatex(22, f.GetParameter(0)+25e3, '2017-08-08/09,  %.3g  e^{#minus} / min' % f.GetParameter(0) )
    lat.SetTextColor(r.kRed)
    lat.DrawLatex(22, f20170808.GetParameter(0)-75e3, '2017-08-08,  %.3g  e^{#minus} / min' % f20170808.GetParameter(0) )
    lat.SetTextColor(r.kBlue)
    lat.DrawLatex(22, f20170809.GetParameter(0)-75e3, '2017-08-09,  %.3g  e^{#minus} / min' % f20170809.GetParameter(0) )
    #################################################################
    c1.Update()
    raw_input()
    ############
    # baseline #
    ############
    c2 = r.TCanvas('c2', 'c2', 600, 600)
    n1 = t.Draw('c1_1[0]*(f1_lim[1]**2-f1_lim[0]**2)+c1_0[0]*(f1_lim[1]-f1_lim[0]):time:((f1_lim[1]**2-f1_lim[0]**2)**2 + (f1_lim[1]-f1_lim[0])**2)**.5:0.',
            'c1_1[0]*(f1_lim[1]**2-f1_lim[0]**2)+c1_0[0]*(f1_lim[1]-f1_lim[0]) < 780e6', 'goff')
    gr2 = mkgrer(t, n1)
    gr2.Draw('ap')
    gr2.GetXaxis().SetTitle('Exposure time, min')
    gr2.GetYaxis().SetTitle('Background intensity, e^{#minus} / min')
    f2 = r.TF1('f2', '[0]+[1]*x', 0, 50)
    f2.SetParameters(710, 1)
    gr2.Fit(f2, '', 'goff')
    f2.Draw('same')
    c2.Update()
    ############
    raw_input()
    c1.SaveAs('~/Desktop/integral_intensity_vs_exposure_time.png')


def test():
    # Fin = r.TFile('~/kek/csibpm/data/diff_exp_time.root')
    Fin = r.TFile('data/diff_exp_time.root')
    t = Fin.Get('t')
    c1 = r.TCanvas('c1', 'c1', 600, 600)
    c1.Divide(4, 4)
    hh = [r.TH1F('h%d' % i, '', 100, 0, 1600) for i in xrange(50)]
    hh2 = [r.TH2F('hh%d' % i, '', 100, 0, 1600, 100, 0, 1200) for i in xrange(50)]
    ff = [r.TF1('f%d' % i, 'gausn(0)+pol1(3)', 0, 1600) for i in xrange(50)]
    # ff2 = [r.TF1('f2%d' % i, 'gausn(0)+gausn(3)+pol0(6)', 0, 1600) for i in xrange(50)]
    ff2 = [r.TF1('f2%d' % i, itst.my_ggp0, 0, 1600, 7) for i in xrange(50)]
    f2p0 = [r.TF1('fp0_%d' % i, 'pol0(0)', 0, 1600) for i in xrange(50)]
    fp1 = [r.TF1('fp1_%d' % i, 'pol1(0)', 0, 1600) for i in xrange(50)]
    fgp1 = [r.TF1('fgp1_%d' % i, 'gaus(0)+pol1(3)', 0, 1600) for i in xrange(50)]
    for i in xrange(50):
        ff[i].SetLineWidth(2)
        ff2[i].SetLineWidth(1)
        ff[i].SetLineColor(r.kCyan)
        fp1[i].SetLineWidth(1)
        fp1[i].SetLineStyle(2)
        fp1[i].SetLineColor(r.kCyan)
        ff2[i].SetLineColor(r.kMagenta)
        f2p0[i].SetLineWidth(1)
        f2p0[i].SetLineStyle(2)
        f2p0[i].SetLineColor(r.kMagenta)
    i = 0
    lat = r.TLatex()
    lat.SetTextFont(12)
    lat.SetTextSize(.075)
    line = r.TLine()
    line.SetLineColor(r.kRed)
    line.SetLineWidth(2)
    r.gStyle.SetOptFit()
    for y in t:
        i += 1
        c1.cd(i)
        for j in xrange(100):
            hh[i-1].SetBinContent(j+1, y.arr[j])
            for jj in xrange(100):
                hh2[i-1].SetBinContent(j+1, jj+1, y.arr2[j*100+jj])
        hh[i-1].Draw('e')
        ##############
        # fgp1[i-1].SetParameters(y.a[0], y.m[0], y.s[0], y.c1_0[0], y.c1_1[0])
        # hh[i-1].Fit(fgp1[i-1])
        ##############
        hh[i-1].GetXaxis().SetNdivisions(4)
        hh[i-1].GetYaxis().SetNdivisions(4)
        hh[i-1].GetXaxis().SetLabelSize(.075)
        hh[i-1].GetYaxis().SetLabelSize(.075)
        ff[i-1].SetParameters(y.a[0], y.m[0], y.s[0], y.c1_0[0], y.c1_1[0])
        ff[i-1].SetRange(y.f1_lim[0], y.f1_lim[1])
        ff[i-1].Draw('same')
        ff2[i-1].SetParameters(y.a1[0], y.m1[0], y.s1[0], y.a2[0], y.m2[0], y.s2[0], y.c2[0])
        ff2[i-1].Draw('same')
        f2p0[i-1].SetParameter(0, y.c2[0])
        f2p0[i-1].Draw('same')
        fp1[i-1].SetParameters(y.c1_0[0], y.c1_1[0])
        fp1[i-1].SetRange(y.f1_lim[0], y.f1_lim[1])
        fp1[i-1].Draw('same')
        print y.a[0], y.a1[0], y.a2[0]
        ########
        line.DrawLine(itst.my_gp1_4_exposure_xmin, hh[i-1].GetMinimum(), itst.my_gp1_4_exposure_xmin, hh[i-1].GetMaximum())
        line.DrawLine(itst.my_gp1_4_exposure_xmax, hh[i-1].GetMinimum(), itst.my_gp1_4_exposure_xmax, hh[i-1].GetMaximum())
        ########
        lat.SetTextColor(r.kBlack)
        lat.DrawLatexNDC(.12, .80, '%.1f min' % (y.time))
        lat.SetTextColor(r.kBlue)
        lat.DrawLatexNDC(.12, .70, '#chi^{2}/NDF = %.3f' % y.f1_chi )
        lat.DrawLatexNDC(.12, .60, 'N = %.2g #pm %.2g' % (y.a[0], y.a[1]) )
        lat.DrawLatexNDC(.12, .50, '  = %.2f %%' % (100*y.a[1]/y.a[0]) )
        if i > 20:
            break
    c1.cd()
    c1.Update()
    ########################################################
    c2 = r.TCanvas('c2', 'c2', 600, 600)
    c2.Divide(4, 4)
    for j in xrange(i):
        c2.cd(j+1)
        hh2[j].Draw('colz')
        hh2[j].GetYaxis().SetRangeUser(400, 1100)
        line.DrawLine(0, px_y_min, 1600, px_y_min)
        line.DrawLine(0, px_y_max, 1600, px_y_max)
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
