import unittest
from unittest.mock import patch
from datetime import datetime
from service.empreinte_carbone_service import EmpreinteCarboneService
from business_object.info_video import InfoVideo
from business_object.zone_geographique import ZoneGeographique
from service.table.cles_api_service import ClesApiService
from datetime import datetime, timedelta

class TestEmpreinteCarboneService(unittest.TestCase):

    def setUp(self):
        now = datetime.now()
        self.date_visionnage = now.replace(minute = 0, second = 0, microsecond = 0)
        self.empreinte_service = EmpreinteCarboneService()
        self.zone_geo = ZoneGeographique("Paris", "France")
        self.info_video = InfoVideo(90, 720, "Wifi", "Mobile", self.zone_geo, self.date_visionnage)
        cle_api = ClesApiService().generer_cle_api("Consommateur")["cle_api"]
        self.cle_api = ClesApiService().trouver_cle_api("Consommateur", cle_api)

    def test_empreinte_carbone_entree_valide_1(self):
        empreinte = self.empreinte_service.empreinte_carbone(self.info_video, self.cle_api)
        self.assertIsNotNone(empreinte)
        self.assertIsInstance(empreinte, float)

    def test_empreinte_carbone_entree_resolution_non_connue(self):
        self.info_video.resolution = 1223
        with self.assertRaises(ValueError, msg = "Résolution non connu"):
            self.empreinte_service.empreinte_carbone(self.info_video, self.cle_api)

    def test_empreinte_carbone_mauvais_format_resolution(self):
        self.info_video.resolution = "720"
        with self.assertRaises(ValueError, msg = "Résolution non connu"):
            self.empreinte_service.empreinte_carbone(self.info_video, self.cle_api)

    def test_empreinte_carbone_entree_materiel_non_connu(self):      
        self.info_video.materiel = "Tablette"
        with self.assertRaises(ValueError, msg = "Matériel non connu"):
            self.empreinte_service.empreinte_carbone(self.info_video, self.cle_api)

    def test_empreinte_carbone_connexion_non_connue(self):
        self.info_video.type_connexion = "4G"
        with self.assertRaises(ValueError, msg = "Type de connexion non connu"):
            self.empreinte_service.empreinte_carbone(self.info_video, self.cle_api)

    def test_empreinte_carbone_date_visionnage_antérieure(self):
        self.info_video.date_visionnage = datetime.now() - timedelta(hours = 1)
        with self.assertRaises(ValueError, msg = "Non accès aux données provenant de l'API Electricity Map"):
            self.empreinte_service.empreinte_carbone(self.info_video, self.cle_api)

    @patch('business_object.zone_geographique.ZoneGeographique.prevision_carbone')
    def test_empreinte_carbone_date_fin_visionnage_postérieure_prévision(self, mock_prevision_carbone):
        next_hour = self.date_visionnage + timedelta(hours = 1)
        mock_prevision_carbone.return_value = [(str(self.date_visionnage), 100),(str(next_hour), 50)]
        self.info_video.date_visionnage = datetime.now() + timedelta(hours = 1)
        with self.assertRaises(ValueError, msg = "Non accès aux données provenant de l'API Electricity Map"):
            self.empreinte_service.empreinte_carbone(self.info_video, self.cle_api)

    @patch('dao.historique_consommateur_dao.HistoriqueConsommateurDao.creer')
    @patch('business_object.zone_geographique.ZoneGeographique.prevision_carbone')
    def test_empreinte_carbone_entree_valide_2(self, mock_prevision_carbone, mock_creer):
        next_hour = self.date_visionnage + timedelta(hours = 1)
        mock_prevision_carbone.return_value = [(str(self.date_visionnage), 100),(str(next_hour), 50)]
        empreinte_calculee = self.empreinte_service.empreinte_carbone(self.info_video, self.cle_api)
        nb_bytes = 1280 * 720 * 25 * 60 * self.info_video.duree
        impact_energie = self.info_video.duree * 1.1e-4 + nb_bytes * (1.52e-10 + 7.2e-11)
        empreinte_main = round(impact_energie * (60*100 + 30*50)/90 ,1)
        self.assertEqual(empreinte_calculee, empreinte_main)
        mock_creer.assert_called()

    @patch('dao.historique_consommateur_dao.HistoriqueConsommateurDao.trouver_empreinte_par_cle_api')
    def test_empreinte_moyenne(self, mock_trouver_empreinte):
        mock_trouver_empreinte.return_value = [100, 200, 300]
        moyenne = self.empreinte_service.empreinte_moyenne(self.cle_api)
        self.assertEqual(moyenne, 200)

    @patch('dao.historique_consommateur_dao.HistoriqueConsommateurDao.trouver_empreinte_par_cle_api')
    def test_empreinte_total(self, mock_trouver_empreinte):
        mock_trouver_empreinte.return_value = [100, 200, 300]
        total = self.empreinte_service.empreinte_total(self.cle_api)
        self.assertEqual(total, 600)

if __name__ == '__main__':
    unittest.main()
