from enum import Enum
import uvicorn
import os
from dotenv import load_dotenv
from datetime import datetime
from fastapi import HTTPException, Depends, FastAPI, Header
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from service.offre_cloud_service import OffreCloudService
from service.empreinte_carbone_service import EmpreinteCarboneService
from service.etat_service import EtatService
from service.table.cles_api_service import ClesApiService
from service.table.historique_consommateur_service import HistoriqueConsommateurService
from service.table.serveurs_service import ServeursService
from business_object.info_video import InfoVideo
from business_object.zone_geographique import ZoneGeographique

load_dotenv()
token_administrateur = os.environ.get('token_admin')

app = FastAPI()

class Utilisateur(str, Enum):
    """
    Enumération des types d'utilisateurs.
    """
    Fournisseur = "Fournisseur"
    Consommateur = "Consommateur"

class Resolution(int, Enum):
    """
    Enumération des types de résolutions possibles.
    """
    _240 = 240
    _360 = 360
    _480 = 480
    _720 = 720
    _1080 = 1080
    _1440 = 1440
    _2160 = 2160
    _4320 = 4320

class Materiel(str, Enum):
    """
    Enumération des types de matériel possibles.
    """
    Ordinateur = "Ordinateur"
    Mobile = "Mobile"

class TypeConnexion(str, Enum):
    """
    Enumération des types de connexion possibles.
    """
    Wifi = "Wifi"
    Reseau = "Reseau"
    Cable = "Cable"

class FournisseurCloud(str, Enum):
    """
    Enumération des fournisseurs cloud.

    Attributes
    ----------
    AWS_GCP_Azure: str
        AWS, GCP, et Azure.
    AWS_GCP: str
        AWS et GCP.
    AWS_Azure: str
        AWS et Azure.
    GCP_Azure: str
        GCP et Azure.
    AWS: str
        AWS seul.
    GCP: str
        GCP seul.
    Azure: str
        Azure seul.

    Methods
    -------
    to_list() -> list[str]:
        Convertit la chaîne de valeurs en liste de fournisseurs cloud.
    """
    AWS_GCP_Azure = "(AWS, GCP, Azure)"
    AWS_GCP = "(AWS, GCP)"
    AWS_Azure = "(AWS, Azure)"
    GCP_Azure= "(GCP, Azure)"
    AWS = "AWS"
    GCP = "GCP"
    Azure = "Azure"

    def to_list(self) -> list[str]:
        """
        Convertit la chaîne de valeurs en liste de fournisseurs cloud.

        Returns
        -------
        list[str]
            Liste des fournisseurs cloud.
        """
        return [fournisseur.strip("() ") for fournisseur in self.value.split(",")]

class ZoneGeographiqueModel(BaseModel):
    """
    Modèle représentant une zone géographique.

    Attributes
    ----------
    ville: str
        Nom de la ville.
    pays: str | None, facultatif
        Nom du pays.
    """
    ville: str
    pays: str | None = None

class ServeurModel(BaseModel):
    """
    Modèle représentant un serveur cloud.

    Attributes
    ----------
    id_serveur: str
        Identifiant unique du serveur.
    nom: str
        Nom du serveur.
    code_region: str
        Code de la région où se trouve le serveur.
    fournisseur_cloud: str
        Fournisseur cloud associé.
    empreinte: float | None, facultatif
        Empreinte carbone du serveur.
    localisation: ZoneGeographiqueModel
        Modèle représentant la localisation géographique (voir la documentation de la classe ZoneGeographiqueModel).
    """
    id_serveur: str
    nom: str
    code_region: str
    fournisseur_cloud: str
    impact_carbone: float | None = None
    localisation: ZoneGeographiqueModel

class InfoVideoModel(BaseModel):
    """
    Modèle représentant les informations associées au visionnage d'une vidéo.

    Attributes
    ----------
    duree: int
        Durée de la vidéo en minutes.
    resolution: Resolution
        Résolution de la vidéo.
    type_connexion: TypeConnexion
        Type de connexion utilisé pour visionner la vidéo.
    materiel: Materiel
        Matériel utilisé pour visionner la vidéo.
    date_visionnage: datetime, facultatif
        Date de visionnage de la vidéo (par défaut, la date actuelle).
    localisation: ZoneGeographiqueModel
        Modèle représentant la localisation géographique (voir la documentation de la classe ZoneGeographiqueModel).
    """
    duree: int
    resolution: Resolution
    type_connexion: TypeConnexion
    materiel: Materiel
    date_visionnage: datetime = datetime.now()
    localisation: ZoneGeographiqueModel

def get_cle_api_consommateur(cle_api: str = Header(...)):
    """
    Obtient la clé API hachée pour un consommateur.

    Parameters:
    - `cle_api` (header): Clé API fournie par le consommateur.

    Returns:
    - Clé API hachée si la correspondance est trouvée.

    Raises:
    - HTTPException(401): En cas de clé API invalide.
    """
    try :
        cle_hachee = ClesApiService().trouver_cle_api("Consommateur", cle_api)
    except ValueError as e:
        raise HTTPException(status_code = 401, detail = str(e))
    return cle_hachee

def get_cle_consommateur_ou_administateur(cle_api: str = Header(...)):
    """
    Obtient la clé API pour un consommateur (hachée) ou un administrateur.

    Parameters:
    - `cle_api` (header): Clé API fournie par le consommateur ou l'administrateur.

    Returns:
    - Clé API de l'administrateur si la correspondance est trouvée, sinon la clé API hachée du consommateur.

    Raises:
    - HTTPException(401): En cas de clé API invalide.
    """
    if cle_api == token_administrateur:
        return cle_api
    return get_cle_api_consommateur(cle_api)


def get_cle_api_fournisseur(cle_api: str = Header(...)):
    """
    Obtient la clé API hachée pour un fournisseur.

    Parameters:
    - `cle_api` (header): Clé API fournie par le fournisseur.

    Returns:
    - Clé API hachée si la correspondance est trouvée.

    Raises:
    - HTTPException(401): En cas de clé API invalide.
    """
    try :
        cle_hachee = ClesApiService().trouver_cle_api("Fournisseur", cle_api)
    except ValueError as e:
        raise HTTPException(status_code = 401, detail = str(e))
    return cle_hachee

def get_cle_fournisseur_ou_administateur(cle_api: str = Header(...)):
    """
    Obtient la clé API pour un fournisseur (hachée) ou un administrateur.

    Parameters:
    - `cle_api` (header): Clé API fournie par le fournisseur ou l'administrateur.

    Returns:
    - Clé API de l'administrateur si la correspondance est trouvée, sinon la clé API hachée du fournisseur.

    Raises:
    - HTTPException(401): En cas de clé API invalide.
    """
    if cle_api == token_administrateur:
        return cle_api
    return get_cle_api_fournisseur(cle_api)

def get_liens_api():
    """
    Vérifie l'état des liens avec les API ElectricityMap et Nominatim.openstreetmap.

    Returns:
    - True si les liens sont établis avec succès.

    Raises:
    - HTTPException(503): En cas d'échec de connexion avec l'une des API.
    """
    if not EtatService().lien_api_electricity_map():
        raise HTTPException(status_code = 503, detail = "Lien avec l'API ElectricityMap impossible")
    if not EtatService().lien_api_nominatim_openstreetmap():
        raise HTTPException(status_code = 503, detail = "Lien avec l'API Nominatim.openstreetmap impossible")
    return True

@app.get("/")
def root():
    """
    Accueil de l'API GreenStream.

    Returns:
    - Message de bienvenue et lien vers la documentation.
    """
    return {"message" : "Bienvenue sur GreenStream",
            "documentation" : "http://127.0.0.1:8000/docs#/"}

@app.get("/etat-fonctionnement")
async def get_etat_fonctionnement():
    """
    Obtient l'état actuel de fonctionnement de l'API.

    Returns:
    - Un dictionnaire contenant l'état actuel de l'API, indiquant si elle fonctionne normalement ou en mode réduit, avec la liste des endpoints accessibles dans chaque cas.
    """
    if get_liens_api():
        return {
            'etat': 'ok', 
            'accessible': ["/serveurs", "/serveurs-eligibles/simulation", "/serveurs-optimaux/simulation",
            "/empreinte-carbone/simulation", "/empreinte-carbone/moyenne", "/empreinte-carbone/total", "/historique-empreinte",
            "/historique-empreinte/supprimer"]}
    return {
        'etat': 'mode reduit', 
        'accessible': ["/serveurs", "/empreinte-carbone/moyenne", "/empreinte-carbone/total", "/historique-empreinte",
            "/historique-empreinte/supprimer"]}
    

@app.post("/generer-cle")
async def generer_cle_api(type_utilisateur: Utilisateur, cle_api: str = Header(...)):
    """
    Génère une nouvelle clé API pour un fournisseur ou un consommateur de VOD.

    Parameters:
    - `type_utilisateur` (query): Type de l'utilisateur pour lequel la clé est générée.
    
    - `cle_api_administrateur` (header): Clé API de l'administrateur pour l'autorisation.

    Possible values:
    - `type_utilisateur`: "Fournisseur", "Consommateur".

    Returns:
    - Nouvelle clé API générée et enregistrée ainsi que le type et l'identifiant d'utilisateur.

    Raises:
    - HTTPException(401): En cas de clé API invalide.
    """
    if cle_api != token_administrateur:
        raise HTTPException(status_code = 401, detail = message)
    nouvelle_cle = ClesApiService().generer_cle_api(type_utilisateur)
    return nouvelle_cle

@app.get("/serveurs", dependencies = [Depends(get_cle_fournisseur_ou_administateur)])
async def get_serveurs(fournisseurs_cloud: FournisseurCloud = FournisseurCloud.AWS_GCP_Azure):
    """
    Obtenez la liste des serveurs en fonction des fournisseurs cloud.

    Parameters:
    - `fournisseurs_cloud` (query, facultatif): Liste des fournisseurs cloud à considérer, par défaut "(AWS, GCP, Azure)".

    Possible values:
    - `fournisseurs_cloud`: "(AWS, GCP, Azure)", "(AWS, GCP)", "(AWS, Azure)", "(GCP, Azure)", "AWS", "GCP", "Azure".

    Returns:
    - Liste des serveurs au format JSON.
    """
    list_serveurs = ServeursService().voir(fournisseurs_cloud.to_list())
    list_model = [ServeurModel(id_serveur = instance.id_serveur, nom = instance.nom,
                               code_region = instance.code_region,
                               fournisseur_cloud = instance.fournisseur_cloud, 
                               localisation = ZoneGeographiqueModel(ville = instance.localisation.ville)) for instance in list_serveurs]
    return jsonable_encoder(list_model, exclude_none = True)

@app.get("/serveurs-eligibles/simulation", dependencies = [Depends(get_cle_api_fournisseur), Depends(get_liens_api)])
async def get_serveurs_eligibles(ville: str, pays: str = None, fournisseurs_cloud: FournisseurCloud = FournisseurCloud.AWS_GCP_Azure):
    """
    Obtenez la liste des serveurs éligibles en fonction des fournisseurs cloud et de la localisation.

    Parameters:
    - `ville` (query): Nom de la ville.

    - `pays` (query, facultatif): Nom du pays.

    - `fournisseurs_cloud` (query, facultatif): Liste des fournisseurs cloud à considérer, par défaut "(AWS, GCP, Azure)".

    - `cle_api` (header): Clé API d'un fournisseur de VOD pour l'autorisation.

    Possible values:
    - `fournisseurs_cloud`: "(AWS, GCP, Azure)", "(AWS, GCP)", "(AWS, Azure)", "(GCP, Azure)", "AWS", "GCP", "Azure".

    Returns:
    - Liste des serveurs éligibles au format JSON.

    Raises:
    - HTTPException(404): Non reconnaissance de la ville par Openstreetmap ou non accès aux données d'Electricty Map.
    """
    lieu = ZoneGeographique(ville, pays)
    try :
        list_serveurs = OffreCloudService().serveurs_eligibles(lieu, fournisseurs_cloud.to_list())
    except ValueError as e:
        raise HTTPException(status_code = 404, detail = str(e))
    list_model = [ServeurModel(id_serveur = instance.id_serveur, nom = instance.nom,
                               code_region = instance.code_region,
                               fournisseur_cloud = instance.fournisseur_cloud, 
                               localisation = ZoneGeographiqueModel(ville = instance.localisation.ville)) for instance in list_serveurs]
    return jsonable_encoder(list_model, exclude_none = True)

@app.get("/serveurs-optimaux/simulation", dependencies = [Depends(get_cle_api_fournisseur), Depends(get_liens_api)])
async def get_serveurs_optimaux(duree: int, ville: str, pays: str = None, 
    date_visionnage: datetime = datetime.now(),
    fournisseurs_cloud: FournisseurCloud = FournisseurCloud.AWS_GCP_Azure):
    """
    Obtenez un dictionnaire des serveurs optimaux associés avec l'impact de la consommation électrique en gCO2eq/kWh prévisionnel en fonction des fournisseurs, de la durée, de la localisation, et de la date de visionnage.

    Parameters:
    - `duree` (query): Durée de visionnage en minutes.

    - `ville` (query): Nom de la ville.

    - `pays` (query, facultatif): Nom du pays.

    - `date_visionnage` (query, facultatif): Date de visionnage au format datetime, par défaut datetime.now().

    - `fournisseurs_cloud` (query, facultatif): Liste des fournisseurs cloud à considérer, par défaut "(AWS, GCP, Azure)".

    - `cle_api` (header): Clé API d'un fournisseur de VOD pour l'autorisation.

    Possible values:
    - `fournisseurs_cloud`: "(AWS, GCP, Azure)", "(AWS, GCP)", "(AWS, Azure)", "(GCP, Azure)", "AWS", "GCP", "Azure".

    Returns:
    - Dictionnaire ordonnée des serveurs optimaux associés à leur impact de la consommation électrique prévisionel en gCO2eq/kWh au format JSON.

    Raises:
    - HTTPException(404): Non reconnaissance de la ville par Openstreetmap ou non accès aux données d'Electricty Map.
    """
    lieu = ZoneGeographique(ville, pays)
    try :
        dict_serveurs = OffreCloudService().serveurs_optimaux(lieu, duree, date_visionnage, fournisseurs_cloud.to_list())
    except ValueError as e:
        raise HTTPException(status_code = 404, detail = str(e))
    list_model = [ServeurModel(id_serveur = key.id_serveur, nom = key.nom, 
                               code_region = key.code_region,
                               fournisseur_cloud = key.fournisseur_cloud,
                               localisation = ZoneGeographiqueModel(ville = key.localisation.ville),
                               impact_carbone = value) for key, value in dict_serveurs.items()]
    return jsonable_encoder(list_model, exclude_none = True)

@app.get("/empreinte-carbone/simulation", dependencies = [Depends(get_cle_api_consommateur), Depends(get_liens_api)])
async def get_empreinte_carbone(
    duree : int, resolution : Resolution, type_connexion : TypeConnexion, materiel : Materiel, ville: str, pays: str = None,
    date_visionnage : datetime = datetime.now(),
    cle_api_hache: str = Depends(get_cle_api_consommateur)
    ):
    """
    Obtenez l'empreinte carbone en fonction de la durée, de la résolution, du type de connexion, du matériel, de la localisation et de la date de visionnage.

    Parameters:
    - `duree` (query): Durée de visionnage en minutes.

    - `resolution` (query): Résolution de la vidéo.

    - `type_connexion` (query): Type de connexion.

    - `materiel` (query): Matériel utilisé.

    - `ville` (query): Nom de la ville.

    - `pays` (query, facultatif): Nom du pays.

    - `date_visionnage` (query, facultatif): Date de visionnage au format datetime, par défaut datetime.now().

    - `cle_api` (header): Clé API d'un consommateur pour l'autorisation.

    Possible values:
    - `resolution`: "240", "360", "480", "720", "1080", "1440", "2160", "4320".

    - `type_connexion`: "Wifi", "Reseau", "Cable".

    - `materiel`: "Ordinateur", "Mobile".

    Returns:
    - Empreinte carbone en gCO2eq et informations sur la vidéo au format JSON.

    Raises:
    - HTTPException(404): Non reconnaissance de la ville par Openstreetmap ou non accès aux données d'Electricty Map.
    """
    lieu = ZoneGeographique(ville, pays)
    donnees = InfoVideo(duree, resolution, type_connexion, materiel, lieu, date_visionnage)
    try :
        empreinte = EmpreinteCarboneService().empreinte_carbone(donnees, cle_api_hache)
    except ValueError as e:
        raise HTTPException(status_code = 404, detail = str(e))
    result = {
        "info_video": InfoVideoModel(duree = duree, resolution = resolution, type_connexion = type_connexion,
                            materiel = materiel, date_visionnage = date_visionnage,
                            localisation = ZoneGeographiqueModel(ville = ville, pays = pays)),
        "empreinte_carbone": empreinte
    }
    return jsonable_encoder(result, exclude_none = True)

@app.get("/empreinte-carbone/moyenne", dependencies = [Depends(get_cle_api_consommateur)])
async def get_empreinte_moyenne(cle_api_hache: str = Depends(get_cle_api_consommateur)):
    """
    Obtenez l'empreinte carbone moyenne en fonction de la clé API consommateur.

    Parameters:
    - `cle_api` (header): Clé API d'un consommateur pour l'autorisation.

    Returns:
    - Empreinte carbone moyenne en gCO2eq au format JSON.
    """
    empreinte = EmpreinteCarboneService().empreinte_moyenne(cle_api_hache)
    result = {"empreinte_carbone_moyenne": empreinte}
    return result

@app.get("/empreinte-carbone/total", dependencies = [Depends(get_cle_api_consommateur)])
async def get_empreinte_total(cle_api_hache: str = Depends(get_cle_api_consommateur)):
    """
    Obtenez l'empreinte carbone totale en fonction de la clé API consommateur.

    Parameters:
    - `cle_api` (header): Clé API d'un consommateur pour l'autorisation.

    Returns:
    - Empreinte carbone totale en gCO2eq au format JSON.
    """
    empreinte = EmpreinteCarboneService().empreinte_total(cle_api_hache)
    result = {"empreinte_carbone_totale": empreinte}
    return result

@app.get("/historique-empreinte", dependencies = [Depends(get_cle_consommateur_ou_administateur)])
async def get_historique_consommateur(cle_api: str = Depends(get_cle_consommateur_ou_administateur), id_utilisateur: int = None):
    """
    Obtenez l'historique de l'empreinte carbone d'un consommateur ou de tous les consommateurs si clé administrateur.

    Parameters:
    - `id_utilisateur` (query, facultatif): identifiant d'un consommateur.

    - `cle_api` (header): Clé API consommateur ou administrateur.

    Returns:
    - Historique des requêtes empreintes carbones au format JSON.

    Raises:
    - HTTPException(404): Pas d'historique trouvé.
    """
    historique = HistoriqueConsommateurService().voir(cle_api = cle_api, id_utilisateur = id_utilisateur)
    if historique == []:
        raise HTTPException(status_code = 404, 
            detail = "L'historique du consommateur associé à l'utilisateur numéro {} n'existe pas".format(id_utilisateur))
    if cle_api != token_administrateur:
        list_model = [{
        "info_video": InfoVideoModel(duree = requete["duree"], resolution = requete["resolution"], type_connexion = requete["type_connexion"],
                            materiel = requete["materiel"], date_visionnage = requete["date_visionnage"],
                            localisation = ZoneGeographiqueModel(ville = requete["ville"], pays = requete["pays"])),
        "empreinte_carbone": requete["empreinte_carbone"],
        "date_requete": requete["date_requete"]
        } for requete in historique]
    else :
        list_model = [{"id_utilisateur": requete["id_utilisateur"], "cle_api_haché": requete["cle_api"],
        "info_video": InfoVideoModel(duree = requete["duree"], resolution = requete["resolution"], type_connexion = requete["type_connexion"],
                            materiel = requete["materiel"], date_visionnage = requete["date_visionnage"],
                            localisation = ZoneGeographiqueModel(ville = requete["ville"], pays = requete["pays"])),
        "empreinte_carbone": requete["empreinte_carbone"],
        "date_requete": requete["date_requete"]
        } for requete in historique]
    return jsonable_encoder(list_model, exclude_none = True)

@app.delete("/historique-empreinte/supprimer", dependencies = [Depends(get_cle_consommateur_ou_administateur)])
async def delete_historique_consommateur(cle_api: str = Depends(get_cle_consommateur_ou_administateur)):
    """
    Supprime l'historique de l'empreinte carbone d'un consommateur ou de tous les consommateurs si clé administrateur.

    Parameters:
    - `cle_api` (header): Clé API consommateur ou administrateur.

    Returns:
    - Message indiquant si la suppression a réussi.

    Raises:
    - HTTPException(404): Pas d'historique trouvé.
    """
    resultat = HistoriqueConsommateurService().supprimer(cle_api)
    if resultat:
        return {"message": "L'historique a bien été supprimé"}
    raise HTTPException(status_code = 404, detail = "L'historique associé à la clé API {} n'existe pas".format(id_utilisateur))

@app.get("/table-cles-api")
async def get_cles_api(cle_api: str = Header(...)):
    """
    Obtenez la table des clés API avec autorisation d'administrateur.

    Parameters:
    - `cle_api` (header): Clé API de l'administrateur pour l'autorisation.

    Returns:
    - Table des clés API au format JSON.

    Raises:
    - HTTPException(401): En cas de clé API invalide.
    """
    if cle_api != token_administrateur:
        raise HTTPException(status_code = 401, detail = message)
    return ClesApiService().voir()

@app.delete("/table-cles-api/supprimer")
async def delete_cles_api(id_utilisateur: int = None, cle_api: str = Header(...)):
    """
    Supprime la table des clés API ou seulement celle d'un utilisateur si spécifié.

    Parameters:
    - `id_utilisateur` (query, facultatif): identifiant d'un consommateur ou fournisseur de VOD.

    - `cle_api` (header): Clé API de l'administrateur pour l'autorisation.

    Returns:
    - Message indiquant si la suppression a réussi.

    Raises:
    - HTTPException(401): En cas de clé API invalide.

    - HTTPException(404): Pas de clé API trouvé.
    """
    if cle_api != token_administrateur:
        raise HTTPException(status_code = 401, detail = message)

    resultat = ClesApiService().supprimer(id_utilisateur = id_utilisateur)
    if id_utilisateur:
        if resultat:
            return {"message": "La clé d'api associé à l'utilisateur numéro {} été supprimé".format(id_utilisateur)}
        raise HTTPException(status_code = 404, detail = "La clé d'api associé à l'utilisateur numéro {} n'existe pas".format(id_utilisateur))
    return {"message": "La table des clés d'api a été supprimé"}

if __name__ == "__main__":
    uvicorn.run(app)