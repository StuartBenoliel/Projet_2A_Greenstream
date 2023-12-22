from InquirerPy import prompt
from datetime import datetime
from view.vue_abstraite import VueAbstraite
from view.menu_fournisseur_vue import MenuFournisseurVue
from business_object.zone_geographique import ZoneGeographique
from service.offre_cloud_service import OffreCloudService

class OffreCloudVue(VueAbstraite):
    def __init__(self, cle, message=""):
        self.cle = cle
        super().__init__(message)
        self.questions = [
            {"type": "input", "name": "duree", "message": "Durée de la vidéo en minutes :"},
            {"type": "input", "name": "ville", "message": "Ville :"},
            {"type": "input", "name": "date_visionnage", "message": "Date de visionnage AAAA-MM-JJTHH:MM (Exemple : 2023-12-22T12:22) :"},
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
        lieu = ZoneGeographique(reponse["ville"])
        fournisseurs = [fournisseur.strip("() ") for fournisseur in reponse["choix"].split(",")]

        try :
            dict_serveurs = OffreCloudService().serveurs_optimaux(lieu, reponse["duree"], datetime.strptime(reponse["date_visionnage"], "%Y-%m-%dT%H:%M"), fournisseurs)
            message = "Liste des serveurs triés par impact électrique croissant:\n\n"
            for key, value in dict_serveurs.items():
                id_serveur = key.id_serveur
                nom_serveur = key.nom
                fournisseur = key.fournisseur_cloud

                message += f"Id Serveur: {id_serveur}, Nom: {nom_serveur}, Fournisseur: {fournisseur}, Impact Electrique: {value} gCO2eq/kWh\n"

        except ValueError as e:
            message = str(e)

        return MenuFournisseurVue(self.cle, message)
