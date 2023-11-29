from business_object.zone_geographique import ZoneGeographique

class ServeurCloud:
    """
    Classe représentant un serveur cloud.

    Attributes
    ----------
    id_serveur : str
        L'identifiant unique du serveur.
    nom : str
        Le nom du serveur.
    code_region : str
        Le code de la région où le serveur est situé.
    fournisseur_cloud : str
        Le fournisseur de services cloud associé au serveur.
    zone_disponibilite : list[str]
        La liste des zones de disponibilité du serveur.
    localisation : ZoneGeographique
        L'objet représentant la localisation géographique du serveur.

    Methods
    -------
    __repr__()
        Retourne une représentation simplifié sous forme de chaîne de caractères du serveur.
    """
    def __init__(self, id_serveur : str, nom : str, code_region : str, fournisseur_cloud : str,
                zone_disponibilite : list[str], localisation : ZoneGeographique):
        self.id_serveur = id_serveur
        self.nom = nom
        self.code_region = code_region
        self.fournisseur_cloud = fournisseur_cloud
        self.zone_disponibilite = zone_disponibilite
        self.localisation = localisation

    def __repr__(self):
        return f"ServeurCloud[id_serveur = '{self.id_serveur}', nom = '{self.nom}', localisation = '{self.localisation}']"