from pathlib import Path
import json

numbers = [2, 3, 5, 7, 11, 13]

current_dir = Path(__file__).parent
path = Path(f"{current_dir}/numbers.json")
contents = json.dumps({"numbers": numbers})
path.write_text(contents)

json_contents = path.read_text()
new_numbers = json.loads(json_contents)

print(numbers)
