#! /bin/bash

./pco2root2x2.py data/20170823/raw/am_16mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_20170823.pcoraw data/20170823/converted/10min1picd16mmL39cm.root
./pco2root2x2.py data/20170823/raw/am_16mm_csitl_mlr_1adc_1by1_10MHz_texp_5min_1pic_20170823.pcoraw data/20170823/converted/5min1picd16mmL39cm.root
./pco2root2x2.py data/20170823/raw/am_17mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_20170823.pcoraw data/20170823/converted/10min1picd17mmL39cm.root
./pco2root2x2.py data/20170823/raw/am_18mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_20170823.pcoraw data/20170823/converted/10min1picd18mmL39cm.root
./pco2root2x2.py data/20170823/raw/am_20mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_20170823.pcoraw data/20170823/converted/10min1picd20mmL39cm.root
./pco2root2x2.py data/20170823/raw/am_21mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_20170823.pcoraw data/20170823/converted/10min1picd21mmL39cm.root
./pco2root2x2.py data/20170823/raw/am_23mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_20170823.pcoraw data/20170823/converted/10min1picd23mmL39cm.root

echo
echo Merging
echo

# ~/kek/muprof/resolution/new/mergepics.py data/20170823/converted/2min3pic.root data/20170823/merged/2min3pic.root -b -q

echo
echo Splitting
echo

# ./split.py data/20170823/converted/10min5pic39cm2.root

echo
echo Remove hot pixels
echo

./remove_hot_pixels.py data/20170823/converted/*.root
