#! /bin/bash

# ./pco2root2x2.py ~/kek/csibpm/data/20170828/raw/am_4mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_taninf_Lm9c_20170828.pcoraw ~/kek/csibpm/data/20170828/converted/10min1picLm9c.root
# ./pco2root2x2.py ~/kek/csibpm/data/20170828/raw/am_4mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_taninf_Lm12c_20170828.pcoraw ~/kek/csibpm/data/20170828/converted/10min1picLm12c.root
# ./pco2root2x2.py ~/kek/csibpm/data/20170828/raw/am_4mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_taninf_Lm16c_20170828.pcoraw ~/kek/csibpm/data/20170828/converted/10min1picLm16c.root
# ./pco2root2x2.py ~/kek/csibpm/data/20170828/raw/am_4mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_taninf_Lm14c_20170828.pcoraw ~/kek/csibpm/data/20170828/converted/10min1picLm14c.root
./pco2root2x2.py ~/kek/csibpm/data/20170828/raw/am_4mm_csitl_mlr_1adc_1by1_10MHz_texp_20min_1pic_taninf_Lm14c_20170828.pcoraw ~/kek/csibpm/data/20170828/converted/20min1picLm14c.root


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

# ./remove_hot_pixels.py ~/kek/csibpm/data/20170825/converted/L_foc/*.root
# ./remove_hot_pixels.py ~/kek/csibpm/data/20170828/converted/*Lm14c*.root
./remove_hot_pixels.py ~/kek/csibpm/data/20170828/converted/*20min*Lm14c*.root
