# Asennusohje, käyttöohje ja käyttötapaukset

## Asennusohje

Sovellusta voi käyttää paikallisesti ja Herokussa. Sovellus toimii samalla tavalla paikallisesti ja Herokussa, mutta tietokannat ovat eri. Paikallisesti sovellus käyttää sijainnissa application/roster.db olevaa SQL-tietokantaa. Herokussa sovellus käyttää Herokun pilvessä olevaa PostgreSql-tietokantaa.

Sovelluksen asennus ja suoritus paikallisesti:
- Asenna tarvittaessa Python, virtualenv ja sqlite3
- Lataa Health Care App -sovelluksen zip-tiedosto ja pura se TAI kloonaa projekti koneellesi komennolla _git_ _clone_ _git@github.com:lottajylha/health-care-roster.git_
- Luo virtuaaliympäristö ladatun projektin juureen komennolla _py -m venv venv_
- Ota virtuaaliympäristö käyttöön projektin juuressa komennolla _source venv/Scripts/activate_
- Asetetaan sovelluksen riippuvuudet tiedostosta requirements.txt komennolla _pip_ _install_ _-r_ _requirements.txt_
- Sovellus käynnistyy nyt komennolla _py_ _run.py_

Sovelluksen käyttö Herokussa
- Sovellus löytyy osoitteesta <https://health-care-roster.herokuapp.com/>

## Käyttöohje

Sovellusta voi käyttää kirjautuneena tai kirjautumatta. Testitunnukset sekä Herokun että paikallisesti suoritettavan sovelluksen työnantaja-käyttäjälle ovat
- käyttäjätunnus: herokuuser
- salasana: herokuuser
ja työntekijä-käyttäjälle ovat
- käyttäjätunnus: employer
- salasana: employer

### Ilman kirjautumista
Ilman kirjautumista käyttäjä voi tarkastella työvuorolistaa, joka avautuu sovelluksen käynnistyessä ja löytyy polusta _/roster_. Työvuorolista on taulukko, jossa näkyy sovelluksen tietokantaan lisättyjen vuorojen
- päivämäärä
- kellonaika
- vuoroon tarvittavien lääkäreiden määrä
- vuoroon tarvittavien sairaanhoitajien määrä
- vuoroon tarvittavien perushoitajien määrä
- vuoroon ilmottautuneet työntekijät (nimi ja asema)
- vuoron status, eli puuttuuko tarvittavia työntekijöitä vai onko vuoro hyväksytty (työntekijöitä on ilmottautunut tarpeeksi).
Sarakkeissa Doctors needed, Nurses needed ja Practical nurses needed on myös napit, joita painamalla määrää voi kasvattaa ja vähentää. Kirjautumattoman käyttäjän tai työntekijä-käyttäjän napin painaminen ei kuitenkaan kasvata/vähennä määriä, sillä vain työnantaja-käyttäjällä on tähän oikeus.
![Työvuorolista](https://user-images.githubusercontent.com/36735637/64443938-ae2b4f80-d0db-11e9-9110-a84311120080.JPG)
Työvuorolista-näkymä kirjatumattomalle käyttäjälle.

Kirjautumaton käyttäjä voi myös rekisteröityä ja kirjautua sisään.

## Rekisteröinti

Etusivulta rekisteröintiin pääsee klikkaamalla "Sign up" -tekstiä. Tämä siirtää käyttäjän polkuun _/auth/new_, jossa on rekisteröintinäkymä. Rekisteröintinäkymässä on tekstikentät nimelle (Name), käyttäjätunnukselle (username) ja salasanalle (password), sekä valintanappi asemalle (Position) sekä rekisteröintiin johtava nappi "Sign up". Jokainen kenttä on täytettävä. Virheellisestä kentän sisällöstä käyttäjä saa ilmoituksen, eikä tietoja lisätä tietokantaan.
Virheellisiä syötteitä ovat
- Name-kenttä on tyhjä tai sisältää vain välilyöntejä tai merkkimäärä on alle 4 tai yli 100
- Username-kenttä on tyhjä tai sisältää vain välilyöntejä tai merkkimäärä on alle 4 tai yli 20 tai syötetty merkkijono on jo käytössä jollain rekisteröityneellä käyttäjällä
- Password-kenttä on tyhjä tai sisältää vain välilyöntejä tai merkkimäärä on alle 4 tai yli 10
- Position-valintaa ei ole tehty
Rekisteröinnin onnistuessa käyttäjä siirretään polkuun _/roster_.
![Onnistunut rekisteröinti](https://user-images.githubusercontent.com/36735637/64444269-7375e700-d0dc-11e9-95ef-2d361296c919.JPG)
Rekisteröinti-näkymä, jossa esimerkki validista käyttäjän syötteestä.
![Epäonnistunut rekisteröinti](https://user-images.githubusercontent.com/36735637/64443970-c13e1f80-d0db-11e9-89dd-8a4bdccbbebe.JPG)
Rekisteröinti-näkymä, jossa esimerkki virheellisestä käyttäjän syötteestä. Näkymässä myös virheilmoitukset.

## Kirjautuminen

Rekisteröitynyt ja kirjautumaton käyttäjä voi kirjautua klikaamalla "Log in" -tekstiä. Klikkaus siirtää käyttäjän polkuun _/auth/login_. Kirjautumiseen vaaditaan rekisteröinnissä syötetyt käyttäjätunnus ja salasana. Käyttäjä saa ilmoituksen virheellisistä syötteestä, joita ovat jommassa kummassa tekstikentässä
- tyhjä kenttä
- virheellinen käyttäjätunnus (annettua syötettä Username-kenttään ei ole rekisteröity sovelluksen tietokantaan)
- virheellinen salasana (annettu syöte Password-kentässä ei vastaa Username-kentän syötettä vastaavalle käyttäjälle tallennettua salasanaa sovelluksen tietokannassa).

Kirjatumisen onnistuessa käyttäjä siirretään polkuun _/roster_ ja kirjatumisen ollessa voimassa jokaisen polun näkymän yläreunassa on teksti "User (kirjatuneen käyttäjän nimi) is logged in." Jokaisen polun näkymässä on myös nappi "Log out", jota klikkaamalla käyttäjä voi kirjatua ulos.
![Kirjatuminen](https://user-images.githubusercontent.com/36735637/64444287-7ffa3f80-d0dc-11e9-9549-8d0d3576d2b3.JPG)
Kirjatumis-näkymä, jossa esimerkki validista käyttäjän syötteestä.

## Kirjatunut käyttäjä (työntekijä)

### Etusivu

Kirjatuneen käyttäjän polun _/roster_ työvuorolistassa näkyy kaksi uutta saraketta Status-sarakkeen jälkeen: "Logged user working in this shift" (onko kirjatunut käyttäjä ilmottautunut kyseiseen vuoroon) ja "Add/remove shift" (sarakkeessa on nappi "Change", josta vuoroon voi ilmottautua tai poistaa itsensä vuorosta). Käyttäjä voi ilmottautua vuoroon, mikäli vuorosta puuttuu käyttäjän asemaa vastaava työntekijä.
![Etusivu työntekijälle](https://user-images.githubusercontent.com/36735637/64443961-bb483e80-d0db-11e9-95f0-e1f144a60f4b.JPG)
Työvuorolista-näkymä työntekijälle, jossa on kirjatumattoman käyttäjän näkymään erona mahdollisuus ilmottautua työvuoroon ja katsoa mihin vuoroihin on ilmottautunut.

### Omat työvuorot

Kirjatunut käyttäjä näkee jokaisen polun näkymässä tekstin "My shifts", jota painamalla käyttäjä siirretään polkuun _/user/get/(käyttäjän id)_. Polun näkymässä on käyttäjän omat työvuorot. Vuoroista näkyy päivämäärä ja kellonaika.
![Omat työvuorot](https://user-images.githubusercontent.com/36735637/64444000-d2872c00-d0db-11e9-9bc6-c4641b2c8ebf.JPG)
Kirjatuneen käyttäjän näkymä, jossa on omat työvuorot listattuna.

## Kirjatunut käyttäjä (työnantaja)

Käyttäjä, jonka asema on työnantaja (Employer) voi kirjautuneen käyttäjän mahdollisuuksien lisäksi nähdä listan työntekijöistä sekä lisätä vuoron vuorolistaan. Käyttäjä ei voi rekisteröityä sovelluksessa työnantajaksi, mutta työnantaja-käyttäjää voi testata testitunnuksilla (ks. kohta Käyttöohje).

### Etusivu

Kirjatuneelle työnantajalle polun _/roster_ näkymä ja toiminnallisuus on sama kuin työntekijälle, mutta työnantaja voi poistaa työvuoroja. Työvuorolistassa on nyt sarake "Delete", jossa jokaisella rivillä nappi kyseisen työvuoron poistamiseen. Työnantajan klikattua nappia, työvuoro poistetaan tietokannasta (eli myös työvuoron työntekijöiltä). Sen työnantaja uudelleenohjataan samaan näkymään jossa näkyy nyt työvuorolista, jossa ei enää ole juuri poistettua vuoroa.
![Työnantaja etusivu](https://user-images.githubusercontent.com/36735637/64443954-b6838a80-d0db-11e9-9d5e-ed347fdf403c.JPG)
Työnantajan etusivu-näkymä, jossa myös mahdollisuus työvuorojen poistoon.


### Uusi työvuoro

Työnantaja voi lisätä uuden työvuoron klikkaamalla "Add shift" -tekstiä. Käyttäjä siirretään polkuun _/roster/new_, jossa työvuorolle valitaan päivämäärä ja kellonaika ja kirjoitetaan numeroina tarvittavien lääkäreiden, sairaanhoitajien ja perushoitajien määrät. Molemmat valintanapit (päivämäärä ja kellonaika) ja määriä koskevat kentät vaativat valinnan. Virheellisistä syötteistä tulee teksti näkymän alareunaan ja työvuoroa ei lisätä. Virheellisiä syötteitä puuttuvan syötteen lisäksi ovat määriä koskevissa kentissä
- syötteet, jotka sisältävät muita merkkejä kuin numeroita (kirjaimet, välilyönnit)
- annettu luku on alle 0 tai yli 15

Kun syötteet ovat valideja, napin "Submit new working hour" klikkaaminen lisää työvuoron sovellukseen. Napin klikkaus siirtää käyttäjän polkuun _/roster_, jossa työvuorolistassa näkyy myös juuri lisätty työvuoro.
![Työvuoron lisäys](https://user-images.githubusercontent.com/36735637/64444418-c51e7180-d0dc-11e9-9f7d-9c220ddba0af.JPG)
Työvuoron lisäys -näkymä ja esimerkki validista syötteestä.

### Työntekijät

Työnantaja näkee listan sovellukseen rekisteröityneistä työntekijöistä klikkaamalla missä tahansa polussa tekstiä "See employees". Klikkaus siirtää käyttäjän polkuun _/users/_, jossa on taulukossa listattuna jokaisen työntekijän nimi (Employee-sarake), asema (Position-sarake), työntekijän minimituntimäärä viikossa (Week minimum) ja työntekijän maksimituntimäärä viikossa (Week maximum). Jokaisen työntekijän perässä on myös kentät työntekijän viikkominimin ja -maksimin muokkaamiselle.

Työnantaja-käyttäjä voi muokata listassa olevan työntekijän viikkotuntiarvoja syöttämällä kenttiin numeroina uudet arvot. Virheellisiä syötteitä viikkominimille ja -maksimille ovat
- tyhjä syöte
- syötteessä muita merkkejä kuin numeroita (välilyöntejä tai kirjaimia)
- luku on alle 0 tai yli 50
Luvut syötettyään napin Set weekhours klikkaaminen vaihtaa työntekijän viikkominimin ja maksimin. Uudet arvot näkyvät samassa näkymässä klikkauksen jälkeen.

![Viikkotuntien päivitys](https://user-images.githubusercontent.com/36735637/64443978-c7340080-d0db-11e9-9053-4967ecdd1b01.JPG)
Työnantajalle sallittu näkymä, jossa lista käyttäjistä ja toiminnallisuus viikkotuntimäärien päivitykseen.
![Virheellinen viikkotuntien päivitys](https://user-images.githubusercontent.com/36735637/64443993-cbf8b480-d0db-11e9-926a-3a0b5064ac8c.JPG)
Työantajan syötteen ollessa virheellinen, näkymään lisätään virheilmoitukset.
