#! /bin/bash

./pco2root2x2.py data/20170817/raw/am_1cm_csitl_mlr_1adc_1by1_10MHz_texp_5min_1pic_L38cm_20170817_3.pcoraw data/20170817/converted/5min1pic38cm3.root

./pco2root2x2.py data/20170817/raw/am_1cm_csitl_mlr_1adc_1by1_10MHz_texp_5min_1pic_L40cm_20170817.pcoraw data/20170817/converted/5min1pic40cm.root
./pco2root2x2.py data/20170817/raw/am_1cm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_L40cm_20170817.pcoraw data/20170817/converted/10min1pic40cm.root
./pco2root2x2.py data/20170817/raw/am_1cm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_L40cm_20170817_2.pcoraw data/20170817/converted/10min1pic40cm2.root

./pco2root2x2.py data/20170817/raw/am_1cm_csitl_mlr_1adc_1by1_10MHz_texp_5min_1pic_L50cm_20170817.pcoraw data/20170817/converted/5min1pic50cm.root
./pco2root2x2.py data/20170817/raw/am_1cm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_L50cm_20170817.pcoraw data/20170817/converted/10min1pic50cm.root

./pco2root2x2.py data/20170817/raw/am_1cm_csitl_mlr_1adc_1by1_10MHz_texp_5min_1pic_L60cm_20170817.pcoraw data/20170817/converted/5min1pic60cm.root
./pco2root2x2.py data/20170817/raw/am_1cm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_L60cm_20170817.pcoraw data/20170817/converted/10min1pic60cm.root
./pco2root2x2.py data/20170817/raw/am_1cm_csitl_mlr_1adc_1by1_10MHz_texp_15min_1pic_L60cm_20170817.pcoraw data/20170817/converted/15min1pic60cm.root

echo
echo Merging
echo

# ~/kek/muprof/resolution/new/mergepics.py data/20170809/converted/2min3pic.root data/20170809/merged/2min3pic.root -b -q

echo
echo Remove hot pixels
echo

./remove_hot_pixels.py data/20170817/converted/5min1pic38cm3.root data/20170817/hot_pixel/5min1pic38cm3.root

./remove_hot_pixels.py data/20170817/converted/5min1pic40cm.root data/20170817/hot_pixel/5min1pic40cm.root
./remove_hot_pixels.py data/20170817/converted/10min1pic40cm.root data/20170817/hot_pixel/10min1pic40cm.root
./remove_hot_pixels.py data/20170817/converted/10min1pic40cm2.root data/20170817/hot_pixel/10min1pic40cm2.root

./remove_hot_pixels.py data/20170817/converted/5min1pic50cm.root data/20170817/hot_pixel/5min1pic50cm.root
./remove_hot_pixels.py data/20170817/converted/10min1pic50cm.root data/20170817/hot_pixel/10min1pic50cm.root

./remove_hot_pixels.py data/20170817/converted/5min1pic60cm.root data/20170817/hot_pixel/5min1pic60cm.root
./remove_hot_pixels.py data/20170817/converted/10min1pic60cm.root data/20170817/hot_pixel/10min1pic60cm.root
./remove_hot_pixels.py data/20170817/converted/15min1pic60cm.root data/20170817/hot_pixel/15min1pic60cm.root
