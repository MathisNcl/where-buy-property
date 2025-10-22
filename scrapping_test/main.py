from scraper import SeLogerPlaywrightScraper
from models import sauvegarder_en_csv


def main():
    ville = "Pineuilh"  # input("Entrez la ville (code postal ou nom) : ")
    prix_max = 100000  # input("Entrez le prix maximum (en euros) : ")
    pieces_min = 2  # input("Entrez le nombre de pièces minimum : ")
    max_pages = 1  # int(input("Nombre de pages à scraper (ex: 3) : "))

    scraper = SeLogerPlaywrightScraper(ville, prix_max, pieces_min)
    annonces = scraper.scrapper(max_pages=max_pages)

    print(f"\n{len(annonces)} annonces trouvées pour {ville} :")
    for annonce in annonces:
        print(annonce)

    sauvegarder_en_csv(annonces)


if __name__ == "__main__":
    main()
