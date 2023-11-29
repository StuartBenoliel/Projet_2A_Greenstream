class TestZoneGeographique(unittest.TestCase):

    def setUp(self):
        self.ville = "Paris"
        self.pays = "France"
        self.zone_geo = ZoneGeographique(self.ville, self.pays)

    @patch('requests.get')
    def test_name_to_zone(self, mock_get):
        # Configurer le mock pour simuler une réponse API réussie
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"lat": "48.8566", "lon": "2.3522"}]
        zone = self.zone_geo.name_to_zone()
        self.assertIsNotNone(zone)
        mock_get.assert_called_with("https://nominatim.openstreetmap.org/search", params={'city': self.ville, 'country': self.pays, 'format': 'json'})

    @patch('requests.get')
    def test_prevision_carbone(self, mock_get):
        # Simuler deux appels API : un pour Nominatim et un pour ElectricityMap
        mock_get.side_effect = [
            # Réponse de Nominatim
            MagicMock(status_code=200, json=MagicMock(return_value=[{"lat": "48.8566", "lon": "2.3522"}])),
            # Réponse de ElectricityMap
            MagicMock(status_code=200, json=MagicMock(return_value={"forecast": [{"datetime": "2022-01-01T00:00:00Z", "carbonIntensity": 100}]}))
        ]
        prevision = self.zone_geo.prevision_carbone()
        self.assertIsNotNone(prevision)
        self.assertEqual(len(prevision), 1)
        self.assertEqual(prevision[0][1], 100)

if __name__ == '__main__':
    unittest.main()