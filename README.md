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
- Oppilaan vastauksista tietokantaan tallentuu tehtävän yksilöivä tunniste sekä tieto siitä, oliko vastaus oikein vai väärin. Oppilas voi tarkastella sovelluksessa onnistumisprosenttiaan ja seurata siten edistymistään. (Suunnittelemani tietokanta mahdollistaa monipuolisen raportin muodostamisen, mutta jää nähtäväksi, kuinka laajasti ehdin hyödyntää projektissani näitä mahdollisuuksia.)

## Sovelluksen ulkoasu

Toteutan ulkoasun ns. käsin kirjoittamalla tyylimäärittelyt css-tiedostoon. Viimeistelen visuaalisen ilmeen itse tekemälläni taustagrafiikalla ja hyödyntämällä Google Fontsia.

## Sovelluksen tila 10.10.2021

Sovellus on käynnissä osoitteessa [https://kielioppikone.herokuapp.com](https://kielioppikone.herokuapp.com). Tietokannassa on jonkin verran testidataa, mm. käyttäjät *mummomatikainen* ja *kattimatikainen*, joista ensimmäisellä on opettajan rooli ja jälkimmäisellä tavallisen käyttäjän rooli. Kummankin salasana on "matikainen".

- Sovellukseen voi rekisteröidä uuden käyttäjätunnuksen sekä tietenkin kirjautua.
- Kursseja voi selata, ja niille voi ilmoittautua. Sovellus ei salli samalle kurssille ilmoittautumista kahteen kertaan.
- Kursseja voi suodattaa hakusanojen perusteella.
- Kursseilla oleviin tehtäviin pystyy vastaamaan, jos on ilmoittautunut kurssille.
- Omalla profiilisivullaan oppilas näkee kaikkien kurssiensa keskimääräisen onnistumisprosentin, ja kurssikohtaisesta näkymästä selviää yksittäisen kurssin onnistumisprosentti.
- Opettaja näkee omalla profiilisivullaan kaikki kurssinsa sekä pystyy lisäämään uuden kurssin.
- Opettaja pääsee profiilisivunsa kautta muokkaamaan kurssejaan ja tarkastelemaan niiden osallistujia. Osallistujalista esittää joitain käyttäjäkohtaisia tietoja, ja käyttäjän nimeä klikkaamalla opettaja pääsee tarkastelemaan käyttäjän onnistumistilastoa.
- Kurssikohtaisella muokkaussivulla opettaja pystyy piilottamaan kurssin tai palauttamaan piilotetun kurssin. Piilotetut kurssit eivät esiinny kaikkien kurssien näkymässä eivätkä oppilaan omien kurssien näkymässä.
- Opettaja voi lisätä kurssille tehtäviä (edelleen on vain yksi tehtävätyyppi käytettävissä) tai poistamaan tehtävän, jos siihen ei ole vielä kukaan vastannut.
- Opettaja pystyy muokkaamaan kurssin otsikkoa ja kuvaustekstiä.

Jatkokehityssuunnitelmia:
- tietokannasta taitaa puuttua joitain constrainteja?
- lomakkeiden kenttiin not null -vaatimus sekä täyttöohjeet
- lisävaatimuksia salasanan koostumukselle
- toisen tehtävätyypin toteutus
- käyttäjän kurssikohtaisten tilastotietojen laajennus
- kurssien luokitteleminen aihepiirin mukaan; mahdollistaa tarkemman osaamisprofiilin muodostamisen oppilaalle sekä selkeyttää kurssitehtävien laatimista
- saavutettavuuden parantaminen?
- tietokantakyselyjen tehokkuuden parantaminen?
- lisää ulkoasun tyylittelyä
- koodin siistimistä ja yhdenmukaistamista sekä sovelluksen rakenteen kehittelyä eteenpäin