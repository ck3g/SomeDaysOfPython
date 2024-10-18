from pathlib import Path
import csv

path = Path(
    f"{Path(__file__).parent.resolve()}/weather_data/berlin_barcelona_weather_2024.csv"
)
lines = path.read_text(encoding="utf-8").splitlines()

reader = csv.reader(lines)
header_row = next(reader)

# Extract high temperatures
NAME_IDX = 1
DATE_IDX = 5
TMAX_IDX = 7

highs = []
for row in reader:
    if row[NAME_IDX] == "BERLIN DAHLEM, GM":
        high = float(row[TMAX_IDX])
        highs.append(high)


print(highs)
