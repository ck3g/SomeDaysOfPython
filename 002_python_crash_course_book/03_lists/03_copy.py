my_foods = ["pizza", "falafel", "carrot cake"]
friend_foods = my_foods[:]  # copying the list

print("My foods: ", my_foods)
print("My friend's foods: ", friend_foods)

print("\n")

# now the lists are different copies
my_foods.append("cannoli")
friend_foods.append("ice cream")

print("My foods: ", my_foods)
print("My friend's foods: ", friend_foods)
