#! /bin/bash

./pco2root2x2.py data/20170809/raw/am_1cm_csitl_mlr_1adc_1by1_10MHz_texp_15min_1pic_20170809.pcoraw data/20170809/converted/15min1pic.root
./pco2root2x2.py data/20170809/raw/am_1cm_csitl_mlr_1adc_1by1_10MHz_texp_20min_1pic_20170809.pcoraw data/20170809/converted/20min1pic.root
./pco2root2x2.py data/20170809/raw/am_1cm_csitl_mlr_1adc_1by1_10MHz_texp_4min_1pic_20170809.pcoraw data/20170809/converted/4min1pic.root
./pco2root2x2.py data/20170809/raw/am_1cm_csitl_mlr_1adc_1by1_10MHz_texp_3min_1pic_20170809.pcoraw data/20170809/converted/3min1pic.root
./pco2root2x2.py data/20170809/raw/am_1cm_csitl_mlr_1adc_1by1_10MHz_texp_2min_3pic_20170809.pcoraw data/20170809/converted/2min3pic.root
./pco2root2x2.py data/20170809/raw/am_1cm_csitl_mlr_1adc_1by1_10MHz_texp_7min30sec_1pic_20170809.pcoraw data/20170809/converted/7min30sec1pic.root

echo
echo Merging
echo

./mergepics.py data/20170809/converted/2min3pic.root data/20170809/merged/2min3pic.root -b -q

echo
echo Remove hot pixels
echo

./remove_hot_pixels.py data/20170809/converted/15min1pic.root data/20170809/hot_pixel/15min1pic.root
./remove_hot_pixels.py data/20170809/converted/20min1pic.root data/20170809/hot_pixel/20min1pic.root
./remove_hot_pixels.py data/20170809/converted/3min1pic.root data/20170809/hot_pixel/3min1pic.root
./remove_hot_pixels.py data/20170809/converted/4min1pic.root data/20170809/hot_pixel/4min1pic.root
./remove_hot_pixels.py data/20170809/converted/7min30sec1pic.root data/20170809/hot_pixel/7min30sec1pic.root

./remove_hot_pixels.py data/20170809/merged/2min3pic.root data/20170809/hot_pixel/2min3pic.root
