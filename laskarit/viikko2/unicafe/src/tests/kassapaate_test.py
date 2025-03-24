import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):

    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(1000)
        self.rajallinen_maksukortti = Maksukortti(200)

    def test_alussa_oikea_rahamaara_kassassa(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)


    def test_edullisia_aluksi_0(self):
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_maukkaita_aluksi_0(self):
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_edullinen_kateisosto_menee_lapi_vaihtoraha_oikea(self):

        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(300), 60)

    def test_edullinen_kateisosto_menee_lapi_kassan_rahamaara_kasvaa(self):
        self.kassapaate.syo_edullisesti_kateisella(240)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)

    def test_maukas_kateisosto_menee_lapi_vaihtoraha_oikea(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(500), 100)

    def test_maukas_kateisosto_menee_lapi_kassan_rahamaara_kasvaa(self):
        self.kassapaate.syo_maukkaasti_kateisella(400)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)

    def test_edullinen_kateisosto_menee_lapi_edullisten_maara_kasvaa(self):
        self.kassapaate.syo_edullisesti_kateisella(240)

        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_maukas_kateisosto_menee_lapi_maukkaiden_maara_kasvaa(self):
        self.kassapaate.syo_maukkaasti_kateisella(400)

        self.assertEqual(self.kassapaate.maukkaat, 1)

    #negatiiviset

    def test_edullinen_kateisosto_ei_mene_lapi_kaikki_rahat_takaisin(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(100), 100)

    def test_edullinen_kateisosto_ei_mene_lapi_kassan_rahamaara_ei_kasva(self):
        self.kassapaate.syo_edullisesti_kateisella(100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_maukas_kateisosto_ei_mene_lapi_kaikki_rahat_takaisin(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(100), 100)

    def test_maukas_kateisosto_ei_mene_lapi_kassan_rahamaara_ei_kasva(self):
        self.kassapaate.syo_maukkaasti_kateisella(100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_edullinen_kateisosto_ei_mene_lapi_edullisten_maara_ei_kasva(self):
        self.kassapaate.syo_edullisesti_kateisella(100)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_maukas_kateisosto_ei_mene_lapi_maukkaiden_maara_ei_kasva(self):
        self.kassapaate.syo_maukkaasti_kateisella(100)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    #negatiiviset loppuuuu :))
    
    def test_kortti_osto_lapi_palauta_True_edullinen(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.maksukortti), True)

    def test_kortti_osto_lapi_velotettu_kortilta_edullinen(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo, 760)

    def test_kortti_osto_lapi_palauta_True_maukas(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti), True)

    def test_kortti_osto_lapi_velotettu_kortilta_maukas(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo, 600)

    def test_kortti_osto_lapi_lounaiden_maara_kasvaa_edullinen(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_kortti_osto_lapi_lounaiden_maara_kasvaa_maukas(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    #negatiiviset 

    def test_kortti_osto_ei_lapi_palauta_False_edullinen(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.rajallinen_maksukortti), False)

    def test_kortti_osto_ei_lapi_ei_velotettu_kortilta_edullinen(self):
        self.kassapaate.syo_edullisesti_kortilla(self.rajallinen_maksukortti)
        self.assertEqual(self.rajallinen_maksukortti.saldo, 200)

    def test_kortti_osto_ei_lapi_palauta_False_maukas(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.rajallinen_maksukortti), False)

    def test_kortti_osto_ei_lapi_ei_velotettu_kortilta_maukas(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.rajallinen_maksukortti)
        self.assertEqual(self.rajallinen_maksukortti.saldo, 200)

    def test_kortti_osto_ei_lapi_lounaiden_maara_ei_kasva_edullinen(self):
        self.kassapaate.syo_edullisesti_kortilla(self.rajallinen_maksukortti)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_kortti_osto_ei_lapi_lounaiden_maara_ei_kasva_maukas(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.rajallinen_maksukortti)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_kassan_rahamaara_ei_muutu_kortilla_ostaessa_edullinen(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_kassan_rahamaara_ei_muutu_kortilla_ostaessa_maukas(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    #negatiiviset loppuu yippe

    def test_kortille_rahaa_ladattaessa_sen_saldo_muuttuu(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 100)
        self.assertEqual(self.maksukortti.saldo, 1100)

    def test_kortille_rahaa_ladattaessa_kassan_rahamaara_kasvaa_samalla_summalla(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100100)

