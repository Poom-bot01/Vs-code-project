"""
Name:Poomrapee Aranyawas
Student ID:693040696-8
P8
"""
# This program does not work correctly. Fix it.

with open("equations.txt", "r") as fin:
    with open("results.txt", "w") as fout:
        for line in fin:
            equ = line.split()  
            if len(equ) != 5:   
                continue
            x = int(equ[0])
            op = equ[1]
            y = int(equ[2])
            result = int(equ[4])
            myresult = 0
            if op == "+":
                myresult = x + y
            elif op == "-":
                myresult = x - y
            elif op == "*":
                myresult = x * y

            print(f"{x} {op} {y} = {result}")
            if myresult == result:
                print("Correct")
                fout.write(f"{x} {op} {y} = {result}\n")
            else:
                print("Wrong")
                print(f"{x} {op} {y} = {myresult}")