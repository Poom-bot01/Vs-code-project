"""
Name:Poomrapee Aranyawas
Student ID:693040696-8
P2
"""
hour = int(input("Time (0-23hr): "))

if hour == 0:
    hour12 = 12
    period = "AM"
elif hour == 12:
    hour12 = 12
    period = "PM"
elif hour > 12:
    hour12 = hour - 12
    period = "PM"
else:
    hour12 = hour
    period = "AM"

with open("sleep.txt", "w") as f:
    f.write(f"It's {hour12} {period} now. Let's go to bed.")