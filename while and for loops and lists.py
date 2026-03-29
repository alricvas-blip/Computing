# This is a simple use of the FizzBuzz problem using a while loop.
k = 0

while k < 101:
    if k % 3 == 0 and k % 5 == 0:
        print("FizzBuzz")
    
    elif k % 3 == 0:
        print("Fizz")

    elif k % 5 == 0:
        print("Buzz")
    
    else:
        print(k)

    k += 1
# This is using a while loop to print all the characters in a string one by one.
Sentence  = "This is a sentence."

s = 0
while s < len(Sentence):
    print(Sentence[s])
    s += 1
# This is using a for loop to calculate the sum of 1 to 1000000.
total = 0
for g in range(1000001):
    total += g
print(total)



#This is asking the user to input a list of groceries and then using a while loop to print each item in the list one by one. 

#newList = input("Enter a grocery list of items separated by commas: ").split(",")
#l = 0
#while l < len(newList):
    #print(newList[l])
   # l += 1


#This is another (better) grocery list program that lets user add remove print items in the list until they want to quit.
grocery_list = []
choice = ""

while choice != "quit":
    choice = input("Enter option (add, remove, print, quit): ").lower()

    if choice == "add":
        item = input("Item to add: ")
        grocery_list.append(item)

    elif choice == "remove":
        item = input("Item to remove: ")
        if item in grocery_list:
            grocery_list.remove(item)
        else:
            print("Item not found.")

    elif choice == "print":
        print(grocery_list)

print("All done!")