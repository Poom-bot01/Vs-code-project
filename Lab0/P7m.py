"""
Name:Poomrapee Aranyawas
Student ID:693040696-8
P7 (main program)
"""
''' --------------------------------
DO NOT change the import section
-------------------------------- '''
from P7f import print_menu, read_scores, write_scores, print_score, find_top

''' ---------------------------
Modify your code here
--------------------------- '''
if __name__ == "__main__":
    scores = []
    while True:
        print_menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            scores = read_scores()
            print("Done reading from file.")
        elif choice == "2":
            write_scores(scores)
            print("Done writing to file.")
        elif choice == "3":
            print_score(scores)
        elif choice == "4":
            top = find_top(scores)
            if top is not None:
                print(f"Midterm max = {top[0]:.2f}")
                print(f"Final max = {top[1]:.2f}")
                print(f"Total max = {top[2]:.2f}")
            else:
                print("No scores available.")
        elif choice == "5":
            print("Bye!")
            break
        else:
             print("Invalid choice.")