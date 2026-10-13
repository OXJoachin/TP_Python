import math

villes = [
    ("Antananarivo", -18.88, 47.51),
    ("Toamasina", -18.15, 49.40),
    ("Mahajanga", -15.72, 46.32),
    ("Fianarantsoa", -21.45, 47.09),
]

for nom, lat, lon in villes:
    print(f"{nom}: {lat}, {lon}")

plus_au_nord = max(villes, key=lambda v: v[1])
print("Ville la plus au nord:", plus_au_nord[0])

def bornes(villes_list):
    lats = [v[1] for v in villes_list]
    lons = [v[2] for v in villes_list]
    return min(lats), max(lats), min(lons), max(lons)

lat_min, lat_max, lon_min, lon_max = bornes(villes)
print(f"Bornes (lat/lon): {lat_min}, {lat_max}, {lon_min}, {lon_max}")


def distance(p1, p2):
    return math.dist(p1, p2)


paires = {}
for i in range(len(villes)):
    for j in range(i + 1, len(villes)):
        v1 = villes[i]
        v2 = villes[j]
        paires[(v1[0], v2[0])] = distance((v1[1], v1[2]), (v2[1], v2[2]))

print("Nombre de paires:", len(paires))


