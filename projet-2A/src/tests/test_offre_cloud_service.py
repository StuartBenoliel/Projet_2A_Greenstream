
import unittest
from unittest.mock import Mock
from service.offre_cloud_service import OffreCloudService
from business_object.ZoneGeographique import ZoneGeographique
from dao.serveur_dao import ServeurDao 

class TestOffreCloudService(unittest.TestCase):

    def setUp(self):
        self.offre_service = OffreCloudService()
        self.zone_geo = ZoneGeographique("Marseille")
        self.fournisseurs_cloud = ["Fournisseur1", "Fournisseur2"]
        self.date_visionnage = datetime.now()
        self.duree = 60

    @patch('service.table_service.TableService.voir_table_serveurs')
    @patch('business_object.zone_geographique.ZoneGeographique.name_to_zone')
    def test_serveurs_eligibles(self, mock_name_to_zone, mock_voir_table_serveurs):
        mock_name_to_zone.return_value = "zone_test"
        mock_voir_table_serveurs.return_value = [ServeurCloud(...), ServeurCloud(...)]
        result = self.offre_service.serveurs_eligibles(self.fournisseurs_cloud, self.zone_geo)
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(serveur, ServeurCloud) for serveur in result))

    @patch('business_object.zone_geographique.ZoneGeographique.prevision_carbone')
    @patch('service.table_service.TableService.voir_table_serveurs')
    def test_serveurs_optimaux(self, mock_voir_table_serveurs, mock_prevision_carbone):
        mock_prevision_carbone.return_value = [("2022-01-01 00:00:00", 100)]
        mock_voir_table_serveurs.return_value = [ServeurCloud(...), ServeurCloud(...)]
        result = self.offre_service.serveurs_optimaux(self.fournisseurs_cloud, self.zone_geo, self.duree, self.date_visionnage)
        self.assertIsInstance(result, dict)
        self.assertTrue(all(isinstance(key, ServeurCloud) and isinstance(value, float) for key, value in result.items()))

class TestOffreCloudService(unittest.TestCase):

    def setUp(self):
        self.service = OffreCloudService()
        self.localisation = ZoneGeographique("Marseille")
        self.fournisseurs_cloud = ["Fournisseur1", "Fournisseur2"]
        self.duree = 60
        self.date_visionnage = datetime.now()

    @patch('service.table_service.TableService.voir_table_serveurs')
    @patch('business_object.zone_geographique.ZoneGeographique.name_to_zone')
    def test_serveurs_eligibles(self, mock_name_to_zone, mock_voir_table_serveurs):
        mock_name_to_zone.return_value = "zone_test"
        mock_voir_table_serveurs.return_value = [MagicMock(spec=ServeurCloud), MagicMock(spec=ServeurCloud)]
        result = self.service.serveurs_eligibles(self.fournisseurs_cloud, self.localisation)
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(serveur, ServeurCloud) for serveur in result))

    @patch('business_object.zone_geographique.ZoneGeographique.prevision_carbone')
    @patch('service.table_service.TableService.voir_table_serveurs')
    def test_serveurs_optimaux(self, mock_voir_table_serveurs, mock_prevision_carbone):
        mock_prevision_carbone.return_value = [("2022-01-01 00:00:00", 100)]
        mock_voir_table_serveurs.return_value = [MagicMock(spec=ServeurCloud), MagicMock(spec=ServeurCloud)]
        result = self.service.serveurs_optimaux(self.fournisseurs_cloud, self.localisation, self.duree, self.date_visionnage)
        self.assertIsInstance(result, dict)
        self.assertTrue(all(isinstance(key, ServeurCloud) and isinstance(value, float) for key, value in result.items()))


if __name__ == '__main__':
    unittest.main()
