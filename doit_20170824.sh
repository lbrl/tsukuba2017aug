#! /bin/bash

./pco2root2x2.py data/20170824/raw/am_7mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_taninf_20170824.pcoraw data/20170824/converted/10min1picd7mmL38cmtaninf.root
./pco2root2x2.py data/20170824/raw/am_7mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_tan1_20170824.pcoraw data/20170824/converted/10min1picd7mmL38cmtan1.root
./pco2root2x2.py data/20170824/raw/am_7mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_tan2_20170824.pcoraw data/20170824/converted/10min1picd7mmL38cmtan2.root
./pco2root2x2.py data/20170824/raw/am_7mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_tan1o2_20170824.pcoraw data/20170824/converted/10min1picd7mmL38cmtan1o2.root
./pco2root2x2.py data/20170824/raw/am_7mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_tan3_20170824.pcoraw data/20170824/converted/10min1picd7mmL38cmtan3.root
./pco2root2x2.py data/20170824/raw/am_7mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_tan6o5_20170824.pcoraw data/20170824/converted/10min1picd7mmL38cmtan6o5.root

echo
echo Merging
echo

# ~/kek/muprof/resolution/new/mergepics.py data/20170824/converted/2min3pic.root data/20170824/merged/2min3pic.root -b -q

echo
echo Splitting
echo

# ./split.py data/20170824/converted/10min5pic39cm2.root

echo
echo Remove hot pixels
echo

./remove_hot_pixels.py data/20170824/converted/*.root
