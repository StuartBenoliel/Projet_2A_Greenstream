from dao.db_connection import DBConnection
from utils.singleton import Singleton

class ClesAPIDao(metaclass = Singleton):
    """
    Classe pour l'accès aux clés API dans la base de données.

    Methods
    -------
    creer(cle_api, type_utilisateur) -> bool
        Crée une clé API dans la base de données.

    existe_cle(cle_api) -> bool
        Vérifie si une clé API existe déjà dans la table.

    trouve_id_par_cle(cle_api) -> int
        Renvoie l'identifiant de l'utilisateur associé à la clé.

    trouver_par_type_utilisateur(type_utilisateur) -> list
        Trouve les clés API par type d'utilisateur.

    trouver_tout() -> list
        Récupère toutes les clés API dans la base de données.

    supprimer(id_utilisateur) -> bool:
        Supprime une clé API via l'identifiant de l'utilisateur.

    supprimer_tout() -> bool
        Supprime toutes les clés API enregistrés.
    """
    def creer(self, cle_api: str, type_utilisateur: str) -> bool:
        """
        Crée une clé API dans la base de données.

        Parameters
        ----------
        cle_api : str
            Clé API à créer.
        type_utilisateur : str
            Type d'utilisateur associé à la clé API.

        Returns
        -------
        bool 
            True si la création est un succès, False sinon.
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO projet.table_cles_api(cle_api, type_utilisateur)  "
                        "   VALUES (%(cle_api)s, %(type_utilisateur)s)                 "
                        "   RETURNING *;                                               ",
                        {"cle_api": cle_api, "type_utilisateur": type_utilisateur},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            print(e)
            raise

        if res and cle_api == res["cle_api"]:
            return res
        return False

    def existe_cle(self, cle_api: str) -> bool:
        """
        Vérifie si une clé API existe déjà dans la table.

        Parameters
        ----------
        cle_api : str
            Clé API à vérifier.

        Returns
        -------
        bool
            True si la clé API existe déjà, False sinon.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT COUNT(*) as count       "
                        "   FROM projet.table_cles_api  " 
                        "   WHERE cle_api = %(cle_api)s;",
                        {"cle_api": cle_api},
                    )
                    count = cursor.fetchone()["count"]
        
        except Exception as e:
            print(e)
            raise

        return count > 0

    def trouver_id_par_cle(self, cle_api: str) -> int:
        """
        Renvoie l'identifiant de l'utilisateur associé à la clé.

        Parameters
        ----------
        cle_api : str
            Clé API à chercher dans la table.

        Returns
        -------
        int
            le numéro de l'identifiant utilisateur.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_utilisateur          "
                        "   FROM projet.table_cles_api  "
                        "   WHERE cle_api = %(cle_api)s;",
                        {"cle_api": cle_api},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            print(e)
            raise

        if res:
            return res["id_utilisateur"]

        return res

    def trouver_par_type_utilisateur(self, type_utilisateur: str) -> list:
        """
        Trouve les clés API par type d'utilisateur.

        Parameters
        ----------
        type_utilisateur : str
            Type d'utilisateur pour lequel rechercher les clés API.

        Returns
        -------
        list
            Liste des clés API trouvées.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT cle_api                                   "
                        "   FROM projet.table_cles_api                    "
                        "   WHERE type_utilisateur = %(type_utilisateur)s;",
                        {"type_utilisateur": type_utilisateur},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            print(e)
            raise

        liste_cles = []

        if res:
            for row in res:
                liste_cles.append(row["cle_api"])

        return liste_cles

    def trouver_tout(self) -> list:
        """
        Récupère toutes les clés API dans la base de données.

        Returns
        -------
        list
            Liste de toutes les clés API.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                      "
                        "   FROM projet.table_cles_api;",
                    )
                    res = cursor.fetchall()
        except Exception as e:
            print(e)
            raise

        requetes = []
        if res:
            for row in res:
                requetes.append(row)

        return requetes

    def supprimer(self, id_utilisateur: int) -> bool:
        """
        Supprime une clé API via l'identifiant de l'utilisateur.

        Parameters
        ----------
        id_utilisateur : int
            Identifiant de l'utilisateur pour lequel on supprime sa clé.

        Returns
        -------
        bool
            True si la suppression est un succès, False sinon.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM projet.table_cles_api            "
                        "   WHERE id_utilisateur = %(id_utilisateur)s;",
                        {"id_utilisateur": id_utilisateur},
                    )
                    res = cursor.rowcount
        except Exception as e:
            print(e)
            raise

        return res > 0

    def supprimer_tout(self) -> bool:
        """
        Supprime toutes les clés API.

        Returns
        -------
        bool
            True si la suppression est un succès, False sinon.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM projet.table_cles_api;"
                    )
                    res = cursor.rowcount
        except Exception as e:
            print(e)
            raise

        return res > 0

