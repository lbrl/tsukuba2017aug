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


def main():
    # file_names = glob.glob('/Users/liberulo/kek/csibpm/data/20170808/hot_pixel/*.root')
    # file_names += glob.glob('/Users/liberulo/kek/csibpm/data/20170809/hot_pixel/*.root')
    file_names = glob.glob('data/20170821/hot_pixel/*_s*.root')
    print '{} files are found.'.format( len(file_names) )
    #
    hx = []
    mean = []
    for fname in file_names:
        # hx.append( itst.get_projection(fname, 500, 1100, isDraw=False,
        hx.append( itst.get_projection(fname, 550, 800, isDraw=False,
            # isRoundAndCenterd=True) )
            isRoundAndCenterd=False) )
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
    Fout = r.TFile('data/stat_error.root', 'recreate')
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
    Fin = r.TFile('data/stat_error.root')
    t = Fin.Get('t')
    c1 = r.TCanvas('c1', 'c1', 2*750, 750)
    c1.Divide(4, 2)
    ############
    t.Draw('a[0]>>h_a_5()', 'time==5', 'goff')
    t.Draw('a[1]>>h_ae_5()', 'time==5', 'goff')
    t.Draw('a[0]>>h_a_10()', 'time==10', 'goff')
    t.Draw('a[1]>>h_ae_10()', 'time==10', 'goff')
    h_a_5 = r.gDirectory.Get('h_a_5')
    h_ae_5 = r.gDirectory.Get('h_ae_5')
    h_a_10 = r.gDirectory.Get('h_a_10')
    h_ae_10 = r.gDirectory.Get('h_ae_10')
    ############
    t.Draw('a1[0]+a2[0]>>h_aa_5()', 'time==5', 'goff')
    t.Draw('(a1[1]**2+a2[1]**2)**.5>>h_aae_5()', 'time==5', 'goff')
    t.Draw('a1[0]+a2[0]>>h_aa_10()', 'time==10', 'goff')
    t.Draw('(a1[1]**2+a2[1]**2)**.5>>h_aae_10()', 'time==10', 'goff')
    h_aa_5 = r.gDirectory.Get('h_aa_5')
    h_aae_5 = r.gDirectory.Get('h_aae_5')
    h_aa_10 = r.gDirectory.Get('h_aa_10')
    h_aae_10 = r.gDirectory.Get('h_aae_10')
    ############
    r.gStyle.SetStatX(.99)
    r.gStyle.SetStatY(.99)
    r.gStyle.SetStatW(.4)
    r.gStyle.SetStatH(.4)
    ############
    c1.cd(1)
    h_a_5.Draw()
    c1.cd(2)
    h_ae_5.Draw()
    c1.cd(3)
    h_a_10.Draw()
    c1.cd(4)
    h_ae_10.Draw()
    ############
    c1.cd(5)
    h_aa_5.Draw()
    c1.cd(6)
    h_aae_5.Draw()
    c1.cd(7)
    h_aa_10.Draw()
    c1.cd(8)
    h_aae_10.Draw()
    ############
    ha = [h_a_5, h_aa_5, h_a_10, h_aa_10]
    he = [h_ae_5, h_aae_5, h_ae_10, h_aae_10]
    for h in ha:
        h.GetXaxis().SetTitle('Signal intensity I, e^{#minus}')
    for h in he:
        h.GetXaxis().SetTitle('Signal intensity error #sigma_{I}, e^{#minus}')
    lat = r.TLatex()
    for i, h in enumerate(ha+he):
        c1.cd(i+1)
        if '10' in h.GetTitle():
            lat.DrawLatexNDC(.3, .92, 't_{exp} = 10 min')
        else:
            lat.DrawLatexNDC(.3, .92, 't_{exp} = 5 min')
        h.SetTitle('')
        h.GetYaxis().SetTitle('# of pictures')
        h.SetFillStyle(1001)
        h.SetFillColor(r.kBlue)
        h.GetXaxis().SetTitleSize(.05)
        h.GetYaxis().SetTitleSize(.05)
        h.GetXaxis().SetTitleOffset(.75)
        h.GetYaxis().SetTitleOffset(.85)
    ############
    print '%0.3g\t%0.3g\t%0.3f' % (h_a_5.GetRMS(), h_ae_5.GetMean(), h_a_5.GetRMS()/h_ae_5.GetMean())
    print '%0.3g\t%0.3g\t%0.3f' % (h_aa_5.GetRMS(), h_aae_5.GetMean(), h_aa_5.GetRMS()/h_aae_5.GetMean())
    print '%0.3g\t%0.3g\t%0.3f' % (h_a_10.GetRMS(), h_ae_10.GetMean(), h_a_10.GetRMS()/h_ae_10.GetMean())
    print '%0.3g\t%0.3g\t%0.3f' % (h_aa_10.GetRMS(), h_aae_10.GetMean(), h_aa_10.GetRMS()/h_aae_10.GetMean())
    ############
    c1.Update()
    raw_input()
    # c1.SaveAs('~/Desktop/compare_stat_errors.png')
    c1.SaveAs('~/compare_stat_errors.png')


def test():
    # Fin = r.TFile('~/kek/csibpm/data/diff_exp_time.root')
    Fin = r.TFile('data/stat_error.root')
    t = Fin.Get('t')
    c1 = r.TCanvas('c1', 'c1', 600, 600)
    c1.Divide(5, 4)
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
        fgp1[i-1].SetParameters(y.a[0], y.m[0], y.s[0], y.c1_0[0], y.c1_1[0])
        hh[i-1].Fit(fgp1[i-1])
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
        lat.SetTextColor(r.kBlack)
        lat.DrawLatexNDC(.12, .80, '%.1f min' % (y.time))
        lat.SetTextColor(r.kBlue)
        lat.DrawLatexNDC(.12, .70, '#chi^{2}/NDF = %.3f' % y.f1_chi )
        lat.DrawLatexNDC(.12, .60, 'N = %.2g #pm %.2g' % (y.a[0], y.a[1]) )
        lat.DrawLatexNDC(.12, .50, '  = %.2f %%' % (y.a[1]/y.a[0]*100) )
        lat.SetTextColor(r.kRed)
        lat.DrawLatexNDC(.12, .40, 'N = %.2g #pm %.2g' % (y.a1[0]+y.a2[0], (y.a1[1]**2+y.a2[1]**2)**.5) )
        lat.DrawLatexNDC(.12, .30, '  = %.2f %%' % (100*(y.a1[1]**2+y.a2[1]**2)**.5 / (y.a1[0]+y.a2[0])) )
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
        hh2[j].GetYaxis().SetRangeUser(400, 1100)
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
