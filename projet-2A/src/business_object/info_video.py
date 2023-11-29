from business_object.zone_geographique import ZoneGeographique
from datetime import datetime

class InfoVideo:
    """
    Classe représentant les informations associées à une vidéo.

    Attributes
    ----------
    duree : int
        La durée de la vidéo en minutes.
    resolution : int
        La résolution de la vidéo.
    type_connexion : str
        Le type de connexion utilisé pour regarder la vidéo.
    materiel : str
        Le matériel utilisé pour regarder la vidéo.
    localisation : ZoneGeographique
        L'objet représentant la localisation géographique associée à la position de l'utilisateur.
    date_visionnage : datetime, optional
        Date de visionnage de la vidéo (par défaut, la date actuelle).
    """
    def __init__(self, duree : int, resolution : int, type_connexion : str, 
                 materiel : str, localisation : ZoneGeographique, date_visionnage : datetime = datetime.now()):
        self.duree = duree
        self.resolution = resolution
        self.type_connexion = type_connexion
        self.materiel = materiel
        self.date_visionnage = date_visionnage
        self.localisation = localisation
