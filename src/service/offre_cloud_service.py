from business_object.zone_geographique import ZoneGeographique
from business_object.serveur_cloud import ServeurCloud
from service.table.serveurs_service import ServeursService
from datetime import datetime, timedelta

erreur_geo = "Non reconnaissance de votre position géographique"
erreur_em = "Non accès aux données provenant de l'API Electricity Map"

class OffreCloudService:
    """
    Cette classe modélise l’offre de serveurs Cloud accessibles aux fournisseurs de VOD.

    Methods
    -------
    serveurs_eligibles(fournisseurs_cloud, localisation) -> list[ServeurCloud]:
        Renvoie une liste de serveurs dont leur zone de disponibilité comprend la localisation géographique du consommateur de VOD.

    serveurs_optimaux(fournisseurs_cloud, localisation, duree, date_visionnage) -> dict:
        Associe le serveur cloud à l'impact de la consommation électrique en gCO2eq/kWh prévisionnelllement à la durée de la vidéo.
    """
    def serveurs_eligibles(self, localisation: ZoneGeographique, 
                            fournisseurs_cloud: list[str] = ["AWS", "GCP", "Azure"]) -> list[ServeurCloud]:
        """
        Renvoie une liste de serveurs dont leur zone de disponibilité comprend la localisation géographique du consommateur de VOD.

        Parameters
        ----------
        localisation : ZoneGeographique
            Représente un lieu géographiquement par le biais du nom d’une ville et du pays.
        fournisseurs_cloud : list[str], optional
            Liste des fournisseurs cloud, par défaut tous les fournisseurs.

        Returns
        -------
        list[ServeurCloud]
            Liste de serveurs dont leur zone de disponibilité comprend la localisation géographique du consommateur de VOD.
        """
        serveurs_eligibles = []
        zone = localisation.name_to_zone()
        for x in ServeursService().voir(fournisseurs_cloud):
            zone_accessible = x.zone_disponibilite
            if zone in zone_accessible:
                serveurs_eligibles.append(x)
        return serveurs_eligibles

    def serveurs_optimaux(self, localisation: ZoneGeographique, duree: int, date_visionnage: datetime = datetime.now(), 
                            fournisseurs_cloud: list[str] = ["AWS", "GCP", "Azure"]) -> dict:
        """
        Associe le serveur cloud à l'impact de la consommation électrique en gCO2eq/kWh prévisionnelllement à la durée de la vidéo.

        Parameters
        ----------
        localisation : ZoneGeographique
            Représente un lieu géographiquement par le biais du nom d’une ville et du pays.
        duree : int
            Durée de la vidéo en minutes.
        date_visionnage : datetime, optional
            Date de visionnage de la vidéo, par défaut datetime.now().
        fournisseurs_cloud : list[str], optional
            Liste des fournisseurs cloud, par défaut tous les fournisseurs.

        Returns
        -------
        dict
            Dictionnaire qui associe le serveur cloud à l'impact de la consommation électrique en gCO2eq/kWh 
            prévisionnelllement à la durée de la vidéo, par ordre croissant.
        """
        if date_visionnage < datetime.now().replace(minute = 0, second = 0, microsecond = 0):
            raise ValueError(erreur_em)

        serveurs_eligibles = self.serveurs_eligibles(localisation, fournisseurs_cloud)
        serveurs_intensite = {}
        for serveur in serveurs_eligibles:

            liste_dates_electricity = serveur.localisation.prevision_carbone()
            date_visionnage_arrondie = date_visionnage.replace(minute = 0, second = 0, microsecond = 0)
            # Conversion des chaînes de dates en objets datetime
            dates = [datetime.strptime(date[0], "%Y-%m-%d %H:%M:%S") for date in liste_dates_electricity]
            date_maximale = max(dates)
            date_fin_visionnage = date_visionnage + timedelta(minutes = duree)
            if date_fin_visionnage > (date_maximale + timedelta(hours = 1)):
                raise ValueError(erreur_em)
            # Recherche de l'indice de la date actuelle arrondie à l'inférieure
            indice_date_visionnage = next((i for i, date in enumerate(dates) if date == date_visionnage_arrondie), None)
            
            l = []
            ecart_date = (dates[indice_date_visionnage + 1] - date_visionnage).seconds // 60 % 60
            duree_restante = duree
            while duree_restante > 0:
                l.append((ecart_date, liste_dates_electricity[indice_date_visionnage][1]))
                duree_restante = duree_restante  - ecart_date
                ecart_date = min(60, duree_restante)
                indice_date_visionnage += 1
            intensite_carbone_moyenne = sum((minutes_par_tranche * impact_conso_elec) / duree for minutes_par_tranche, impact_conso_elec in l)

            serveurs_intensite[serveur] = round(intensite_carbone_moyenne, 1)

        # Trier le dictionnaire par intensité carbone
        serveurs_tries = dict(sorted(serveurs_intensite.items(), key = lambda item: item[1]))
        return serveurs_tries


if __name__ == "__main__":
    X = OffreCloudService()
    loc = ZoneGeographique("Marseille")
    print(X.serveurs_eligibles(loc))
    print(X.serveurs_optimaux(loc, 20))
