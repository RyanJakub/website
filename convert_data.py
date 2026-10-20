
import csv
import json
from pathlib import Path

DATA_DIR = Path("data")

# Load U.S. airports with usable coordinates and IATA codes.
airports = {}
with open(DATA_DIR / "airports.dat", newline="", encoding="utf-8") as f:
    for row in csv.reader(f):
        if len(row) < 8:
            continue

        airport_id, name, city, country, iata = row[:5]
        latitude, longitude = row[6], row[7]

        if country != "United States":
            continue
        if iata == "\\N" or len(iata) != 3:
            continue

        try:
            lat, lon = float(latitude), float(longitude)
        except ValueError:
            continue

        airports[airport_id] = {
            "id": airport_id,
            "iata": iata,
            "name": name,
            "city": city,
            "lat": lat,
            "lon": lon
        }

# Keep unique domestic connections between these airports.
edges = set()
with open(DATA_DIR / "routes.dat", newline="", encoding="utf-8") as f:
    for row in csv.reader(f):
        if len(row) < 6:
            continue

        source_id, destination_id = row[3], row[5]

        if source_id not in airports or destination_id not in airports:
            continue
        if source_id == destination_id:
            continue

        edge = tuple(sorted((source_id, destination_id)))
        edges.add(edge)

airport_list = list(airports.values())
edge_list = [
    {"source": source, "target": target}
    for source, target in sorted(edges)
]

(DATA_DIR / "airports.json").write_text(
    json.dumps(airport_list, separators=(",", ":")),
    encoding="utf-8"
)
(DATA_DIR / "routes.json").write_text(
    json.dumps(edge_list, separators=(",", ":")),
    encoding="utf-8"
)

print(f"Converted {len(airport_list)} airports and {len(edge_list)} unique connections.")
