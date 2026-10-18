"""
统计角色活动跃迁里每个五星出现在第几抽，以及相邻两个五星之间隔了多少抽。
"""

import csv

SOURCE = "data/限定角色跃迁抽卡记录.csv"
OUTPUT = "data/五星间隔统计.csv"

with open(SOURCE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

# 按时间排序，保证"第几抽"的顺序和真实抽卡顺序一致
rows.sort(key=lambda row: row["抽卡时间"])

# 找出所有五星，并记下它在整个卡池里的序号（从 1 开始）
five_stars = []
for index, row in enumerate(rows, start=1):
    if row["星数"] == "5":
        five_stars.append((index, row))

result = []
previous_index = None
gap_list = []

for index, row in five_stars:
    if previous_index is None:
        # 第一个五星前面没有可比较的对象，间隔留空
        gap = None
    else:
        gap = index - previous_index
        gap_list.append(gap)
    result.append({
        "序号": len(result) + 1,
        "名称": row["名称"],
        "抽卡时间": row["抽卡时间"],
        "角色活动池第几抽": index,
        "间隔": gap,
    })
    previous_index = index

with open(OUTPUT, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["序号", "名称", "抽卡时间", "角色活动池第几抽", "间隔"])
    writer.writeheader()
    for row in result:
        writer.writerow(row)

# 只有记录里至少有两个五星，才存在有效间隔
if gap_list:
    average_gap = f"{sum(gap_list) / len(gap_list):.2f}"
    min_gap = min(gap_list)
    max_gap = max(gap_list)
else:
    average_gap = min_gap = max_gap = "无数据"

print(f"统计出来的五星角色抽卡记录一共有:{len(result)}条")
print(f"其中，五星角色之间的平均间隔为:{average_gap}")
print(f"其中，五星角色之间的最小间隔为:{min_gap}")
print(f"其中，五星角色之间的最大间隔为:{max_gap}")
