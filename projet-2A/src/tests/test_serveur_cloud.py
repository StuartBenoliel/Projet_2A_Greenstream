import unittest
from business_object.zone_geographique import ZoneGeographique
from business_object.serveur_cloud import ServeurCloud

class TestServeurCloud(unittest.TestCase):

    def setUp(self):
        self.id_serveur = "srv123"
        self.nom = "Serveur Test"
        self.code_region = "EU-WEST-1"
        self.fournisseur_cloud = "FournisseurTest"
        self.zone_disponibilite = ["zone1", "zone2"]
        self.localisation = ZoneGeographique("Paris", "France")
        self.serveur = ServeurCloud(self.id_serveur, self.nom, self.code_region, self.fournisseur_cloud, self.zone_disponibilite, self.localisation)

    def test_attributs_serveur(self):
        self.assertEqual(self.serveur.id_serveur, self.id_serveur)
        self.assertEqual(self.serveur.nom, self.nom)
        self.assertEqual(self.serveur.code_region, self.code_region)
        self.assertEqual(self.serveur.fournisseur_cloud, self.fournisseur_cloud)
        self.assertListEqual(self.serveur.zone_disponibilite, self.zone_disponibilite)
        self.assertEqual(self.serveur.localisation, self.localisation)

    def test_repr(self):
        representation = repr(self.serveur)
        self.assertIsInstance(representation, str)
        self.assertIn(self.id_serveur, representation)
        self.assertIn(self.nom, representation)
        self.assertIn(str(self.localisation), representation)

if __name__ == '__main__':
    unittest.main()