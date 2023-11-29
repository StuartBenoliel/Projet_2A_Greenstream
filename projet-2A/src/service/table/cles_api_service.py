from dao.cles_api_dao import ClesAPIDao
from service.table.abstract_table import AbstractTable
import os
import secrets
import bcrypt
from dotenv import load_dotenv

load_dotenv()

class ClesApiService(AbstractTable):
    def voir(self, *args, **kwargs) -> list:
        """
        Renvoie la table des clés API.

        Returns
        -------
        list
            Liste des clés API.
        """
        return ClesAPIDao().trouver_tout()

    def supprimer(self, id_utilisateur: int | None = None, *args, **kwargs) -> bool:
        """
        Supprime la table des clés API ou d'un utilisateur particulier.

        Parameters
        ----------
        id_utilisateur : int | None, optional
            Identifiant d'un utilisateur connu uniquement par l'administrateur.

        Returns
        -------
        bool
            True si la suppression est réussie, False sinon.
        """
        if id_utilisateur:
                return ClesAPIDao().supprimer(id_utilisateur)
        return ClesAPIDao().supprimer_tout()

    def generer_cle_api(self, type_utilisateur: str) -> dict:
        """
        Génère une nouvelle clé API pour un fournisseur ou un consommateur de VOD.

        Parameters
        ----------
        type_utilisateur : str
            Type de l'utilisateur pour lequel la clé est générée.
            Possible values: "Fournisseur", "Consommateur".

        Returns
        -------
        dict
            Nouvelle clé API générée et enregistrée ainsi que le type et l'identifiant d'utilisateur.
        """
        if type_utilisateur not in ["Fournisseur", "Consommateur"]:
            raise ValueError("Mauvais utilisateur")

        while True:
            nouvelle_cle = secrets.token_urlsafe(32)
            cle_hache = bcrypt.hashpw(nouvelle_cle.encode("utf-8"), bcrypt.gensalt())

            # Vérification de l'unicité de la clé API hachée dans la table
            if not ClesAPIDao().existe_cle(cle_hache.decode("utf-8")) and nouvelle_cle != (os.environ.get('token_admin')) and cle_hache.decode("utf-8") != (os.environ.get('token_admin')):
                break

        result = ClesAPIDao().creer(cle_hache.decode("utf-8"), type_utilisateur)
        result["cle_api"] = nouvelle_cle
        return result

    def trouver_cle_api(self, type_utilisateur: str, cle_api: str) -> str:
        """
        Obtient la clé API hachée d'un consommateur ou fournisseur.

        Parameters
        ----------
        type_utilisateur : str
            Type de l'utilisateur pour lequel la clé est cherchée.
            Possible values: "Fournisseur", "Consommateur"

        cle_api : str
            Clé API fournie par le consommateur ou le fournissseur.

        Returns
        -------
        str
            Clé API hachée si la correspondance est trouvée.
        """
        if type_utilisateur not in ["Fournisseur", "Consommateur"]:
            raise ValueError("Mauvais utilisateur")
            
        cles_api_haches = ClesAPIDao().trouver_par_type_utilisateur(type_utilisateur)

        # Vérifiez si la clé API fournie correspond à l'une des clés API hachées
        for cle_hache in cles_api_haches:
            if bcrypt.checkpw(cle_api.encode("utf-8"), cle_hache.encode("utf-8")):
                return cle_hache
        raise ValueError("Clé API invalide")
