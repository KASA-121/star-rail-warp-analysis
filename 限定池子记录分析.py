"""
从全卡池记录里只保留角色活动跃迁（卡池编号 11）。
"""

import csv
import json

SOURCE = "data/跃迁记录.txt"
OUTPUT = "data/限定角色跃迁抽卡记录.csv"

POOL_NAME = {
    "1": "常驻池",
    "2": "新手池",
    "11": "限定角色池",
    "12": "限定光锥池",
}

star_5_num = 0

with open(SOURCE, "r", encoding="utf-8") as f1:
    raw = json.load(f1)

rows = []

for pool_id in raw:
    if pool_id != "11":
        continue
    for record in raw[pool_id]:
        row = {
            "抽卡时间": record["time"],
            "卡池名称": POOL_NAME[pool_id],
            "星数": record["star"],
            "名称": record["name"],
        }
        rows.append(row)
        if record["star"] == 5:
            star_5_num += 1

with open(OUTPUT, "w", encoding="utf-8-sig", newline="") as f2:
    writer = csv.DictWriter(f2, fieldnames=["抽卡时间", "卡池名称", "星数", "名称"])
    writer.writeheader()
    for item in rows:
        writer.writerow(item)

print(f"限定角色卡池的抽卡记录一共有:{len(rows)}条")
print(f"卡池中五星角色的抽卡记录一共有:{star_5_num}条")
