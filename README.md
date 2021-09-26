# Kielioppikone

## Sovelluksen tarkoitus

Sovellus on tarkoitettu suomen kielen sanojen taivutusmuotojen harjoitteluun. Sovelluksella on kaksi käyttäjäryhmää: **opettajat** luovat kielioppitehtäviä, ja **oppilaat** suorittavat tehtäviä. Niiden avulla oppilaat voivat opetella tunnistamaan ja muodostamaan sekä **nominien sijamuotoja** että **verbien persoona- ja aikamuotoja**.

## Sovelluksen toiminnot

- käyttäjäksi **rekisteröityminen** (eri roolit opettajille ja oppilaille; sovelluksen käyttäjä voi itse rekisteröityä vain oppilaan rooliin)
- **kirjautuminen**
- opettajilla **kurssien ja kurssitehtävien luominen**
- oppilailla **kurssille liittyminen ja kurssitehtävien suorittaminen**
- kaikilla käyttäjillä oma **profiilinäkymä**: oppilas voi tarkastella mm. suorittamiaan tehtäviä ja niiden onnistumisprosentteja; opettaja näkee omat kurssinsa ja niille ilmoittautuneet oppilaat sekä pääsee muokkaamaan kurssien tehtäviä

(Jos ehdin, toteutan ehkä opettajille mahdollisuuden tarkastella oppilaidensa tehtäväsuorituksia ja niistä muodostettuja tilastoja.)

## Kurssitehtävien toteutus

- Opettajalla on pääsy lomakkeelle, jolla hän syöttää tietokantaan kurssin aiheen (esim. *Kieliopillisten sijamuotojen tunnistaminen*) sekä laatii siihen sopivat tehtävät.
- Tehtävät syötetään tietokantaan määrittelemällä kolme asiaa: sanan perusmuoto (esim. *kissa*), sanan taivutusmuoto (esim. *kissan*) ja taivutusmuodon määritelmä (esim. *y. genetiivi*). Tietokanta mahdollistaa näillä eväillä kaksi tehtävätyyppiä: voidaan kysyä sanan taivutusmuodon määritelmää tai pyytää oppilasta taivuttamaan tietty sana tiettyyn muotoon. Tehtävätyyppi määritellään sovellustasolla, ei tietokannassa.
- Oppilaalla on pääsy lomakkeelle, jolla hän ilmoittautuu kurssille ja pääsee siten tekemään kurssitehtäviä.
- Oppilaan vastauksista tietokantaan tallentuu tehtävän yksilöivä tunniste sekä tieto siitä, oliko vastaus oikein vai väärin. Oppilas voi tarkastella sovelluksessa onnistumisprosenttiaan ja seurata siten edistymistään. (Suunnittelemani tietokanta mahdollistaa monipuolisen raportin muodostamisen, mutta jää nähtäväksi, kuinka laajasti ehdin hyödyntää projektissani näitä mahdollisuuksia.)

## Sovelluksen ulkoasu

Toteutan ulkoasun ns. käsin kirjoittamalla tyylimäärittelyt css-tiedostoon. Viimeistelen visuaalisen ilmeen itse tekemälläni taustagrafiikalla ja hyödyntämällä Google Fontsia.

## Sovelluksen tila 26.9.2021

Sovellus on käynnissä osoitteessa [https://kielioppikone.herokuapp.com](https://kielioppikone.herokuapp.com). Tietokannassa on jonkin verran testidataa, mm. käyttäjät *mummomatikainen* ja *kattimatikainen*, joista ensimmäisellä on opettajan rooli ja jälkimmäisellä tavallisen käyttäjän rooli. Kummankin salasana on "matikainen". Sovellukseen voi myös rekisteröidä uuden käyttäjätunnuksen sekä tietenkin kirjautua. Kursseja voi selata, mutta tällä hetkellä niihin ilmoittautumisessa on vika, jota en ole ehtinyt korjata (vain yhdelle kurssille ilmoittautuminen onnistuu). Kursseilla oleviin tehtäviin pystyy vastaamaan, jos on ilmoittautunut kurssille.

Toistaiseksi hiukan rikkinäinen toiminto on opettajan rooliin kuuluva tehtävien lisääminen kurssille: olen saanut sen toimimaan osittain paikallisella palvelimella, mutta Herokussa se ei toimi lainkaan. 

Hakutoiminto ja uusien kurssien luominen puuttuvat vielä kokonaan, samoin käyttäjän profiilisivulla näytettävät tilastotiedot.