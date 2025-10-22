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
        # Accepter les cookies si le bandeau apparaît
        self.accepter_cookies(page)

        # Sélectionner "Acheter"
        page.click('[data-key="BUY"]')
        time.sleep(DELAY_SECONDS)

        # Remplir le champ de localisation (ex: "Paris" ou "75001")
        page.fill('[placeholder="Saisir le lieu ou le code postal"]', self.ville)
        page.wait_for_timeout(1000)  # Attendre la suggestion
        page.keyboard.press("Enter")
        page.wait_for_load_state()

        # Ouvrir le menu Filtres
        try:
            page.click('[data-testid="search-mfe-filtersbar-filter-button"]')
            page.wait_for_load_state("networkidle")
            time.sleep(DELAY_SECONDS)
        except Exception as e:
            print(f"Erreur lors de l'ouverture des filtres: {e}")

        # Filtrer par type de bien (maison dans la version test)
        try:
            page.click('button[aria-label="estate_type"]')
            # Attendre que la liste déroulante soit visible
            page.wait_for_selector("role=listbox", state="visible", timeout=3000)
            # Sélectionner l'option "Maison" (value="House")
            page.click('role=listbox >> text="Maison"')
        except Exception as e:
            print(f"Erreur lors de la sélection du type de bien: {e}")

        # Filtrer par ancienneté / type d'investissement (ancien, neuf, viager, en construction)
        try:
            # Cocher "Ancien" (value="Resale")
            page.click('label:has(input[value="Resale"])')  # Clique sur le texte "Ancien" (plus fiable)
            print("Case 'Ancien' cochée.")
            time.sleep(DELAY_SECONDS)
            # Cocher "Immobilier neuf" en cliquant sur le label
            page.click('label:has(input[value="New_Build"])')
            print("Case 'Immobilier neuf' cochée.")
            time.sleep(DELAY_SECONDS)
        except Exception as e:
            print(f"Erreur lors de la sélection de l'ancienneté: {e}")

        # Filtrer par prix max
        try:
            page.locator('[data-testid="searchmfe-textfield-testid-price-max"] input').fill(str(self.prix_max))
            time.sleep(DELAY_SECONDS)
            print("Saisie du prix maximum effectuée.")
        except Exception as e:
            print(f"Erreur lors de la saisie du prix max: {e}")

        # Filtrer par nombre de pièces minimum
        # utiliser le test id si disponible (déjà présent dans le HTML observé)
        page.click('[data-testid="searchmfe-mindropdownrange-rooms"] button')
        page.wait_for_selector("role=listbox", state="visible", timeout=3000)

        # Sélection du data-key correct en fonction de l'attribut "pieces_min"
        mapping_pieces = {
            1: "one",
            2: "two",
            3: "three",
            4: "four",
            5: "five",
            6: "six",
            7: "seven",
            8: "eight",
            9: "nine",
            10: "ten",
            11: "eleven",
            12: "twelve",
            13: "thirteen",
            14: "fourteen",
            15: "fifteen",
        }

        nb_pieces_str = mapping_pieces.get(int(self.pieces_min))
        page.click(f'[data-key="{nb_pieces_str}"]')
        print(f"Option '{nb_pieces_str} pièces' sélectionnée.")
        time.sleep(DELAY_SECONDS)

        # Valider les filtres
        page.click('button[type="submit"]')
        page.wait_for_load_state("networkidle")  # Attendre le chargement complet

    def accepter_cookies(self, page):
        try:
            # Attendre que la fenêtre de cookies apparaisse (timeout court pour ne pas bloquer)
            page.wait_for_selector('text="Tout accepter"', timeout=5000)  # 5 secondes max
            # Cliquer sur le bouton "Tout accepter"
            page.click('text="Tout accepter"')
            print("Fenêtre de cookies acceptée.")
            time.sleep(1)  # Attendre la disparition de la fenêtre

        except TimeoutError:
            # La fenêtre de cookies n'est pas apparue, on continue
            print("Aucune fenêtre de cookies détectée.")

        except Exception as e:
            # Autre erreur (ex: le bouton n'est pas cliquable)
            print(f"Erreur lors de l'acceptation des cookies: {e}")

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
