#! /bin/bash

./pco2root2x2.py data/20170808/raw/am_1cm_csitl_mlr_1adc_1by1_10MHz_texp_10min_4pic_20170808.pcoraw data/20170808/converted/10min4pic38cm.root
./pco2root2x2.py data/20170808/raw/am_1cm_csitl_mlr_1adc_1by1_10MHz_texp_1min_10pic_20170808.pcoraw data/20170808/converted/1min10pic38cm.root
./pco2root2x2.py data/20170808/raw/am_1cm_csitl_mlr_1adc_1by1_10MHz_texp_5min_4pic_20170808.pcoraw data/20170808/converted/5min4pic38cm.root

./pco2root2x2.py data/20170808/raw/am_1cm_csitl_mlr_1adc_1by1_10MHz_texp_1min_1pic_20170808.pcoraw data/20170808/converted/1min1pic38cm.root
./pco2root2x2.py data/20170808/raw/am_1cm_csitl_mlr_1adc_1by1_10MHz_texp_20min_1pic_20170808.pcoraw data/20170808/converted/10min1pic38cm.root
./pco2root2x2.py data/20170808/raw/am_1cm_csitl_mlr_1adc_1by1_10MHz_texp_20min_1pic_20170808_2.pcoraw data/20170808/converted/20min1pic38cm2.root
./pco2root2x2.py data/20170808/raw/am_1cm_csitl_mlr_1adc_1by1_10MHz_texp_40min_1pic_20170808.pcoraw data/20170808/converted/40min1pic38cm.root

echo
echo Merging
echo

./mergepics.py data/20170808/converted/1min10pic38cm.root data/20170808/merged/1min10pic38cm.root -b -q
./mergepics.py data/20170808/converted/5min4pic38cm.root data/20170808/merged/5min4pic38cm.root -b -q
./mergepics.py data/20170808/converted/10min4pic38cm.root data/20170808/merged/10min4pic38cm.root -b -q

echo
echo Remove hot pixels
echo

./remove_hot_pixels.py data/20170808/converted/1min1pic38cm.root data/20170808/hot_pixel/1min1pic38cm.root
./remove_hot_pixels.py data/20170808/converted/10min1pic38cm.root data/20170808/hot_pixel/10min1pic38cm.root
./remove_hot_pixels.py data/20170808/converted/20min1pic38cm2.root data/20170808/hot_pixel/20min1pic38cm2.root
./remove_hot_pixels.py data/20170808/converted/40min1pic38cm.root data/20170808/hot_pixel/40min1pic38cm.root

./remove_hot_pixels.py data/20170808/merged/1min10pic38cm.root data/20170808/hot_pixel/1min10pic38cm.root
./remove_hot_pixels.py data/20170808/merged/5min4pic38cm.root data/20170808/hot_pixel/5min4pic38cm.root
./remove_hot_pixels.py data/20170808/merged/10min4pic38cm.root data/20170808/hot_pixel/10min4pic38cm.root
