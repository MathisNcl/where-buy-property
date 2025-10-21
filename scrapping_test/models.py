import csv

class Annonce:
    def __init__(self, titre, prix, pieces, surface, lien, ville):
        self.titre = titre
        self.prix = prix
        self.pieces = pieces
        self.surface = surface
        self.lien = lien
        self.ville = ville

    def __repr__(self):
        return f"Annonce(titre={self.titre}, prix={self.prix}, pièces={self.pieces}, surface={self.surface}, lien={self.lien}, ville={self.ville})"

    def to_dict(self):
        return {
            "titre": self.titre,
            "prix": self.prix,
            "pièces": self.pieces,
            "surface": self.surface,
            "lien": self.lien,
            "ville": self.ville
        }

def sauvegarder_en_csv(annonces, fichier="annonces.csv"):
    if not annonces:
        print("Aucune annonce à sauvegarder.")
        return
    with open(fichier, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=annonces[0].to_dict().keys())
        writer.writeheader()
        for annonce in annonces:
            writer.writerow(annonce.to_dict())
    print(f"Les annonces ont été sauvegardées dans {fichier}.")
