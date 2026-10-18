"""
把游戏导出的抽卡 JSON 记录整理成一行一抽的 CSV。

原始文件需要自己从游戏里导出，重命名为 跃迁记录.txt 放进 data 文件夹。
"""

import csv
import json

SOURCE = "data/跃迁记录.txt"
OUTPUT = "data/抽卡记录.csv"

# 原始记录里不同卡池用数字编号表示，这里换成便于阅读的中文名
POOL_NAMES = {
    "1": "常驻跃迁",
    "2": "新手跃迁",
    "11": "角色活动跃迁",
    "12": "光锥活动跃迁",
}

star_5_num = 0

with open(SOURCE, "r", encoding="utf-8") as f:
    raw = json.load(f)

rows = []

# 外层字典的键是卡池编号，另外还有一个 uid（账号 ID），它不是抽卡记录，需要跳过
for pool_id in raw:
    if pool_id == "uid":
        continue
    for record in raw[pool_id]:
        row = {
            "抽卡时间": record["time"],
            "卡池名称": POOL_NAMES[pool_id],
            "星数": record["star"],
            "名称": record["name"],
        }
        rows.append(row)
        if record["star"] == 5:
            star_5_num += 1

# utf-8-sig 是为了让 Excel 打开时中文不乱码
with open(OUTPUT, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["抽卡时间", "卡池名称", "星数", "名称"])
    writer.writeheader()
    for row in rows:
        writer.writerow(row)

print(f"整理的抽卡记录一共有:{len(rows)}条")
print(f"卡池中五星角色的抽卡记录一共有：{star_5_num}条")
