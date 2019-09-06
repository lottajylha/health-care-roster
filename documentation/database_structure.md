# Tietokannan rakenne
 
## Tietokannan alustus
Paikallisesti suoritettuna sovellus käyttää SQL-tietokantaa sijainnissa application/roster.db. Sovelluksen käynnistyessä ensimmäistä kertaa tietokanta luodaan Flaskin SQLAlchemyn avulla. Herokussa on käytössä Herokun pilvessä oleva PostgreSQL-tietokanta.
Sovelluksen molempiin tietokantoihin alustetaan tarvittaessa seuraavat tietokantataulut:
### Account
CREATE TABLE account (
        id INTEGER NOT NULL,
        date_created DATETIME,
        date_modified DATETIME,
        name VARCHAR(100) NOT NULL,
        username VARCHAR(20) NOT NULL,
        password VARCHAR(300) NOT NULL,
        position VARCHAR(20) NOT NULL,
        weekmin INTEGER NOT NULL,
        weekmax INTEGER NOT NULL,
        PRIMARY KEY (id)
);

### Shift
CREATE TABLE shift (
        id INTEGER NOT NULL,
        day VARCHAR(20) NOT NULL,
        hour VARCHAR(5) NOT NULL,
        accepted BOOLEAN NOT NULL,
        doctors_needed INTEGER NOT NULL,
        nurses_needed INTEGER NOT NULL,
        practical_nurses_needed INTEGER NOT NULL,
        PRIMARY KEY (id),
        CHECK (accepted IN (0, 1))
);

### Usershift
CREATE TABLE usershift (
        account_id INTEGER,
        shift_id INTEGER,
        FOREIGN KEY(account_id) REFERENCES account (id),
        FOREIGN KEY(shift_id) REFERENCES shift (id)
);

## Tietokantakaavio
Kuvassa tämän hetkisen sovelluksen tietokantakaavio.
![tietokantakaavio](https://user-images.githubusercontent.com/36735637/64445636-a2418c80-d0df-11e9-85af-2fc831381807.jpg)

## Turvallisuus
- Käyttäjien syötteet validoidaan WTFormsin validointitoiminnallisuudella. 
- Käyttäjien salasanoja ei talleta tietokantaan selkokielisinä. Rekisteröinnin yhteydessä käyttäjä syöttää salasanan WTFormsin PasswordField-kenttään, jossa salasanan merkit on peitetty. Kun käyttäjä lähettää syötteen, annettu salasana validoidaan ensin WTFormsin validators-toiminnalisuudella. Validaattoreista käytetään
    * validators.Length(min=4, max=10) (syötetyn salasanan pituus on oltava 4-10 merkkiä)
    * validators.Required() (syöte ei saa olla tyhjä).
Salasanan ollessa validi, se koodataan UTF-8 -merkistöstandardin mukaiseksi. Koodatusta salasanasta muodostetaan hajautusarvo Flaskin Bcryptin avulla käyttäen Bcryptin metodia generate_password_hash(password, rounds). Lopuksi luodusta hajautusarvosta talletaan sen UTF-8 -dekoodattu versio.
Kirjatumisen yhteydessä salasanan syötteestä muodostetaan vastaavasti hajautusarvo ja sitä verrataan tietokannassa syötteenä annetun käyttäjänimeä vastaavan rivin salasanaan.
- SQL-injektiot on estetty. Tähän käytetään SQLAlchemyn params-metodia. Esimerkiksi kun työnantajan päivittää työntekijöiden viikkotuntimääriä, päivitys tehdään kyselyllä
    UPDATE account set weekmin = :minparam,"
                        " weekmax = :maxparam"
                        " WHERE account.id = :idparam;").params(minparam=weekmin, maxparam=weekmax, idparam=user_id),
jossa parametrin minparam arvoksi asetetaan työnantajan syöte minimituntimäärän kentästä (weekmin) ja parametrin maxparam arvoksi asetetaan työnantajan syöte maksimituntimäärän kentästä (weekmax).
Kaikki kyselyt on toteutettu vastaavasti parametrejä käyttäen.

## Yhteenvetokyselyt
Yksinkertaisten tietokantakyselyjen lisäksi käytössä on yksi yhteenvetokysely. Yhteenvetokyselyssä lasketaan tiettyyn työvuoroon (Shift) ilmottautuneet työntekijät (Account). Kysely on
    SELECT COUNT(*) FROM (SELECT Account.name, Account.position
                    FROM Account, Usershift WHERE Usershift.shift_id = :shiftparam
                    AND Usershift.account_id = account.id AND Account.position = :positionparam
                    GROUP BY Account.name, Account.position) AS alias;").params(shiftparam=shift_id, positionparam=position)
Kyselyn sisemmässä kyselyssä (alkaa SELECT Account.name, Account.position...) valitaan tulostettavalle riville taulun Account sarakkeet name ja position arvot. Seuraavaksi haetaan liitostaulusta Usershift riviä, jonka sarakkeen shift_id arvo vastaa parametria shift_id ja sarakkeen account_id arvo vastaa taulun Account rivin id:tä, jossa sarakkeen position arvo vastaa parametrin position arvoa. Lopuksi tulokset ryhmitellään taulun Account sarakkeiden name ja position perusteella.


## Jatkokehitys
Tarkemmin jatkokehityksestä löytyy tiedostosta [/documentation/further_development.md](https://github.com/lottajylha/health-care-roster/blob/master/documentation/further_development.md)