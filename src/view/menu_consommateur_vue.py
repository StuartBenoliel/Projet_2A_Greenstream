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
        super().__init__(message, cle)
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
            from view.empreinte_carbonne_vue import EmpreinteCarboneVue
            return EmpreinteCarboneVue()

        elif reponse["choix"] == "Empreinte moyenne générée":
            from service.empreinte_carbone_service import EmpreinteCarboneService
            empreinte = EmpreinteCarboneService().empreinte_moyenne(self.cle)
            message = f'Votre empreinte carbone moyenne générée est de {empreinte} gCO2eq'
            return MenuConsommateurVue(message)

        elif reponse["choix"] == "Empreinte totale générée":
            from service.empreinte_carbone_service import EmpreinteCarboneService
            empreinte = EmpreinteCarboneService().empreinte_total(self.cle)
            message = f'Votre empreinte carbone totale générée est de {empreinte} gCO2eq'
            return MenuConsommateurVue(message)

        elif reponse["choix"] == "Voir son historique":
            from service.table.historique_consommateur_service import HistoriqueConsommateurService
            historique = HistoriqueConsommateurService().voir(self.cle)
            list_model = [{
        "info_video": InfoVideoModel(duree = requete["duree"], resolution = requete["resolution"], type_connexion = requete["type_connexion"],
                            materiel = requete["materiel"], date_visionnage = requete["date_visionnage"],
                            localisation = ZoneGeographiqueModel(ville = requete["ville"], pays = requete["pays"])),
        "empreinte_carbone": requete["empreinte_carbone"],
        "date_requete": requete["date_requete"]
        } for requete in historique]
            return MenuConsommateurVue(list_model)

        elif reponse["choix"] == "Supprimer son historique":
            from service.table.historique_consommateur_service import HistoriqueConsommateurService

            resultat = HistoriqueConsommateurService().supprimer(self.cle)
            if resultat:
                return MenuConsommateurVue("L'historique a bien été supprimé")
            return MenuConsommateurVue("??????")
