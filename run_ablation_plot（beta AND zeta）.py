import os
import subprocess
import glob
import json
import matplotlib.pyplot as plt
import numpy as np  # 添加这行修复NameError

# === 实验配置 ===
beta_list = [0.1, 0.25, 0.5, 1.0, 2.5, 5.0]  # 新增：beta值列表
zeta_list = [0.01, 0.1, 0.3, 0.5, 0.7, 1.0]

# 其他固定参数
runs = 1 
epochs = 1000
L_num = 200
python_script = "main_PPO_stat_box_save.py"

# 存储 JSON 文件路径的列表
data_files = []

print("=== 开始运行 Beta 消融实验（6个fixed_beta值） ===")

# 外层循环：遍历所有beta值
for fixed_beta in beta_list:
    print(f"\n=== Beta组 {fixed_beta} 开始 ===")
    
    # 内层循环：每个beta下运行所有zeta
    for zeta in zeta_list:
        print(f">>> 正在运行 beta={fixed_beta}, zeta={zeta} ...")
        
        current_seed = np.random.randint(1, 100000)
        
        cmd = [
            "python", python_script,
            "-zeta", str(zeta),
            "-beta", str(fixed_beta),  # 使用当前fixed_beta
            "-runs", str(runs),
            "-epochs", str(epochs),
            "-L_num", str(L_num),
            "-seed", str(current_seed),
        ]
        
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running beta={fixed_beta}, zeta={zeta}: {e}")
            continue
        
        # 搜索当前组合的输出目录
        search_pattern = f"data/PPO_stat_box_*_zeta_{zeta}_beta_{fixed_beta}"
        dirs = sorted(glob.glob(search_pattern), key=os.path.getmtime)
        
        if dirs:
            latest_dir = dirs[-1]
            json_file = os.path.join(latest_dir, "final_fractions_data.json")
            if os.path.exists(json_file):
                data_files.append((fixed_beta, zeta, json_file))  # 记录beta, zeta, 文件路径
                print(f"  [Success] beta={fixed_beta}, zeta={zeta}: {json_file}")
            else:
                print(f"  [Warning] 未找到数据文件: {json_file}")
        else:
            print(f"  [Error] 未找到输出目录: {search_pattern}")

print("\n=== 所有36个实验运行结束，开始绘图 ===")

# 绘图部分（修改标签显示beta值）
plt.figure(figsize=(10, 8))
markers = ['o', 's', '^', 'D', 'v', 'p', '*', 'X']
colors = plt.cm.viridis(np.linspace(0, 0.9, max(len(data_files), 1)))

for i, (fixed_beta, zeta, file_path) in enumerate(data_files):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    r_values = data['r_values']
    c_means = data['C_means']
    
    plt.plot(
        r_values, c_means,
        marker=markers[i % len(markers)],
        color=colors[i],
        markersize=8,
        markerfacecolor='none',
        markeredgewidth=1.5,
        linewidth=2,
        label=f'$\\beta={fixed_beta}$ (zeta={zeta})$'
    )

plt.xlabel('r', fontsize=14)
plt.ylabel('Fractions', fontsize=14)
plt.ylim(-0.05, 1.05)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=10, loc='lower right')  # 缩小字体适应更多标签
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

out_png = 'Ablation_Beta_Result.png'
plt.savefig(out_png, dpi=300, bbox_inches='tight')
print(f"绘图完成！图片已保存为: {out_png}")