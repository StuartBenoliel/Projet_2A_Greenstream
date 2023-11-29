import re
from dao.db_connection import DBConnection
from business_object.serveur_cloud import ServeurCloud
from business_object.zone_geographique import ZoneGeographique
from utils.singleton import Singleton

class ServeurDao(metaclass = Singleton):
    """
    Classe pour l'accès aux données des serveurs dans la base de données.

    Methods
    -------
    trouver_par_fournisseur_cloud(fournisseurs) -> list
        Récupère tous les serveurs appartenant aux fournisseurs cloud de la liste dans la base de données.
    """
    def trouver_par_fournisseur_cloud(self, fournisseurs: list) -> list:
        """
        Récupère tous les serveurs appartenant aux fournisseurs cloud de la liste dans la base de données.

        Parameters
        ----------
        fournisseur : list
            Liste des fournisseurs.

        Returns
        -------
        list
            Liste de tous les serveurs trouvés.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                                     "
                        "   FROM projet.regions_fournisseurs_cloud    "
                        "   WHERE fournisseur = ANY(%(fournisseurs)s);",
                        {"fournisseurs": fournisseurs},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            print(e)
            raise
        list_serveurs = []

        if res:
            for row in res:
                localisation = ZoneGeographique(row["ville"])
                list_serveur = re.findall(r"'(.*?)'", row["zone_disponibilite_em"])
                serveur = ServeurCloud(
                    id_serveur = row["identifiant"],
                    nom = row["nom"],
                    code_region = row["code_region"],
                    fournisseur_cloud = row["fournisseur"],
                    zone_disponibilite = list_serveur,
                    localisation = localisation)
                list_serveurs.append(serveur)

        return list_serveurs

if __name__ == "__main__":
    X = ServeurDao().trouver_par_fournisseur_cloud(["AWS", "Azure"])
    for i in range(len(X)):
        print(vars(X[i]))
