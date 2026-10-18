import csv

SOURCE = r"data\限定角色跃迁抽卡记录.csv"
OUTPUT = r"data\五星间隔统计.csv"

with open(SOURCE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))


rows.sort(key=lambda row: row["抽卡时间"])

five_stars = []
for index, row in enumerate(rows, start=1):
    if row["星数"] == "5":
        five_stars.append((index, row))

result = []
previous_index = None
gap_list = []

for index, row in five_stars:

    if previous_index is None:
        gap = None
    else:
        gap = index - previous_index
        gap_list.append(gap)
    result.append({
        "序号":len(result) + 1,
        "名称":row["名称"],
        "抽卡时间":row["抽卡时间"],
        "角色活动池第几抽":index,
        "间隔": gap
    })

    previous_index = index

with open(OUTPUT, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["序号","名称", "抽卡时间", "角色活动池第几抽", "间隔"])
    writer.writeheader()
    for row in result:
        writer.writerow(row)

if gap_list:
    average_gap = sum(gap_list) / len(gap_list)
else:
    average_gap = None

print(f"统计出来的五星角色抽卡记录一共有:{len(result)}条")
print(f"其中，五星角色之间的平均间隔为:{average_gap:.2f}")
print(f"其中，五星角色之间的最小间隔为:{min(gap_list)}")
print(f"其中，五星角色之间的最大间隔为:{max(gap_list)}")