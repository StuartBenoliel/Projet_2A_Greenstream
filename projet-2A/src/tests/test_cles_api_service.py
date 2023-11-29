import unittest
from service.table.cles_api_service import ClesApiService
import os
from dotenv import load_dotenv

# Charge les variables d'environnement depuis le fichier .env
load_dotenv()

class TestClesApiService(unittest.TestCase):

    def setUp(self):
        self.service = ClesApiService()
        self.type_utilisateur = "Fournisseur"
        self.cle_api_administrateur = (os.environ.get('token_admin'))
        self.cle_api_utilisateur = "user_api_key"

    @patch('dao.table_cles_api_dao.TableClesAPIDao.existe')
    @patch('dao.table_cles_api_dao.TableClesAPIDao.creer')
    @patch('os.environ.get')
    def test_generer_cle_api(self, mock_os_environ_get, mock_creer, mock_existe):
        mock_os_environ_get.return_value = self.cle_api_administrateur
        mock_existe.return_value = False
        cle_api = self.service.generer_cle_api(self.type_utilisateur, self.cle_api_administrateur)
        self.assertIsNotNone(cle_api)
        self.assertNotEqual(cle_api, "Mauvais token")
        self.assertNotEqual(cle_api, "Mauvais utilisateur")
        mock_creer.assert_called_once()

    @patch('dao.table_cles_api_dao.TableClesAPIDao.trouver_par_type_utilisateur')
    def test_trouver_cle_api_consommateur(self, mock_trouver_par_type_utilisateur):
        mock_trouver_par_type_utilisateur.return_value = ["hashed_api_key"]
        cle_api_trouvee = self.service.trouver_cle_api_consommateur(self.cle_api_utilisateur)
        self.assertIsNone(cle_api_trouvee)  

    @patch('dao.table_cles_api_dao.TableClesAPIDao.trouver_par_type_utilisateur')
    def test_trouver_cle_api_fournisseur(self, mock_trouver_par_type_utilisateur):
        mock_trouver_par_type_utilisateur.return_value = ["hashed_api_key"]
        cle_api_trouvee = self.service.trouver_cle_api_fournisseur(self.cle_api_utilisateur)
        self.assertIsNone(cle_api_trouvee)  
        
if __name__ == '__main__':
    unittest.main()
  