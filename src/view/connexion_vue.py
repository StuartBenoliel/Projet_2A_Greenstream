from InquirerPy import prompt
import dotenv
import os
from view.vue_abstraite import VueAbstraite
from service.table.cles_api_service import ClesApiService

dotenv.load_dotenv(override=True)
token_administrateur = os.environ.get('token_admin')

class ConnexionVue(VueAbstraite):
    def __init__(self, message=""):
        super().__init__(message)
        self.questions = [
            {
                "type": "list",
                "name": "utilisateur",
                "message": "Type d'utilisateur :",
                "choices": [
                    "Administrateur",
                    "Fournisseur",
                    "Consommateur",
                ],
            },
            {"type": "input", "name": "cle", "message": "Entrez votre clé API :"}
        ]

    def afficher(self):
        self.nettoyer_console()
        print("Connexion à l'application")
        print()

    def choisir_menu(self):
        reponse = prompt(self.questions)

        if reponse["utilisateur"] == "Administrateur" and reponse["cle"] == token_administrateur:
            message = f'Vous êtes connecté en tant que {reponse["utilisateur"]} via la clé API : {reponse["cle"]}'
            from view.menu_administrateur_vue import MenuAdministrateurVue
            return MenuAdministrateurVue(reponse["cle"], message)

        try :
            cle_hachee = ClesApiService().trouver_cle_api(reponse["utilisateur"], reponse["cle"])
        except ValueError as e:
            message = str(e)
            from view.accueil_vue import AccueilVue
            return AccueilVue(message)

        message = f'Vous êtes connecté en tant que {reponse["utilisateur"]} via la clé API : {reponse["cle"]}'
        if reponse["utilisateur"] == "Fournisseur":
            from view.menu_fournisseur_vue import MenuFournisseurVue
            return MenuFournisseurVue(cle_hachee, message)

        if reponse["utilisateur"] == "Consommateur":
            from view.menu_consommateur_vue import MenuConsommateurVue
            return MenuConsommateurVue(cle_hachee, message)