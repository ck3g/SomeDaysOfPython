from pathlib import Path

path = Path("./002_python_crash_course_book/10_files/learning_python.txt")
contents = path.read_text()

print(contents)

contents += "In Python you can create classes with the class keyword.\n"
contents += "In Python you can create objects from classes.\n"

path.write_text(contents)
