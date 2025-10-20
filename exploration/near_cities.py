# or use https://public.opendatasoft.com/api/records/1.0/search/?dataset=georef-france-commune&q=&rows=5000&geofilter.distance=48.8566,2.3522,100000&refine.population=10000
import requests
from geopy.distance import distance

HOME: tuple = (48.117266, -1.6777926) # Rennes
RAYON_TOTAL: int = 150  # km autour de HOME
RAYON_COUPLAGE:int = 50  # km autour de chaque ville
POP_MIN = 10000

resp = requests.get(
    "https://geo.api.gouv.fr/communes?fields=nom,centre,population&format=json"
)
resp_json = resp.json()

near_cities = [
    {
        "nom": c["nom"],
        "lat": c["centre"]["coordinates"][1],
        "lon": c["centre"]["coordinates"][0],
    }
    for c in resp_json
    if c.get("population", 0) >+ POP_MIN
    and distance(
        HOME, (c["centre"]["coordinates"][1], c["centre"]["coordinates"][0])
    ).km
    <= RAYON_TOTAL
]

print(near_cities)
# --- Étape 3 : construction des voisinages ---
for v in near_cities:
    v["cover"] = [
        u["nom"]
        for u in near_cities
        if distance((v["lat"], v["lon"]), (u["lat"], u["lon"])).km <= RAYON_COUPLAGE
    ]

# --- Étape 4 : heuristique de couverture minimale ---
remaining = set(v["nom"] for v in near_cities)
selected = []

while remaining:
    best = max(near_cities, key=lambda x: len(set(x["cover"]) & remaining))
    selected.append(best["nom"])
    remaining -= set(best["cover"])

print("Villes retenues :", selected)
print(f"{len(selected)} villes pour couvrir la zone de {RAYON_TOTAL} km avec un rayon de {RAYON_COUPLAGE} km chacune.")

