from pathlib import Path
import csv

import matplotlib.pyplot as plt
from datetime import datetime

path = Path(
    f"{Path(__file__).parent.resolve()}/weather_data/berlin_barcelona_weather_2024.csv"
)
lines = path.read_text(encoding="utf-8").splitlines()

reader = csv.reader(lines)
header_row = next(reader)

# Extract dates and high temperatures
NAME_IDX = 1
DATE_IDX = 5
TMAX_IDX = 7

dates, highs = [], []
for row in reader:
    if row[NAME_IDX] == "BERLIN DAHLEM, GM":
        current_date = datetime.strptime(row[DATE_IDX], "%Y-%m-%d")
        dates.append(current_date)
        high = float(row[TMAX_IDX])
        highs.append(high)


# Plot the high temperatures
plt.style.use("Solarize_Light2")
fig, ax = plt.subplots()
ax.plot(dates, highs, color="orange")

# Format plot
ax.set_title("High temperatures, 2024", fontsize=24)
ax.set_xlabel("", fontsize=16)
fig.autofmt_xdate()
ax.set_ylabel("Temperature (C)", fontsize=16)
ax.tick_params(labelsize=16)

plt.show()
