import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
token_em = os.environ.get('token_em')
headers = {'auth-token': token_em}

# URL pour les requetes API sur Nominatim et ElectricityMap
url_geo = "https://nominatim.openstreetmap.org/search"
url_em = "https://api.electricitymap.org/v3/carbon-intensity/latest"
# Utilisé pour récupérer la zone. Url plus rapide que le deuxième et moins restrictif.
url_em_prev = "https://api.electricitymap.org/v3/carbon-intensity/forecast"

erreur_geo = "Non reconnaissance de votre position géographique"
erreur_em = "Non accès aux données provenant de l'API Electricity Map"

class ZoneGeographique:
    """ 
    Cette classe représente un lieu géographiquement par le biais du nom d’une
    ville et du pays.

    Attributes
    ----------
    ville : str
        Le nom de la ville.
    pays : str | None, optional
        Le nom du pays. Par défaut, None.

    Methods
    -------
    name_to_zone()
        Fournit la zone electricity map contenant la ville.
    prevision_carbone()
        Accède à la prévision de l'impact de la consommation électrique en gCO2eq/kWh de la zone electricity map correspondante.
    __repr__()
        Retourne une représentation sous forme de chaîne de caractères de la zone géographique.
    """
    def __init__(self, ville : str, pays : str | None = None) :
        self.ville = ville
        self.pays = pays
    
    def name_to_zone(self) -> str:
        """ 
        Fournit la zone electricity map comprenant la ville.

        Returns
        -------
        str
            Zone electricity map.
        """
        if self.pays is None:
            params_geo = {'city': self.ville, 'format': 'json'}
            response = requests.get(url_geo, params = params_geo)
        else:
            params_geo = {'city': self.ville, 'country': self.pays, 'format': 'json'}
            response = requests.get(url_geo, params = params_geo)

        if response.status_code != 200:
            raise ValueError(erreur_geo)
        
        if len(response.json()) == 0:
            raise ValueError(erreur_geo)
 
        response_nominatim = response.json()[0] 
        params_em = {'lat': response_nominatim['lat'], 'lon': response_nominatim['lon']}
        response_em = requests.get(url_em, params = params_em, headers = headers)

        if response_em.status_code != 200:
            raise ValueError(erreur_em)

        return response_em.json()["zone"]

    def prevision_carbone(self) -> list:
        """ 
        Accède à la prévision de l'impact de la consommation électrique en gCO2eq/kWh de la zone géographique.

        Returns
        -------
        list
            Liste de tuples contenant la date et la prévision de l'impact carbone de la consommation d’électricité associée.
        """
        zone = self.name_to_zone()
        params_em_prev = {'zone': zone}
        response = requests.get(url_em_prev, params = params_em_prev, headers = headers)
        if response.status_code != 200:
            raise ValueError(erreur_em)

        if 'error' in response.json():
            raise ValueError(erreur_em)

        response_list = response.json()["forecast"]
        l = []
        for entree in response_list:
            date_string = entree['datetime']
            date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
            # Convertir l'objet datetime en une nouvelle chaîne avec un format différent
            date_object = date_object.strftime('%Y-%m-%d %H:%M:%S')
            l.append((date_object, entree['carbonIntensity']))
        return l
        
    def __repr__(self):
        return f"ZoneGeographique[ville = '{self.ville}', pays = '{self.pays}']"


if __name__ == "__main__":
    X = ZoneGeographique("Bruz")
    Y = ZoneGeographique("Pékin")
    print(X.name_to_zone())
    print(X.prevision_carbone())
    print(Y.name_to_zone())