# Testausdokumentti
Ohjelma on testattu pääasiassa automatisoiduilla yksikkö- ja integraatiotesteillä, käyttäen unittestiä. Pelin toiminnallisuuden toimivuus on testattu, myös itse manuaalisesti etsimällä erilaisia virhetilanteita.

## Yksikkö- ja integraatiotestaus

## Testauskattavuus

![testikattavuus](../src/assets/Screenshot%202025-05-09%20154049.png)
Ohjelman haarautumakattavuus on 76%. Testauksen ulkopuolelle on jätetty tiedostot `textmanager.py`, `index.py` ja `game_over.py`, sillä ne hoitavat käyttöliittymään piirtämistä ja sen pyörimistä. Testauskattavuutta voisi kasvattaa laajentamalla tiedostossa objects.py sijaitsevan luokan MinusEnergy testausta. 

## Sovelluslogiikka
Testaus on jaettu kahteen luokkaan: `TestBackend` ja `TestSql`. Nimensä mukaan `TestBackend` testaa tiedostossa `objects.py` olevien objektien toimivuutta, yhteisien tietojen saatavuutta luokista `LogInManager` ja `GameStatus`. `TestSql` taas testaa toimivatko sql komennot halutulla ja odotetulla tavalla.

## Manuaalinen testaus

Pelin toimivuutta on testattu sekä Linux että Windows käyttöjärjestelmillä, molemmat toimivat odotetulla tavalla. Testaus on tapahtunut lataamalla projekti konelle, ja käynnistämällä se käyttöohjeiden kuvaamalla tavalla. Windows käyttöjärjestelmässä invoke komennot eivät toimi, joten pyöritettävät komennot, voi katsoa tiedostosta tasks.py.

Pelin toimivuutta piti testata manuaalisesti siksi, että pystyi tarkistamaan muun muassa objektien piirtyvän sinne minne niiden kuuluisi ja niiden olevan sopivan kokoisia. Testausta tein manuaalisesti myös siksi, että voisin itse kokea, onko peliä mielekästä pelata.