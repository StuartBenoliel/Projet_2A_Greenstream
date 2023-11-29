from business_object.info_video import InfoVideo
from dao.historique_consommateur_dao import HistoriqueConsommateurDao
from datetime import datetime, timedelta
from statistics import mean

erreur_em = "Non accès aux données provenant de l'API Electricity Map"

class EmpreinteCarboneService:
    """ 
    Cette classe permet aux consommateurs de VOD de simuler l'impact carbone généré par la lecture d'une vidéo en streaming.

    Methods
    -------
    empreinte_carbone(donnees, cle_api) -> float:
        Simule l'impact carbone généré par la lecture d'une vidéo en streaming.

    empreinte_moyenne(cle_api) -> float:
        Calcule la moyenne de l'empreinte carbone du consommateur sur les requêtes depuis la base de données.

    empreinte_total(cle_api) -> float:
        Calcule le total de l'empreinte carbone du consommateur sur les requêtes depuis la base de données.
    """
    def empreinte_carbone(self, donnees: InfoVideo, cle_api: str) -> float:
        """ 
        Simule l'impact carbone généré par la lecture d'une vidéo en streaming.

        Parameters
        ----------
        donnees : InfoVideo
            Informations de la vidéo et les paramètres de sa visualisation.
        cle_api : str
            Clé API du consommateur de VOD.

        Returns
        -------
        float
            Simulation de l'empreinte carbone générée par la lecture d'une vidéo en gCO2eq.
        """
        dict_resolution = {240: 426 * 240, 360: 640 * 360, 480: 854 * 480,
                           720: 1280 * 720, 1080:  1920 * 1080, 1440: 2560 * 1440,
                           2160: 3840 * 2160, 4320: 7680 * 4320}
        
        dict_materiel = {"Ordinateur": 3.2e-4, "Mobile": 1.1e-4}

        dict_type_connexion = {"Wifi": 1.52e-10, "Reseau": 8.84e-10, "Cable": 4.29e-10}
        
        resolution = donnees.resolution
        materiel = donnees.materiel
        type_connexion = donnees.type_connexion
        date_visionnage = donnees.date_visionnage
        energie_data_center = 7.2e-11
        duree = donnees.duree
    
        if resolution not in dict_resolution:
            raise ValueError("Résolution non connu")

        if materiel not in dict_materiel:
            raise ValueError("Matériel non connu")

        if type_connexion not in dict_type_connexion:
            raise ValueError("Type de connexion non connu")

        if date_visionnage < datetime.now().replace(minute = 0, second = 0, microsecond = 0):
            raise ValueError(erreur_em)

        liste_dates_electricity = donnees.localisation.prevision_carbone()

        # 25 images par sec * 60 sec
        nb_bytes = dict_resolution[resolution] * 25 * 60 * duree
        # en KWh
        impact_energie = duree * dict_materiel[materiel] + nb_bytes * (dict_type_connexion[type_connexion] + energie_data_center)
        # Conversion des chaînes de dates en objets datetime
        dates = [datetime.strptime(date[0], "%Y-%m-%d %H:%M:%S") for date in liste_dates_electricity]

        date_maximale = max(dates)
        date_fin_visionnage = date_visionnage + timedelta(minutes = duree)
        if date_fin_visionnage > (date_maximale + timedelta(hours = 1)):
            raise ValueError(erreur_em)

        date_visionnage_arrondie = date_visionnage.replace(minute = 0, second = 0, microsecond = 0)
        # Recherche de l'indice de la date actuelle arrondie à l'inférieure
        indice_date_visionnage = next((i for i, date in enumerate(dates) if date == date_visionnage_arrondie), None)
        print(indice_date_visionnage)
        l = []
        ecart_date = (dates[indice_date_visionnage + 1] - date_visionnage).seconds // 60 % 60
        if date_visionnage == date_visionnage_arrondie:
            ecart_date = 60
        while duree > 0:
            l.append((ecart_date, liste_dates_electricity[indice_date_visionnage][1]))
            duree = duree - ecart_date
            ecart_date = min(60, duree)
            indice_date_visionnage += 1
        intensite_carbone_moyenne = sum((minutes_par_tranche * impact_conso_elec) / donnees.duree for minutes_par_tranche, impact_conso_elec in l)
        empreinte = round(impact_energie * intensite_carbone_moyenne, 1)

        HistoriqueConsommateurDao().creer(donnees, empreinte, cle_api)

        return empreinte
        
    def empreinte_moyenne(self, cle_api: str) -> float:
        """ 
        Calcule la moyenne de l'empreinte carbone du consommateur sur les requêtes depuis la base de données.

        Parameters
        ----------
        cle_api : str
            Clé API du consommateur ce VOD.

        Returns
        -------
        float
            Moyenne de l'empreinte carbone du consommateur de VOD en gCO2eq.
        """
        l = HistoriqueConsommateurDao().trouver_empreinte_par_cle_api(cle_api) 
        if len(l) == 0:
            return 0
        return mean(l)

    def empreinte_total(self, cle_api: str) -> float:
        """ 
        Calcule le total de l'empreinte carbone du consommateur sur les requêtes depuis la base de données.

        Parameters
        ----------
        cle_api : str
            Clé API du consommateur de VOD.

        Returns
        -------
        float
            Total de l'empreinte carbone du consommateur de VOD en gCO2eq.
        """
        l = HistoriqueConsommateurDao().trouver_empreinte_par_cle_api(cle_api) 
        return sum(l)


if __name__ == "__main__":
    
    from business_object.zone_geographique import ZoneGeographique
    from service.table.cles_api_service import ClesApiService
    import time

    X = EmpreinteCarboneService()

    resolution = 720
    duree = 60  # en minutes
    typeConnexion = "Wifi"
    materiel = "Ordinateur"

    zone_geo = ZoneGeographique("Paris", "France")
    donnee = InfoVideo(duree,resolution,typeConnexion, materiel, zone_geo)
    donnee2 = InfoVideo(210,resolution,typeConnexion, materiel, zone_geo)

    cle_api = ClesApiService().generer_cle_api("Consommateur")["cle_api"]
    cle_hachee = ClesApiService().trouver_cle_api("Consommateur", cle_api)

    print(X.empreinte_carbone(donnee, cle_hachee))
    time.sleep(2) # Ecart d'au moins 1 sec pour l'enregistrement dans la table.
    print(X.empreinte_carbone(donnee2, cle_hachee))
    print(X.empreinte_moyenne(cle_hachee))
    print(X.empreinte_total(cle_hachee))