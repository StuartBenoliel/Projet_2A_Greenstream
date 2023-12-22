from InquirerPy import prompt

from view.vue_abstraite import VueAbstraite


class MenuConsommateurVue(VueAbstraite):
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
                "choices": ["Estimer son empreinte carbone", "Empreinte moyenne générée",
                            "Empreinte totale générée", "Voir son historique",
                            "Supprimer son historique", "Se déconnecter"],
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

        elif reponse["choix"] == "Estimer son empreinte carbone":
            from view.empreinte_carbone_vue import EmpreinteCarboneVue
            return EmpreinteCarboneVue(self.cle)

        elif reponse["choix"] == "Empreinte moyenne générée":
            from service.empreinte_carbone_service import EmpreinteCarboneService
            empreinte = EmpreinteCarboneService().empreinte_moyenne(self.cle)
            message = f'Votre empreinte carbone moyenne générée est de {empreinte} gCO2eq'
            return MenuConsommateurVue(self.cle, message)

        elif reponse["choix"] == "Empreinte totale générée":
            from service.empreinte_carbone_service import EmpreinteCarboneService
            empreinte = EmpreinteCarboneService().empreinte_total(self.cle)
            message = f'Votre empreinte carbone totale générée est de {empreinte} gCO2eq'
            return MenuConsommateurVue(self.cle, message)

        elif reponse["choix"] == "Voir son historique":
            from service.table.historique_consommateur_service import HistoriqueConsommateurService
            historique = HistoriqueConsommateurService().voir(self.cle)
            message = "Votre historique:\n\n"
            for requete in historique:
                date_requete = requete["date_requete"]
                empreinte = requete["empreinte_carbone"]
                ville = requete["ville"]
                date_visionnage = requete["date_visionnage"]
                duree = requete["duree"]
                resolution = requete["resolution"]
                type_connexion = requete["type_connexion"]
                materiel = requete["materiel"]
                message += f"Date Requête: {date_requete}, Empreinte Carbone: {empreinte} gCO2eq, Localisation: {ville}, Date Visionnage: {date_visionnage},\n Durée: {duree}, Résolution: {resolution}, Type de Connexion: {type_connexion}, Matériel: {materiel}\n\n"
            return MenuConsommateurVue(self.cle, message)

        elif reponse["choix"] == "Supprimer son historique":
            from service.table.historique_consommateur_service import HistoriqueConsommateurService

            resultat = HistoriqueConsommateurService().supprimer(self.cle)
            if resultat:
                return MenuConsommateurVue(self.cle, "Votre historique a bien été supprimé")
            return MenuConsommateurVue(self.cle, "Votre historique était déjà vide")
