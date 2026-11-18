"""
Name:Poomrapee Aranyawas
Student ID:693040696-8
P1
"""
FILENAME = input("Filename: ")
total = 0
i = 1
with open(FILENAME, "r") as f:
    for line in f:
        line = line[:-1]
        total += len(line)
        i += 1
        print(f"{i}:{len(line)} {line}")