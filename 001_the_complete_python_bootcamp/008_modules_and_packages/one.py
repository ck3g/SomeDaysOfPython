# all the code at indentation level 0 is going to be runned
# it will be executed when importing a module

print('hello one.py (runs all the time)')

def somefunc():
  print("A func in one.py")

# __name__ = "__main__" # Python will assign this variable when the file is runned directly via `python one.py`

if __name__ == "__main__":
  print("only runs when the file is directly called")
else:
  print("one.py has been imported")