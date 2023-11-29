from utils.singleton import Singleton
from dao.db_connection import DBConnection
import os
import pandas as pd
from sqlalchemy import create_engine, text
import dotenv

class TraitementDatabase(metaclass = Singleton):
    """
    Cette classe gère la ré-initialisation de la base de données et le traitement des données des fournisseurs de régions.

    Methods
    -------
    lancer()
        Ré-initialise la base de données en exécutant le script SQL d'initialisation.

    traitement_regions_fournisseur()
        Effectue le traitement des données du csv regions_fournisseurs-cloud.
    """

    def lancer(self):
        """
        Ré-initialise la base de données en exécutant le script SQL d'initialisation.
        """
        print("Ré-initialisation de la base de données")

        init_db = open("data/init_db.sql", encoding = "utf-8")
        init_db_as_string = init_db.read()

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(init_db_as_string)
        except Exception as e:
            print(e)
            raise

        dotenv.load_dotenv(override = True)
        HOST = os.environ["HOST"]
        PORT = os.environ["PORT"]
        DATABASE = os.environ["DATABASE"]
        USER = os.environ["DB_USER"]
        PASSWORD = os.environ["PASSWORD"]

        df = pd.read_csv('./data/regions_fournisseurs-cloud.csv', delimiter = ';', encoding = "utf-8")

        # Supprimer la colonne "zone_Disponibilite"
        if 'zone_disponibilite' in df.columns:
            df = df.drop(columns = ['zone_disponibilite'])

        connection_string = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

        # Créez une connexion à la base de données en utilisant SQLAlchemy
        engine = create_engine(connection_string)

        # Écrivez le DataFrame dans la base de données en tant que table
        df.to_sql('regions_fournisseurs_cloud', engine, schema = "projet", if_exists = 'replace', index = False)

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "ALTER TABLE projet.regions_fournisseurs_cloud"
                        "   ADD PRIMARY KEY (identifiant);            ",
                        )
        except Exception as e:
            print(e)
            raise

        print("Ré-initialisation de la base de données - Terminée")

        return True

    def traitement_regions_fournisseur(self):
        """
        Effectue le traitement des données du csv regions_fournisseurs-cloud.
        """
        df = pd.read_csv('data/regions_fournisseurs-cloud.csv', delimiter = ';', encoding = "utf-8")

        # Appliquer la fonction strip() pour supprimer les espaces inutiles dans la colonne
        df["Identifiant"] = df["Identifiant"].str.strip()
        df["Nom"] = df['Nom'].str.strip()
        df["Fournisseur"] = df['Fournisseur'].str.strip()
        df["Zone_Disponibilite"] = df['Zone_Disponibilite'].str.strip()
        df["Code_Region"] = df['Code_Region'].str.strip()
        df["Ville"] = df['Ville'].str.strip()
        df["Zone_Disponibilite_EM"] = df['Zone_Disponibilite_EM'].str.strip()

        df.columns = df.columns.str.lower()
        # Enregistrer les modifications dans un nouveau fichier CSV
        df.to_csv("data/regions_fournisseurs-cloud.csv", sep = ';', index = False)

if __name__ == "__main__":
    TraitementDatabase().lancer()
