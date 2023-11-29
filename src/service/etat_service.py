import os
from dotenv import load_dotenv
import requests

load_dotenv()
token_em = os.environ.get('token_em')
headers = {'auth-token': token_em}

url_etat_electricity_map = "https://api.electricitymap.org/health"
url_etat_nominatim_openstreetmap = "https://nominatim.openstreetmap.org/status"

class EtatService:
    """
    Cette classe fournit des méthodes pour vérifier l'état de l'accès aux APIs externes.

    Methods
    -------
    lien_api_electricity_map() -> bool
        Vérifie l'état de l'accès à l'API Electricity Map.
    lien_api_nominatim_openstreetmap() -> bool
        Vérifie l'état de l'accès à l'API Nominatim OpenStreetMap.
    """
    def lien_api_electricity_map(self) -> bool:
        """
        Vérifie l'état de l'accès à l'API Electricity Map.

        Returns
        -------
        bool
            True si l'accès à l'API est réussi, False sinon.
        """
        response = requests.get(url_etat_electricity_map, headers = headers, timeout = 60)
        if response.status_code == 200:
            return True
        return False
    
    def lien_api_nominatim_openstreetmap(self) -> bool:
        """
        Vérifie l'état de l'accès à l'API Nominatim OpenStreetMap.

        Returns
        -------
        bool
            True si l'accès à l'API est réussi, False sinon.
        """
        response = requests.get(url_etat_nominatim_openstreetmap, timeout = 90)
        if response.status_code == 200:
            return True
        return False

if __name__ == "__main__":
    X = EtatService()
    print(X.lien_api_electricity_map())
    print(X.lien_api_nominatim_openstreetmap())