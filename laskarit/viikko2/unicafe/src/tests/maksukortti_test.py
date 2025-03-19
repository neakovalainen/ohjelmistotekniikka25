import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_kortin_saldo_alussa_oikea(self):

        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

    def test_saldo_vahenee_jos_rahaa_tarpeeksi(self):
        self.maksukortti.ota_rahaa(500)
        
        self.assertEqual(self.maksukortti.saldo_euroina(), 5.0)

    def test_rahan_lataaminen_toimii(self):
        self.maksukortti.lataa_rahaa(1000)

        self.assertEqual(self.maksukortti.saldo_euroina(), 20.0)

    def test_saldo_ei_muutu_jos_rahaa_ei_tarpeeksi(self):
        self.maksukortti.ota_rahaa(2000)

        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

    def test_jos_rahat_riitti_True(self):

        self.assertEqual(self.maksukortti.ota_rahaa(100), True)

    def test_jos_ei_tarpeeksi_rahaa_False(self):

        self.assertEqual(self.maksukortti.ota_rahaa(10000), False)
        


