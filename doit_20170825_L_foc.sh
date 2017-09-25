#! /bin/bash

# ./pco2root2x2.py ~/kek/csibpm/data/20170825/raw/L_foc/am_4mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_taninf_L0c_20170825.pcoraw ~/kek/csibpm/data/20170825/converted/L_foc/10min1picL0c.root
# ./pco2root2x2.py ~/kek/csibpm/data/20170825/raw/L_foc/am_4mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_taninf_L3c_20170825.pcoraw ~/kek/csibpm/data/20170825/converted/L_foc/10min1picL3c.root
# ./pco2root2x2.py ~/kek/csibpm/data/20170825/raw/L_foc/am_4mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_taninf_L6c_20170825.pcoraw ~/kek/csibpm/data/20170825/converted/L_foc/10min1picL6c.root
# ./pco2root2x2.py ~/kek/csibpm/data/20170825/raw/L_foc/am_4mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_taninf_L12c_20170825.pcoraw ~/kek/csibpm/data/20170825/converted/L_foc/10min1picL12c.root
# ./pco2root2x2.py ~/kek/csibpm/data/20170825/raw/L_foc/am_4mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_taninf_L18c_20170825.pcoraw ~/kek/csibpm/data/20170825/converted/L_foc/10min1picL18c.root
# ./pco2root2x2.py ~/kek/csibpm/data/20170825/raw/L_foc/am_4mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_taninf_L24c_20170825.pcoraw ~/kek/csibpm/data/20170825/converted/L_foc/10min1picL24c.root
# ./pco2root2x2.py ~/kek/csibpm/data/20170825/raw/L_foc/am_4mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_taninf_L15c_20170825.pcoraw ~/kek/csibpm/data/20170825/converted/L_foc/10min1picL15c.root
# ./pco2root2x2.py ~/kek/csibpm/data/20170825/raw/L_foc/am_4mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_taninf_L9c_20170825.pcoraw ~/kek/csibpm/data/20170825/converted/L_foc/10min1picL9c.root
./pco2root2x2.py ~/kek/csibpm/data/20170825/raw/L_foc/am_4mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_taninf_L21c_20170825.pcoraw ~/kek/csibpm/data/20170825/converted/L_foc/10min1picL21c.root
# ./pco2root2x2.py ~/kek/csibpm/data/20170825/raw/L_foc/am_4mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_taninf_L36c_20170825.pcoraw ~/kek/csibpm/data/20170825/converted/L_foc/10min1picL36c.root
# ./pco2root2x2.py ~/kek/csibpm/data/20170825/raw/L_foc/am_4mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_taninf_L30c_20170825.pcoraw ~/kek/csibpm/data/20170825/converted/L_foc/10min1picL30c.root
./pco2root2x2.py ~/kek/csibpm/data/20170825/raw/L_foc/am_4mm_csitl_mlr_1adc_1by1_10MHz_texp_10min_1pic_taninf_Lm18c_20170825.pcoraw ~/kek/csibpm/data/20170825/converted/L_foc/10min1picLm18c.root


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
./remove_hot_pixels.py ~/kek/csibpm/data/20170825/converted/L_foc/*Lm18c*.root
