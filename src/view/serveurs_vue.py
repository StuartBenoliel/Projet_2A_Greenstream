from InquirerPy import prompt
import dotenv
import os
from view.vue_abstraite import VueAbstraite
from service.table.serveurs_service import ServeursService

dotenv.load_dotenv(override=True)
token_administrateur = os.environ.get('token_admin')

class ServeursVue(VueAbstraite):
    def __init__(self, cle, message=""):
        self.cle = cle
        super().__init__(message)
        self.questions = [
            {
                "type": "list",
                "name": "choix",
                "message": "Types de fournisseurs cloud :",
                "choices": ["(AWS, GCP, Azure)", "(AWS, GCP)", "(AWS, Azure)", "(GCP, Azure)",
                        "AWS", "GCP", "Azure"],
            }
        ]

    def choisir_menu(self):
        reponse = prompt(self.questions)
        fournisseurs = [fournisseur.strip("() ") for fournisseur in reponse["choix"].split(",")]
        list_serveurs = ServeursService().voir(fournisseurs)
        message = "Liste des serveurs:\n\n"

        for serveur in list_serveurs:
            id_serveur = serveur.id_serveur
            nom_serveur = serveur.nom
            fournisseur = serveur.fournisseur_cloud

            message += f"Id Serveur: {id_serveur}, Nom: {nom_serveur}, Fournisseur: {fournisseur}\n"
        if self.cle == token_administrateur:
            from view.menu_administrateur_vue import MenuAdministrateurVue
            return MenuAdministrateurVue(self.cle, message)

        from view.menu_fournisseur_vue import MenuFournisseurVue
        return MenuFournisseurVue(self.cle, message)
