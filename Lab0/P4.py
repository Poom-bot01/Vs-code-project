"""
Name:Poomrapee Aranyawas
Student ID:693040696-8
P4
"""
def Wordinput():
    print("Words in input order:")
    print(*word)
def Wordalphabetical():
    print("Words in alphabetical order:")
    print(*sorted(word))
def FindWord():
    target = input("Word to be search: ")
    for i in range(len(word)):
        if word[i].lower() == target.lower():
            print(f"Found >> {target} << at index {i}")
    if target.lower() not in [w.lower() for w in word]:
        print(f">> {target} << not found ")
word = []
while True:
    w = input("Word: ")
    if w.upper() == "GOLDEN":
        break
    word.append(w)
Wordinput()
Wordalphabetical()
FindWord()