import json
from datetime import datetime

etudiants = {
    "L3-001": {
        "nom": "Rakoto",
        "prenom": "Soa",
        "notes": {"Python": [15, 14], "Réseaux": [12]},
    },
    "L3-002": {
        "nom": "Rabe",
        "prenom": "Andry",
        "notes": {"Python": [9, 13], "Réseaux": [11, 10]},
    },
}
historique = []

def journaliser(fonction):
    @__import__("functools").wraps(fonction)
    def enveloppe(*args, **kwargs):
        historique.append((
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            fonction.__name__,
            {"args": list(args), "kwargs": kwargs.copy()}
        ))
        return fonction(*args, **kwargs)
    return enveloppe

def note_valide(fonction):
    @__import__("functools").wraps(fonction)
    def enveloppe(matricule, matiere, note, *args, **kwargs):
        if not isinstance(note, (int, float)) or not 0 <= note <= 20:
            raise ValueError("Une note doit être comprise entre 0 et 20.")
        return fonction(matricule, matiere, note, *args, **kwargs)
    return enveloppe

def etudiant_existe(fonction):
    @__import__("functools").wraps(fonction)
    def enveloppe(matricule, *args, **kwargs):
        if matricule not in etudiants:
            raise KeyError(f"Matricule inconnu : {matricule}")
        return fonction(matricule, *args, **kwargs)
    return enveloppe

@journaliser
def ajouter_etudiant(matricule, nom, prenom):
    if matricule in etudiants:
        return False, "Ce matricule existe déjà."
    etudiants[matricule] = {"nom": nom, "prenom": prenom, "notes": {}}
    return True, "Étudiant ajouté."

@journaliser
@etudiant_existe
@note_valide
def ajouter_note(matricule, matiere, note):
    etudiants[matricule]["notes"].setdefault(matiere, []).append(note)
    return True, "Note ajoutée."

@etudiant_existe
def moyenne_matiere(matricule, matiere):
    notes = etudiants[matricule]["notes"].get(matiere, [])
    return sum(notes) / len(notes) if notes else 0.0

@etudiant_existe
def moyenne_generale(matricule):
    notes_par_matiere = etudiants[matricule]["notes"]
    moyennes = [
        sum(notes) / len(notes)
        for notes in notes_par_matiere.values()
        if notes
    ]
    return sum(moyennes) / len(moyennes) if moyennes else 0.0

def classement():
    resultat = []
    for matricule, infos in etudiants.items():
        nom_complet = f"{infos['prenom']} {infos['nom']}"
        resultat.append((nom_complet, moyenne_generale(matricule)))
    return sorted(resultat, key=lambda paire: paire[1], reverse=True)

def majors():
    matieres = set()
    for infos in etudiants.values():
        matieres.update(infos["notes"].keys())

    resultat = {}
    for matiere in sorted(matieres):
        candidats = []
        for infos in etudiants.values():
            notes = infos["notes"].get(matiere, [])
            if notes:
                moyenne = sum(notes) / len(notes)
                candidats.append((f"{infos['prenom']} {infos['nom']}", moyenne))
        if candidats:
            resultat[matiere] = max(candidats, key=lambda paire: paire[1])[0]
    return resultat

def sauvegarder(fichier="carnet_notes.json"):
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(etudiants, f, ensure_ascii=False, indent=2)
    print(f"Carnet sauvegardé dans {fichier}.")

def charger(fichier="carnet_notes.json"):
    global etudiants
    with open(fichier, "r", encoding="utf-8") as f:
        donnees = json.load(f)
    # Les clés/valeurs restent compatibles avec les fonctions du programme.
    etudiants = donnees
    print(f"Carnet chargé depuis {fichier}.")

def afficher_bulletin(matricule):
    if matricule not in etudiants:
        print("Matricule inconnu.")
        return
    infos = etudiants[matricule]
    print(f"\\nBulletin de {infos['prenom']} {infos['nom']} ({matricule})")
    for matiere, notes in infos["notes"].items():
        moyenne = sum(notes) / len(notes) if notes else 0
        print(f"- {matiere} : notes {notes}, moyenne {moyenne:.2f}")
    print(f"Moyenne générale : {moyenne_generale(matricule):.2f}")

def afficher_classement():
    print("\\nClassement :")
    for position, (nom, moyenne) in enumerate(classement(), start=1):
        print(f"{position}. {nom:<22} {moyenne:.2f}")

def afficher_majors():
    print("\\nMajors par matière :")
    for matiere, nom in majors().items():
        print(f"- {matiere} : {nom}")

def afficher_historique():
    print("\\nHistorique :")
    if not historique:
        print("Aucune opération enregistrée.")
    for date_heure, fonction, arguments in historique:
        print(date_heure, "-", fonction, "-", arguments)

def demander_matricule():
    return input("Matricule : ").strip()

def menu():
    while True:
        print("""
===== CARNET DE NOTES =====
1. Ajouter un étudiant
2. Ajouter une note
3. Afficher un bulletin
4. Afficher le classement
5. Afficher les majors
6. Afficher l'historique
7. Sauvegarder
8. Charger
0. Quitter
""")
        choix = input("Votre choix : ").strip()
        try:
            if choix == "1":
                matricule = input("Matricule : ").strip()
                nom = input("Nom : ").strip()
                prenom = input("Prénom : ").strip()
                succes, message = ajouter_etudiant(matricule, nom, prenom)
                print(message)
            elif choix == "2":
                matricule = demander_matricule()
                matiere = input("Matière : ").strip()
                note = float(input("Note (0 à 20) : "))
                succes, message = ajouter_note(matricule, matiere, note)
                print(message)
            elif choix == "3":
                afficher_bulletin(demander_matricule())
            elif choix == "4":
                afficher_classement()
            elif choix == "5":
                afficher_majors()
            elif choix == "6":
                afficher_historique()
            elif choix == "7":
                sauvegarder()
            elif choix == "8":
                charger()
            elif choix == "0":
                print("Au revoir !")
                break
            else:
                print("Choix invalide.")
        except (ValueError, KeyError, FileNotFoundError, json.JSONDecodeError) as erreur:
            print("Erreur :", erreur)

if __name__ == "__main__":
    menu()
