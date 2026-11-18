"""
Name:Poomrapee Aranyawas
Student ID:693040696-8
P6
"""
def inventory():
    print("---- Inventory ----")
    for name, amount in sorted(Inventory):
        print(f"{name} : {amount}")
    print(f"Total pet: {sum(row[1] for row in Inventory)}")
    print("-------------------")
def adoption():
    pet, amount = input("Name and amount you want to adopt: ").split()
    amount = int(amount)
    for item in Inventory:
        if item[0] == pet:
            if amount > item[1]:
                print(f"You can only adopt {item[1]} {pet}.")
            else:
                item[1] -= amount
                print(f"Thank you! There are {item[1]} {pet} left.")
            return
    print(f"No available {pet}.")
Inventory = []
Animaltype = input("How many types of animals? ")
for i in range(int(Animaltype)):
    Animalname, amount = input("Enter name and quantity for type: ").split()
    Animalnum = int(amount)
    Inventory.append([Animalname, Animalnum])
inventory()
adoption()
