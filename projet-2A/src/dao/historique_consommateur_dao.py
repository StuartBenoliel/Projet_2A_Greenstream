from dao.db_connection import DBConnection
from dao.cles_api_dao import ClesAPIDao
from business_object.info_video import InfoVideo
from utils.singleton import Singleton
from datetime import datetime


class HistoriqueConsommateurDao(metaclass = Singleton):
    """
    Classe pour l'accès aux données de l'historique des simulations d'empreinte carbone des consommateurs de VOD.

    Methods
    -------
    creer(donnee, empreinte, cle_api) -> bool
        Enregistre une estimation dans la base de données.

    trouver_par_id_utilisateur(id_utilisateur) -> list
        Trouve les enregistrements d'historique par l'identifiant utilisateur.

    trouver_par_cle_api(cle_api) -> list
        Trouve les enregistrements d'historique de consommation pour une clé API donnée.

    trouver_empreinte_par_cle_api(cle_api) -> list
        Trouve les enregistrements d'empreintes carbone pour une clé API donnée.

    trouver_tout() -> list
        Récupère tous les enregistrements d'historique des consommateurs de VOD.

    supprimer(cle_api) -> bool
        Supprime des enregistrements d'historique associés à une clé API.

    supprimer_tout() -> bool
        Supprime tous les enregistrements d'historique des consommateurs de VOD.
    """
    def creer(self, donnees: InfoVideo, empreinte: float, cle_api: str) -> bool:
        """
        Crée une estimation dans la base de données.

        Parameters
        ----------
        donnee : InfoVideo
            Objet représentant les paramètres de visionnage de la video.
        empreinte : float
            Empreinte carbone associée à la consommation.
        cle_api : str
            Clé API du consommateur de VOD.

        Returns
        -------
        bool
            True si la création est un succès, False sinon.
        """
        res = None
        date_requete = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        id_utilisateur = ClesAPIDao().trouver_id_par_cle(cle_api)
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO projet.historique_consommateur(                                                         "
                        "    id_utilisateur, cle_api, date_requete, duree, date_visionnage,                                  "
                        "    resolution, type_connexion, materiel, empreinte_carbone, ville, pays)                           "
                        "   VALUES (                                                                                         "
                        "       %(id_utilisateur)s, %(cle_api)s, %(date_requete)s, %(duree)s, %(date_visionnage)s,           "
                        "       %(resolution)s, %(type_connexion)s, %(materiel)s, %(empreinte_carbone)s, %(ville)s, %(pays)s)"
                        "RETURNING cle_api, date_requete;                                                                    ",
                        {
                            "id_utilisateur": id_utilisateur,
                            "cle_api": cle_api,
                            "date_requete": date_requete,
                            "duree": donnees.duree,
                            "date_visionnage": donnees.date_visionnage,
                            "resolution": donnees.resolution,
                            "type_connexion": donnees.type_connexion,
                            "materiel": donnees.materiel,
                            "empreinte_carbone" : empreinte,
                            "ville" : donnees.localisation.ville,
                            "pays" : donnees.localisation.pays
                        },
                        )
                    res = cursor.fetchone()
        except Exception as e:
            print(e)
            raise

        if res:
            return cle_api == res["cle_api"] and date_requete == str(res["date_requete"])

        return False

    def trouver_par_id_utilisateur(self, id_utilisateur: int) -> list:
        """
        Trouve les enregistrements d'historique par l'identifiant utilisateur.

        Parameters
        ----------
        id_utilisateur : int
            id du consommateur de VOD.

        Returns
        -------
        list
            Liste des enregistrements d'historique de consommation trouvés.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                                           "
                        "  FROM projet.historique_consommateur              "
                        " WHERE id_utilisateur = %(id_utilisateur)s;        ",
                        {"id_utilisateur": id_utilisateur},
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

    def trouver_par_cle_api(self, cle_api: str) -> list:
        """
        Trouve les enregistrements d'historique par une clé API.

        Parameters
        ----------
        cle_api : str
            Clé API du consommateur de VOD.

        Returns
        -------
        list
            Liste des enregistrements d'historique de consommation trouvés.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT date_requete, duree, date_visionnage, resolution, type_connexion, "
                        "       materiel, empreinte_carbone, ville, pays                          "
                        "   FROM projet.historique_consommateur                                   "             
                        "   WHERE cle_api = %(cle_api)s;                                          ",
                        {"cle_api": cle_api},
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

    def trouver_empreinte_par_cle_api(self, cle_api: str) -> list:
        """
        Trouve les empreintes carbone enregistrés pour une clé API.

        Parameters
        ----------
        cle_api : str
            Clé API du consommateur de VOD.

        Returns
        -------
        list
            Liste des empreintes carbone trouvées.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT empreinte_carbone              "
                        "   FROM projet.historique_consommateur"
                        "   WHERE cle_api = %(cle_api)s;       ",
                        {"cle_api": cle_api},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            print(e)
            raise

        list_empreinte = []
        if res:
            list_empreinte = [row['empreinte_carbone'] for row in res]

        return list_empreinte

    def trouver_tout(self) -> list:
        """
        Récupère tous les enregistrements d'historique.

        Returns
        -------
        list
            Liste de tous les enregistrements d'historique des consommateurs de VOD.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                               "
                        "   FROM projet.historique_consommateur;",
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

    def supprimer(self, cle_api: str) -> bool:
        """
        Supprime les enregistrements d'historique d'une clé API.

        Parameters
        ----------
        cle_api : str
            Clé API du consommateur de VOD.

        Returns
        -------
        bool
            True si la suppression est un succès, False sinon.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM projet.historique_consommateur"
                        "   WHERE cle_api = %(cle_api)s;           ",
                        {"cle_api": cle_api},
                    )
                    res = cursor.rowcount
        except Exception as e:
            print(e)
            raise

        return res > 0

    def supprimer_tout(self) -> bool:
        """
        Supprime tous les enregistrements d'historique.

        Returns
        -------
        bool
            True si la suppression est un succès, False sinon.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM projet.historique_consommateur;"
                    )
                    res = cursor.rowcount
        except Exception as e:
            print(e)
            raise

        return res > 0
 