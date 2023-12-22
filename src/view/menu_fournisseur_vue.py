from InquirerPy import prompt

from view.vue_abstraite import VueAbstraite


class MenuFournisseurVue(VueAbstraite):
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
                "choices": ["Voir la liste de serveurs",
                            "Voir les serveurs optimaux conseillés par Greenstream", "Se déconnecter"],
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

        elif reponse["choix"] == "Voir les serveurs optimaux conseillés par Greenstream":
            from view.offre_cloud_vue import OffreCloudVue
            return OffreCloudVue(self.cle)
