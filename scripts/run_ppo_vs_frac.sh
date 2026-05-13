#!/bin/bash

# Zeta=0.3 FRAC-PPO 实验 (50 runs)
python main_PPO_stat_box_save.py \
  -runs 50 -epochs 1000 -L_num 200 \
  -zeta 0.3 -beta 1.0 \
  -seed 42 \
  -output_path "data/FRAC_PPO_zeta0.3"

echo "FRAC-PPO (zeta=0.3) 完成！"

# zeta=0.0 标准 PPO 实验 (50 runs)
python main_PPO_stat_box_save.py \
  -runs 50 -epochs 1000 -L_num 200 \
  -zeta 0.0 -beta 0.0 \
  -seed 42 \
  -output_path "data/PPO_standard"

echo "标准 PPO (zeta=0.0) 完成！"
echo "所有实验完成！"
echo "输出目录："
echo "  FRAC-PPO: data/FRAC_PPO_zeta0.3/"
echo "  PPO: data/PPO_standard/"