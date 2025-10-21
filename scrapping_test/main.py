from scraper import SeLogerScraper
from models import sauvegarder_en_csv

def main():
    ville = input("Entrez la ville (code postal ou nom) : ")
    prix_max = input("Entrez le prix maximum (en euros) : ")
    pieces_min = input("Entrez le nombre de pièces minimum : ")
    max_pages = int(input("Nombre de pages à scraper (ex: 3) : "))

    scraper = SeLogerScraper(ville, prix_max, pieces_min)
    annonces = scraper.scrapper(max_pages=max_pages)

    print(f"\n{len(annonces)} annonces trouvées pour {ville} :")
    for annonce in annonces:
        print(annonce)

    sauvegarder_en_csv(annonces)

if __name__ == "__main__":
    main()
