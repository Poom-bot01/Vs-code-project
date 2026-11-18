"""
Name:Poomrapee Aranyawas
Student ID:693040696-8
P3
"""
filename = input("filename: ")
name = filename.replace(".txt", "")

day = 0
Total_Save = 0
with open(filename, "r") as f:
    for bud in f:
        day += 1
        Total_Save += float(bud)

Avg_P_day = Total_Save / day
report = f"""Summary for {name}
Day saved: {day} days
Total saving: {Total_Save:.2f} Baht
Avg per day saved: {Avg_P_day:.2f} Baht
Good Job!"""

print(report)
with open ("summary.txt", "w") as f:
    f.write(report)