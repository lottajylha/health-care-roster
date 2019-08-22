# Käyttöohje

Sovellusta voi käyttää kirjautuneena tai kirjautumatta. Testitunnukset Herokussa olevaan sovellukseen työntekijä-käyttäjälle:
- käyttäjätunnus: herokuuser
- salasana: herokuuser
ja työnantaja-käyttäjälle:
- käyttäjätunnus: employer
- salasana: employer

Ilman kirjautumista käyttäjä voi tarkastella työvuorolistaa, josta näkyy työvuorolistaan lisättyjen vuorojen
- päivämäärä
- kellonaika
- vuoroon tarvittavien lääkäreiden määrä
- vuoroon tarvittavien sairaanhoitajien määrä
- vuoroon tarvittavien perushoitajien määrä
- vuoroon ilmottautuneet työntekijät (nimi ja asema)
- vuoron status, eli puuttuuko tarvittavia työntekijöitä vai onko vuoro hyväksytty (työntekijöitä on ilmottautunut tarpeeksi).

Tämän lisäksi kirjautumaton käyttäjä voi rekisteröityä ja kirjautua sisään.

## Rekisteröinti

Etusivulta rekisteröintiin pääsee klikkaamalla "Sign up" -tekstiä. Rekisteröintiin vaaditaan nimi (Name), käyttäjätunnus (Username), salasana (Password) sekä aseman valinta (lääkäri, sairaanhoitaja, perushoitaja). Jokainen kenttä on täytettävä. Virheellisestä kentän sisällöstä käyttäjä saa ilmoituksen, eikä tietoja lisätä tietokantaan.

## Kirjautuminen

Rekisteröitynyt ja kirjautumaton käyttäjä voi kirjautua klikaamalla "Log in" -tekstiä. Kirjautumiseen vaaditaan rekisteröinnissä syötetyt käyttäjätunnus ja salasana. Käyttäjä saa ilmoituksen virheellisistä syötöistä, joita ovat puuttuva kenttä, virheellinen käyttäjätunnus tai virheellinen salasana.

## Kirjatunut käyttäjä (työntekijä)

### Etusivu

Kirjatuneen käyttäjän etusivun työvuorolistassa näkyy kaksi uutta saraketta: onko kirjatunut käyttäjä ilmottautunut kyseiseen vuoroon ja nappi, josta vuoroon voi ilmottautua tai poistaa itsensä vuorosta. Käyttäjä voi ilmottautua vuoroon, mikäli vuorosta puuttuu käyttäjän asemaa vastaava työntekijä.

### Omat työvuorot

Kirjatunut käyttäjä näkee yhteenvedon omista työvuoroistaan klikaamalla "My shifts" -tekstiä. Vuoroista näkyy päivämäärä ja kellonaika.

### Uloskirjautuminen

Kirjautunut käyttäjä voi kirjautua ulos klikkaamalla "Log out" -tekstiä.

## Kirjatunut käyttäjä (työnantaja)

Käyttäjä, jonka asema on työnantaja (Employer) voi kirjautuneen käyttäjän mahdollisuuksien lisäksi nähdä listan työntekijöistä sekä lisätä vuoron vuorolistaan.

### Uusi työvuoro

Työnantaja voi lisätä uuden työvuoron klikkaamalla "Add shift" -tekstiä. Työvuorolle valitaan päivämäärä ja kellonaika, joista molemmat vaativat käyttäjän valinnan. Lisäksi työvuorolle voi asettaa tarvittavien lääkäreiden, sairaanhoitajien ja perushoitajien määrät. Mikäli jonkin henkilömäärää koskevan kentän jättää täyttämättä, sen arvoksi asetetaan 0.

Työnantaja-tyyppinen käyttäjä ei voi rekisteröityä sovelluksessa.