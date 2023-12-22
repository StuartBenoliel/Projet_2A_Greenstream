from InquirerPy import prompt
from datetime import datetime
from view.vue_abstraite import VueAbstraite
from view.menu_consommateur_vue import MenuConsommateurVue
from business_object.info_video import InfoVideo
from business_object.zone_geographique import ZoneGeographique
from service.empreinte_carbone_service import EmpreinteCarboneService

class EmpreinteCarboneVue(VueAbstraite):
    def __init__(self, cle, message=""):
        self.cle = cle
        super().__init__(message)
        self.questions = [
            {"type": "input", "name": "duree", "message": "Durée de la vidéo en minutes :"},
            {"type": "input", "name": "ville", "message": "Ville :"},
            {"type": "input", "name": "date_visionnage", "message": "Date de visionnage AAAA-MM-JJTHH:MM (Exemple : 2023-12-22T12:22):"},
            {"type": "list", "name": "resolution", "message": "Résolution :",
                "choices": [240,360,480,720,1080,1440,2160,4320]},
            {"type": "list", "name": "type_connexion", "message": "Type de connexion :",
                "choices": ["Wifi", "Reseau", "Cable"]},
            {"type": "list", "name": "materiel", "message": "Matériel utilisé :",
                "choices": ["Ordinateur", "Mobile"],
            },
        ]

    def choisir_menu(self):
        reponse = prompt(self.questions)
        lieu = ZoneGeographique(reponse["ville"])
        donnees = InfoVideo(reponse["duree"], reponse["resolution"], reponse["type_connexion"], reponse["materiel"], lieu, datetime.strptime(reponse["date_visionnage"], "%Y-%m-%dT%H:%M"))
        try :
            empreinte = EmpreinteCarboneService().empreinte_carbone(donnees, self.cle)
            message = f'Votre empreinte carbone générée suivant vos paramètres de visualisation est de {empreinte} gCO2eq'

        except ValueError as e:
            message = str(e)

        return MenuConsommateurVue(self.cle, message)
