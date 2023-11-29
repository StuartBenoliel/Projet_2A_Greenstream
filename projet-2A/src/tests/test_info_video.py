import unittest
from datetime import datetime
from business_object.info_video import InfoVideo
from business_object.zone_geographique import ZoneGeographique

class TestInfoVideo(unittest.TestCase):

    def setUp(self):
        self.duree = 120
        self.resolution = 1080
        self.type_connexion = "Wifi"
        self.materiel = "Ordinateur"
        self.localisation = ZoneGeographique("Paris", "France")
        self.date_visionnage = datetime(2022, 1, 1, 12, 0, 0)
        self.info_video = InfoVideo(self.duree, self.resolution, self.type_connexion, self.materiel, self.localisation, self.date_visionnage)

    def test_initialisation(self):
        self.assertEqual(self.info_video.duree, self.duree)
        self.assertEqual(self.info_video.resolution, self.resolution)
        self.assertEqual(self.info_video.type_connexion, self.type_connexion)
        self.assertEqual(self.info_video.materiel, self.materiel)
        self.assertEqual(self.info_video.localisation, self.localisation)
        self.assertEqual(self.info_video.date_visionnage, self.date_visionnage)

    def test_initialisation_avec_date_par_defaut(self):
        info_video_sans_date = InfoVideo(self.duree, self.resolution, self.type_connexion, self.materiel, self.localisation)
        self.assertIsInstance(info_video_sans_date.date_visionnage, datetime)

if __name__ == '__main__':
    unittest.main()