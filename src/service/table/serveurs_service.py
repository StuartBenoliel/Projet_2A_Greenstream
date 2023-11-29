from dao.serveur_dao import ServeurDao
from service.table.abstract_table import AbstractTable

class ServeursService(AbstractTable):
    def voir(self, fournisseurs_cloud: list, *args, **kwargs) -> list:
        """
        Renvoie la table des serveurs en fonction des fournisseurs cloud spécifiés.

        Parameters
        ----------
        fournisseurs_cloud : list
            Liste des fournisseurs cloud.

        Returns
        -------
        list
            Liste des serveurs en fonction des fournisseurs spécifiés.
        """
        return ServeurDao().trouver_par_fournisseur_cloud(fournisseurs_cloud)

    def supprimer(self, *args, **kwargs):
        """
        Pas de suppression autorisée
        """
        pass
    