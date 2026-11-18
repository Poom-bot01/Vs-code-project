"""
Name:Poomrapee Aranyawas
Student ID:693040696-8
P7 (functions)
"""


def read_scores():
    filename = input("Filename: ")
    scores = []
    with open(filename, "r") as f:
        for line in f:
            parts = line.split()
            if len(parts) == 3:
                scores.append([parts[0], float(parts[1]), float(parts[2])])
    return scores


def write_scores(scores):
    with open("scores_new.txt", "w") as f:
        for name, mid, final in scores:
            f.write(f"{name} {mid} {final}\n")


def print_score(scores):
    for name, mid, final in scores:
        print(f"{name}: {mid:.2f} + {final:.2f} = {mid + final:.2f}")


def print_menu():
    print("-----")
    print("1) Read database")
    print("2) Save database")
    print("3) Print database")
    print("4) Find top scores")
    print("5) Exit")
    print("-----")


def find_top(scores):
    if not scores:
        return None
    mid_max = max(s[1] for s in scores)
    final_max = max(s[2] for s in scores)
    total_max = max(s[1] + s[2] for s in scores)
    return mid_max, final_max, total_max