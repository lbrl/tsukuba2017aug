#! /bin/bash

./pco2root2x2.py data/20170821/raw/am_1cm_csitl_mlr_1adc_1by1_10MHz_texp_5min_5pic_20170821.pcoraw data/20170821/converted/5min5pic39cm.root
./pco2root2x2.py data/20170821/raw/am_1cm_csitl_mlr_1adc_1by1_10MHz_texp_5min_5pic_20170821_2.pcoraw data/20170821/converted/5min5pic39cm2.root
./pco2root2x2.py data/20170821/raw/am_1cm_csitl_mlr_1adc_1by1_10MHz_texp_10min_5pic_20170821.pcoraw data/20170821/converted/10min5pic39cm.root
./pco2root2x2.py data/20170821/raw/am_1cm_csitl_mlr_1adc_1by1_10MHz_texp_10min_5pic_20170821_2.pcoraw data/20170821/converted/10min5pic39cm2.root

echo
echo Merging
echo

# ~/kek/muprof/resolution/new/mergepics.py data/20170821/converted/2min3pic.root data/20170821/merged/2min3pic.root -b -q

echo
echo Splitting
echo

./split.py data/20170821/converted/5min5pic39cm.root
./split.py data/20170821/converted/5min5pic39cm2.root
./split.py data/20170821/converted/10min5pic39cm.root
./split.py data/20170821/converted/10min5pic39cm2.root

echo
echo Remove hot pixels
echo

./remove_hot_pixels.py data/20170821/splitted/5min5pic39cm_s*.root
./remove_hot_pixels.py data/20170821/splitted/5min5pic39cm2_s*.root
./remove_hot_pixels.py data/20170821/splitted/10min5pic39cm_s*.root
./remove_hot_pixels.py data/20170821/splitted/10min5pic39cm2_s*.root
