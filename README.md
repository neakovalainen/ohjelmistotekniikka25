# Ohjemistotekniikka harjoitustyö
__cloudleap__ on yksinkertainen tasohyppelypeli, jossa käyttäjä voi kerätä energiajuomia nostaakseen energiatasoonsa/pisteitään. Pelissä vastaan tulee koulutehtäviä, jotka vähentävät pisteitä. Käyttäjän pitää pyrkiä välttelemään niitä parhaansa mukaan.

## Dokumentaatio

[vaatimusmäärittely](https://github.com/neakovalainen/ohjelmistotekniikka25/tree/main/cloudleap/dokumentaatio/vaatimusmaarittely.md) \
[työaikakirjanpito](https://github.com/neakovalainen/ohjelmistotekniikka25/tree/main/cloudleap/dokumentaatio/tyoaikakirjanpito.md) \
[arkkitehtuuri](https://github.com/neakovalainen/ohjelmistotekniikka25/tree/main/cloudleap/dokumentaatio/arkkitehtuuri.md) \
[changelog](https://github.com/neakovalainen/ohjelmistotekniikka25/tree/main/cloudleap/dokumentaatio/changelog.md)

## käynnistysohjeet
1.  kopioi repositorio koneellesi
2. asenna projektin riippuvuudet \
 ``` poetry install```
3. käynnistä tietokanta \
   ``` python3 src/build.py ```
 5. käynnistä sovellus \
 ``` poetry run invoke start```

## muut ohjeet
- voit suorittaa testit komennolla \
``` poetry run invoke test```
- testikattavuuden saat suorittamalla komennon \
``` poetry run invoke coverage-report```
- pylintin saa suoritettua komennon \
``` poetry run invoke lint```

[__ylimääräinen koodikatselmointi__](https://github.com/JuhoTurunen/chess-app/issues/1)
