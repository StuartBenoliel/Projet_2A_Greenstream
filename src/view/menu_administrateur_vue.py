from InquirerPy import prompt

from view.vue_abstraite import VueAbstraite


class MenuAdministrateurVue(VueAbstraite):
    """Vue du menu du joueur

    Attributes
    ----------
    message=''
        str

    Returns
    ------
    view
        retourne la prochaine vue, celle qui est choisi par l'utilisateur de l'application
    """

    def __init__(self, cle, message="") -> None:
        self.cle = cle
        super().__init__(message)
        self.questions = [
            {
                "type": "list",
                "name": "choix",
                "message": "Faites votre choix",
                "choices": ["Voir la liste de serveurs", "Voir l'historique", "Supprimer l'historique",
                            "Voir la table des clés", "Supprimer la table des clés", "Se déconnecter"],
            }
        ]

    def choisir_menu(self):
        """Choix du menu suivant de l'utilisateur

        Return
        ------
        vue
            Retourne la vue choisi par l'utilisateur dans le terminal
        """
        reponse = prompt(self.questions)

        if reponse["choix"] == "Se déconnecter":
            from view.accueil_vue import AccueilVue
            return AccueilVue()

        elif reponse["choix"] == "Voir la liste de serveurs":
            from view.serveurs_vue import ServeursVue
            return ServeursVue(self.cle)

        elif reponse["choix"] == "Voir l'historique":
            from service.table.historique_consommateur_service import HistoriqueConsommateurService
            historique = HistoriqueConsommateurService().voir(self.cle)
            message = "L'historique:\n\n"
            for requete in historique:
                id_utilisateur = requete["id_utilisateur"]
                cle = requete["cle_api"]
                date_requete = requete["date_requete"]
                empreinte = requete["empreinte_carbone"]
                ville = requete["ville"]
                date_visionnage = requete["date_visionnage"]
                duree = requete["duree"]
                resolution = requete["resolution"]
                type_connexion = requete["type_connexion"]
                materiel = requete["materiel"]
                message += f"Id Utilisateur: {id_utilisateur}, Clé API Hachée: {cle}, Date Requête: {date_requete}, Empreinte Carbone: {empreinte} gCO2eq,\n Localisation: {ville}, Date Visionnage: {date_visionnage}, Durée: {duree}, Résolution: {resolution}, Type de Connexion: {type_connexion}, Matériel: {materiel}\n\n"
            return MenuAdministrateurVue(self.cle, message)

        elif reponse["choix"] == "Supprimer l'historique":
            from service.table.historique_consommateur_service import HistoriqueConsommateurService
            resultat = HistoriqueConsommateurService().supprimer(self.cle)
            if resultat:
                return MenuAdministrateurVue(self.cle, "L'historique a bien été supprimé")
            return MenuAdministrateurVue(self.cle, "L'historique était déjà vide")

        elif reponse["choix"] == "Voir la table des clés":
            from service.table.cles_api_service import ClesApiService
            resultat = ClesApiService().voir()
            message = "La table des clés API :\n\n"
            for row in resultat:
                id_utilisateur = row['id_utilisateur']
                cle_api = row['cle_api']
                type_utilisateur = row['type_utilisateur']
                message += f"Id Utilisateur: {id_utilisateur}, Clé API: {cle_api}, Type Utilisateur: {type_utilisateur}\n"
            return MenuAdministrateurVue(self.cle, message)

        elif reponse["choix"] == "Supprimer la table des clés":
            from service.table.cles_api_service import ClesApiService
            resultat = ClesApiService().supprimer()
            if resultat:
                return MenuAdministrateurVue(self.cle, "La table des clés a bien été supprimé")
            return MenuAdministrateurVue(self.cle, "La table des clés était déjà vide")
