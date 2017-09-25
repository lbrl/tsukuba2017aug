#! /bin/bash

./pco2root2x2.py ~/kek/csibpm/data/20170825/raw/am_cu_1mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_taninf_20170825.pcoraw ~/kek/csibpm/data/20170825/converted/10min1picd1mmL38cmtaninfcu.root
./pco2root2x2.py ~/kek/csibpm/data/20170825/raw/am_cu_1mm_csitl_mlr_1adc_1by1_10MHz_texp_20min_1pic_taninf_20170825.pcoraw ~/kek/csibpm/data/20170825/converted/20min1picd1mmL38cmtaninfcu.root
./pco2root2x2.py ~/kek/csibpm/data/20170825/raw/am_cu_1mm_csitl_mlr_1adc_1by1_10MHz_texp_40min_1pic_taninf_20170825.pcoraw ~/kek/csibpm/data/20170825/converted/40min1picd1mmL38cmtaninfcu.root
./pco2root2x2.py ~/kek/csibpm/data/20170825/raw/am_4mm_ruler_3mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_taninf_20170825.pcoraw ~/kek/csibpm/data/20170825/converted/10min1picd7mmL38cmtaninfruler.root


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

./remove_hot_pixels.py ~/kek/csibpm/data/20170825/converted/*.root
