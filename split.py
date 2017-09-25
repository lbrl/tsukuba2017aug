#! /usr/bin/env python

# from ROOT import RooFit as rf
# from ROOT import *
import ROOT as r
import sys
import os
# import glob
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
    Fin_name = sys.argv[1]
    Fin = r.TFile(Fin_name)
    if Fin.IsZombie():
        print 'A problem with the file openning.'
        return 1
    name = Fin_name.split('.root')[0]
    name = name.replace('converted', 'splitted')
    iy = 0
    tree = Fin.Get('tree')
    for y in tree:
        Fout = r.TFile('{}_s{}.root'.format(name, iy), 'recreate')
        y.t1.Write('hm')
        Fout.Close()
        iy += 1
    Fin.Close()



if __name__ == '__main__':
    main()
