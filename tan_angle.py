#! /usr/bin/env python

# from ROOT import RooFit as rf
# from ROOT import *
# import ROOT as r
import sys
import os
import glob
import math
# import datetime
import numpy as np
# from array import array
# import re
# import matplotlib as ml
# import matplotlib.pyplot as plt
# from PIL import Image

# R.gSystem.Load('libRooFit')


def main():
    for i in xrange(0, 10):
        if i != 0:
            print '%8d ' % i,
        else:
            print ' '*9,
        for j in xrange(1, 10):
            if i == 0:
                print '   %d    ' % j,
            else:
                x = 180 / np.pi * math.atan( float(i) / j )
                print '%4.4f ' % x,
        print


if __name__ == '__main__':
    main()
