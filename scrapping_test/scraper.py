from playwright.sync_api import sync_playwright
from config import BASE_URL, DELAY_SECONDS
from models import Annonce
import time


class SeLogerPlaywrightScraper:
    def __init__(self, ville, prix_max, pieces_min):
        self.ville = ville
        self.prix_max = prix_max
        self.pieces_min = pieces_min
        self.annonces = []

    def _remplir_formulaire(self, page):
        # Remplir le champ de localisation (ex: "Paris" ou "75001")
        page.fill('input[aria-label="Rechercher une ville, un quartier, une adresse..."]', self.ville)
        page.wait_for_timeout(1000)  # Attendre la suggestion
        page.keyboard.press("Enter")
        time.sleep(DELAY_SECONDS)

        # Sélectionner "Acheter"
        page.click('text="Acheter"')
        time.sleep(DELAY_SECONDS)

        # Filtrer par prix max
        page.fill('input[aria-label="Budget maximum"]', self.prix_max)
        time.sleep(DELAY_SECONDS)

        # Filtrer par nombre de pièces min
        page.select_option('select[aria-label="Nombre de pièces minimum"]', str(self.pieces_min))
        time.sleep(DELAY_SECONDS)

        # Valider les filtres
        page.click('button[type="submit"]')
        page.wait_for_load_state("networkidle")  # Attendre le chargement complet

    def _extraire_annonces(self, page):
        annonces = []
        items = page.query_selector_all(".c-pa-list")
        for item in items:
            try:
                titre = item.query_selector(".c-pa-link").inner_text().strip()
                prix = item.query_selector(".c-pa-price").inner_text().strip()
                pieces = item.query_selector(".c-pa-room").inner_text().strip()
                surface = item.query_selector(".c-pa-area").inner_text().strip()
                lien = BASE_URL + item.query_selector(".c-pa-link").get_attribute("href")
                annonces.append(Annonce(titre, prix, pieces, surface, lien, self.ville))
            except Exception as e:
                print(f"Erreur lors de l'extraction: {e}")
        return annonces

    def scrapper(self, max_pages=2):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # Mode visible pour debug
            page = browser.new_page()
            page.goto(BASE_URL, timeout=60000)

            # Remplir le formulaire
            self._remplir_formulaire(page)

            # Scraper les annonces sur plusieurs pages
            for _ in range(max_pages):
                annonces_page = self._extraire_annonces(page)
                if not annonces_page:
                    break
                self.annonces.extend(annonces_page)

                # Pagination (si disponible)
                try:
                    page.click('a[aria-label="Page suivante"]')
                    page.wait_for_load_state("networkidle")
                    time.sleep(DELAY_SECONDS)
                except Exception as e:
                    print(f"Plus de pages ou erreur: {e}")
                    break

            browser.close()
        return self.annonces
