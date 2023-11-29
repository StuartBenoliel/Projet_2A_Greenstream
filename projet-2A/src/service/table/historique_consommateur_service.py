from dao.historique_consommateur_dao import HistoriqueConsommateurDao
from service.table.abstract_table import AbstractTable
import os
from dotenv import load_dotenv

# Charge les variables d'environnement depuis le fichier .env
load_dotenv()

class HistoriqueConsommateurService(AbstractTable):
    def voir(self, cle_api: str, id_utilisateur: int | None = None, *args, **kwargs) -> list:
        """
        Renvoie la table de l'historique des consommateurs de VOD selon l'utilisateur.

        Parameters
        ----------
        cle_api : str
            Clé API pour filtrer les résultats.

        id_utilisateur : int | None, optional
            Identifiant d'un utilisateur connu uniquement par l'administrateur.

        Returns
        -------
        list
            Table de l'historique des consommateurs si administrateur sinon l'historique d'un consommateur donné.
        """
        if cle_api == (os.environ.get('token_admin')):
            if id_utilisateur:
                    return HistoriqueConsommateurDao().trouver_par_id_utilisateur(id_utilisateur)
            return HistoriqueConsommateurDao().trouver_tout()
        return HistoriqueConsommateurDao().trouver_par_cle_api(cle_api)

    def supprimer(self, cle_api: str, *args, **kwargs) -> bool:
        """
        Supprime l'historique du consommateur de VOD donné ou de tous si administrateur.

        Parameters
        ----------
        cle_api : str
            Clé API pour filtrer les résultats.

        Returns
        -------
        bool
            True si la suppression est réussie, False sinon.
        """
        if cle_api == (os.environ.get('token_admin')):
            return HistoriqueConsommateurDao().supprimer_tout()
        return HistoriqueConsommateurDao().supprimer(cle_api)