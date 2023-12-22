from InquirerPy import prompt

from view.vue_abstraite import VueAbstraite
from view.accueil_vue import AccueilVue
from service.table.cles_api_service import ClesApiService


class GenererCleVue(VueAbstraite):
    def __init__(self, message=""):
        super().__init__(message)
        self.questions = [
            {
                "type": "list",
                "name": "utilisateur",
                "message": "Type d'utilisateur :",
                "choices": [
                    "Fournisseur",
                    "Consommateur",
                ],
            }
        ]

    def choisir_menu(self):
        reponse = prompt(self.questions)
        nouvelle_cle = ClesApiService().generer_cle_api(reponse["utilisateur"])  
        message = f'Votre clé API de {reponse["utilisateur"]} : {nouvelle_cle["cle_api"]}'
        return AccueilVue(message)
