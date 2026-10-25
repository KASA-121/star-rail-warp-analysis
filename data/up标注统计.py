import csv
from pathlib import Path

# 找到当前 Python 文件所在的文件夹，再找到 data 文件夹里的 CSV
data_path = Path(__file__).parent / "data" / "五星UP标注.csv"

# 读取 CSV
with data_path.open("r", encoding="utf-8-sig", newline="") as file:
    rows = list(csv.DictReader(file))

# 准备统计变量
up_count = 0
off_banner_count = 0
gaps = []

# 逐行处理17条五星记录
for row in rows:
    result_type = row["结果类型"].strip()

    if result_type == "当期UP":
        up_count += 1
    elif result_type == "歪卡":
        off_banner_count += 1

    # 第一个五星的间隔为空，不参与计算
    gap_text = row["间隔"].strip()
    if gap_text != "":
        gap = float(gap_text)
        gaps.append(gap)

# 输出结果
print(f"五星记录：{len(rows)} 次")
print(f"当期 UP：{up_count} 次")
print(f"歪卡：{off_banner_count} 次")
print(f"有效五星间隔：{len(gaps)} 个")

if gaps:
    average_gap = sum(gaps) / len(gaps)
    print(f"平均间隔：{average_gap:.2f} 抽")
    print(f"最短间隔：{min(gaps):.0f} 抽")
    print(f"最长间隔：{max(gaps):.0f} 抽")