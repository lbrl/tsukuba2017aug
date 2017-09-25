#! /usr/bin/env python

# from ROOT import RooFit as rf
# from ROOT import *
# import ROOT as r
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


def main():
    t = np.array([1., 5., 10., 20., 40.])# minutes
    t = np.array([1., 5., 10.])# minutes
    I = 3.7e6#4.e6# Bq - decays per second
    eps = .3# geometrical efficiency
    dE = .75# energy loss in the CsI(Tl) foil
    # geom = (43./2)**2 / (4*380**2)# geometrical light collection efficiency
    geom = 7.4**2 / (4*450**2)# geometrical light collection efficiency
    N_alpha = I*eps*t*60# The number of particles hit the CsI(Tl) foil.
    E = N_alpha * dE# Total energy deposition.
    N_ph = E * 10000. / 2.# The number of photons, light yield considering Birks' law.
    N_ph_on_cam = N_ph * geom# The number of photons which reach the CCD sensor.
    qe = .223# transmission and quantum efficiency
    N_det_ph = N_ph_on_cam * qe# The number of detected photons. It is equavalent to the signal charge - number of electrons.
    k_adc2e = 2.1# e^- / count
    k_e2adc = 1/k_adc2e# count / e^-
    N_e_sig = N_det_ph
    N_adc_sig = N_e_sig * k_e2adc
    d_img = 300# diameter of the signal area in pixels
    N_e_rms = 10. * np.pi * d_img**2 / 4
    np.set_printoptions(precision=1)
    print 'The geometrical efficiency is {}.'.format( geom )
    print 't', t
    print 'N_alpha', N_alpha
    print 'E', E
    # print 'N_e_sig', N_e_sig
    print 'N_e_sig',
    for x in N_e_sig:
        print '%.3g' % x,
    print
    print 'N_e_rms', N_e_rms
    print 'N_e_sig / N_e_rms', N_e_sig / N_e_rms
    print 'N_adc_sig', N_adc_sig



if __name__ == '__main__':
    main()
