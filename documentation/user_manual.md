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

Kirjautumaton käyttäjä voi myös rekisteröityä ja kirjautua sisään.

## Rekisteröinti

Etusivulta rekisteröintiin pääsee klikkaamalla "Sign up" -tekstiä. Tämä siirtää käyttäjän polkuun _/auth/new_, jossa on rekisteröintinäkymä. Rekisteröintinäkymässä on tekstikentät nimelle (Name), käyttäjätunnukselle (username) ja salasanalle (password), sekä valintanappi asemalle (Position) sekä rekisteröintiin johtava nappi "Sign up". Jokainen kenttä on täytettävä. Virheellisestä kentän sisällöstä käyttäjä saa ilmoituksen, eikä tietoja lisätä tietokantaan.
Virheellisiä syötteitä ovat
- Name-kenttä on tyhjä tai sisältää vain välilyöntejä tai merkkimäärä on alle 4 tai yli 100
- Username-kenttä on tyhjä tai sisältää vain välilyöntejä tai merkkimäärä on alle 4 tai yli 20 tai syötetty merkkijono on jo käytössä jollain rekisteröityneellä käyttäjällä
- Password-kenttä on tyhjä tai sisältää vain välilyöntejä tai merkkimäärä on alle 4 tai yli 10
- Position-valintaa ei ole tehty
Rekisteröinnin onnistuessa käyttäjä siirretään polkuun _/roster_.

## Kirjautuminen

Rekisteröitynyt ja kirjautumaton käyttäjä voi kirjautua klikaamalla "Log in" -tekstiä. Klikkaus siirtää käyttäjän polkuun _/auth/login_. Kirjautumiseen vaaditaan rekisteröinnissä syötetyt käyttäjätunnus ja salasana. Käyttäjä saa ilmoituksen virheellisistä syötteestä, joita ovat jommassa kummassa tekstikentässä
- tyhjä kenttä
- virheellinen käyttäjätunnus (annettua syötettä Username-kenttään ei ole rekisteröity sovelluksen tietokantaan)
- virheellinen salasana (annettu syöte Password-kentässä ei vastaa Username-kentän syötettä vastaavalle käyttäjälle tallennettua salasanaa sovelluksen tietokannassa).

Kirjatumisen onnistuessa käyttäjä siirretään polkuun _/roster_ ja kirjatumisen ollessa voimassa jokaisen polun näkymän yläreunassa on teksti "User (kirjatuneen käyttäjän nimi) is logged in." Jokaisen polun näkymässä on myös nappi "Log out", jota klikkaamalla käyttäjä voi kirjatua ulos.

## Kirjatunut käyttäjä (työntekijä)

### Etusivu

Kirjatuneen käyttäjän polun _/roster_ työvuorolistassa näkyy kaksi uutta saraketta Status-sarakkeen jälkeen: "Logged user working in this shift" (onko kirjatunut käyttäjä ilmottautunut kyseiseen vuoroon) ja "Add/remove shift" (sarakkeessa on nappi "Change", josta vuoroon voi ilmottautua tai poistaa itsensä vuorosta). Käyttäjä voi ilmottautua vuoroon, mikäli vuorosta puuttuu käyttäjän asemaa vastaava työntekijä.

### Omat työvuorot

Kirjatunut käyttäjä näkee jokaisen polun näkymässä tekstin "My shifts", jota painamalla käyttäjä siirretään polkuun _/user/get/(käyttäjän id)_. Polun näkymässä on käyttäjän omat työvuorot. Vuoroista näkyy päivämäärä ja kellonaika.

## Kirjatunut käyttäjä (työnantaja)

Käyttäjä, jonka asema on työnantaja (Employer) voi kirjautuneen käyttäjän mahdollisuuksien lisäksi nähdä listan työntekijöistä sekä lisätä vuoron vuorolistaan. Käyttäjä ei voi rekisteröityä sovelluksessa työnantajaksi, mutta työnantaja-käyttäjää voi testata testitunnuksilla (ks. kohta Käyttöohje).

### Uusi työvuoro

Työnantaja voi lisätä uuden työvuoron klikkaamalla "Add shift" -tekstiä. Käyttäjä siirretään polkuun _/roster/new_, jossa työvuorolle valitaan päivämäärä ja kellonaika ja kirjoitetaan numeroina tarvittavien lääkäreiden, sairaanhoitajien ja perushoitajien määrät. Molemmat valintanapit (päivämäärä ja kellonaika) ja määriä koskevat kentät vaativat valinnan. Virheellisistä syötteistä tulee teksti näkymän alareunaan ja työvuoroa ei lisätä. Virheellisiä syötteitä puuttuvan syötteen lisäksi ovat määriä koskevissa kentissä
- syötteet, jotka sisältävät muita merkkejä kuin numeroita (kirjaimet, välilyönnit)
- annettu luku on alle 0 tai yli 15

Kun syötteet ovat valideja, napin "Submit new working hour" klikkaaminen lisää työvuoron sovellukseen. Napin klikkaus siirtää käyttäjän polkuun _/roster_, jossa työvuorolistassa näkyy myös juuri lisätty työvuoro.

### Työntekijät

Työnantaja näkee listan sovellukseen rekisteröityneistä työntekijöistä klikkaamalla missä tahansa polussa tekstiä "See employees". Klikkaus siirtää käyttäjän polkuun _/users/_, jossa on taulukossa listattuna jokaisen työntekijän nimi (Employee-sarake), asema (Position-sarake), työntekijän minimituntimäärä viikossa (Week minimum) ja työntekijän maksimituntimäärä viikossa (Week maximum). Jokaisen työntekijän perässä on myös kentät työntekijän viikkominimin ja -maksimin muokkaamiselle.

Työnantaja-käyttäjä voi muokata listassa olevan työntekijän viikkotuntiarvoja syöttämällä kenttiin numeroina uudet arvot. Virheellisiä syötteitä viikkominimille ja -maksimille ovat
- tyhjä syöte
- syötteessä muita merkkejä kuin numeroita (välilyöntejä tai kirjaimia)
- luku on alle 0 tai yli 50
Luvut syötettyään napin Set weekhours klikkaaminen vaihtaa työntekijän viikkominimin ja maksimin. Uudet arvot näkyvät samassa näkymässä klikkauksen jälkeen.
