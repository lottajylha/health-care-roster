# Puutteita ja jatkokehitysideoita

## Puutteet ja rajoiteet
- Työnantaja voi lisätä vain työvuoron päivämäärällä ja kellonajalla, jotka on kovakoodattu. 
- Tietokannan lisättäville riveille asetetaan yksinkertaiset, helposti arvattavat id-arvot...
- ... ja samoja arvoja käytetään polun osotteissa sellaisenaan.
- Työantaja ei voi rekisteröityä sovelluksessa.
- Listojen järjestys muuttuu esimerkiksi työvoiman määrän päivityksessä, työvuorot voisi järjestää päivämäärän mukaan.
- Kun työnantaja yrittää muuttaa yhden työntekijän viikkotuntimäärää virheellisellä syötteellä, virheellinen syöte jää näkymään (kaikkiin kenttiin).

## Jatkokehitysideoita
- Kovakoodatun päivämäärä- ja kellonaikalistan sijaan voisi käyttää jotain valmista kalenteria.
- Työvuorolistalle voisi lisätä pidemmän aikavälin statuksen. Esimerkiksi, viikon työvuorolista olisi hyväksytty, jos se toteuttaa kaikkien työntekijöiden viikkotuntimäärät.
- Käyttäjälle voisi näyttää tilastoja omista työvuoroista, esimerkiksi aamu-, päivä- ja iltavuorojen osuudet.
- Toiminnallisuuden kasvaessa tietokantaa voisi muokata: sen sijaan, että taulussa Shift on sarakkeet doctors_needed, nurses_needed ja practical_nurses_needed, voisi tietokannassa olla taulu Staff, jossa sarakkeet jokaisen aseman tarvittavalle henkilömäärälle ja sen hetkiselle henkilömäärälle.
- Työvuoroon voisi liittyä viesti-toiminto, johon työvuoron työntekijät voisivat kirjoittaa raportteja työvuorosta.