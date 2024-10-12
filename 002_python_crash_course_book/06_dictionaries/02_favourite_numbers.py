favourite_numbers = {"John": 42, "Karl": 15, "Tom": 503}
print(favourite_numbers)

john = favourite_numbers["John"]
print(john)

default = favourite_numbers.get("Bob", 0)
print(default)

# raises KeyError: 'Bill'
# unknown = favourite_numbers["Bill"]
# print(unknown)
