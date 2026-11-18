"""
Name:Poomrapee Aranyawas
Student ID:693040696-8
P5
"""
def matrix():
    print("All: ")
    for row in Matrix:
        print(*row)
def transpose():
    print("Transposed: ")
    for col in range(len(Matrix[0])):
        print(*[Matrix[row][col] for row in range(len(Matrix))])
Matrix = []
Row = int(input("Row: "))
for i in range(Row):
    nums = list(map(int, input(f"Enter row {i}: ").split()))
    Matrix.append(nums)
matrix()
transpose()