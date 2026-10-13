notes = [12, 8, 15, 17, 9, 11, 14, 6, 13, 16]

# 1. Nombre de notes, moyenne, min et max
nbr_notes = len(notes)
moyenne = sum(notes) / nbr_notes
note_min = min(notes)
note_max = max(notes)

print(f"Nombre de notes: {nbr_notes}")
print(f"Moyenne des notes: {moyenne:.2f}")
print(f"Note min: {note_min}")
print(f"Note max: {note_max}")

admis = [n for n in notes if n >= 10]
ajournes = len([n for n in notes if n < 10])
print("Notes >= 10:", admis)
print("Nombre d'ajournés:", ajournes)


notes_triees = sorted(notes)
trois_meilleures = sorted(notes, reverse=True)[:3]
print("Tri croissant:", notes_triees)
print("Trois meilleures notes:", trois_meilleures)


notes_ajustees = [n + 2 if n < 10 else n for n in notes]
print("Notes ajustées:", notes_ajustees)

def histogramme(liste_notes):
    tranches = {"0-4": 0, "5-9": 0, "10-14": 0, "15-20": 0}
    for n in liste_notes:
        if 0 <= n <= 4: tranches["0-4"] += 1
        elif 5 <= n <= 9: tranches["5-9"] += 1
        elif 10 <= n <= 14: tranches["10-14"] += 1
        elif 15 <= n <= 20: tranches["15-20"] += 1
    for tranche, count in tranches.items():
        print(f"{tranche:<7} | {'*' * count}")

histogramme(notes)


def rang(liste_notes, note_valeur):
    classement = sorted(liste_notes, reverse=True)
    return classement.index(note_valeur) + 1

print("Rang de 14:", rang(notes, 14))


