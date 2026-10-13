import json
from collections import Counter

stock = {
    "riz": {"prix": 3200, "quantite": 50},
    "huile": {"prix": 9500, "quantite": 12},
    "sucre": {"prix": 4000, "quantite": 30},
    "savon": {"prix": 1500, "quantite": 0},
}


for produit, infos in stock.items():
    print(f"{produit} - Prix: {infos['prix']} Ar, Quantité: {infos['quantite']}")


valeur_totale = sum(infos["prix"] * infos["quantite"] for infos in stock.values())
print(f"Valeur totale du stock: {valeur_totale} Ar")


rupture = [p for p, infos in stock.items() if infos["quantite"] == 0]
print("En rupture:", rupture)


def vendre(stock_dict, produit, qte):
    item = stock_dict.get(produit)
    if not item:
        return False, "Produit inconnu"
    if item["quantite"] < qte:
        return False, "Quantité insuffisante"
    item["quantite"] -= qte
    return True, "Vente réussie"


def ajouter_produit(stock_dict, nom, prix, quantite):
    if nom in stock_dict:
        return False, "Produit déjà présent"
    stock_dict[nom] = {"prix": prix, "quantite": quantite}
    return True, "Produit ajouté avec succès"


prix_hausse = {p: round(infos["prix"] * 1.1) for p, infos in stock.items()}
print("Prix haussés:", prix_hausse)


ventes = ["riz", "sucre", "riz", "huile", "riz"]
compteur_get = {}
for v in ventes:
    compteur_get[v] = compteur_get.get(v, 0) + 1
print("Compteur avec get:", compteur_get)
print("Compteur avec Counter:", dict(Counter(ventes)))


with open("stock.json", "w", encoding="utf-8") as f:
    json.dump(stock, f, ensure_ascii=False, indent=2)

with open("stock.json", "r", encoding="utf-8") as f:
    stock_charge = json.load(f)

print("Stocks identiques :", stock == stock_charge)