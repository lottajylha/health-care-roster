# Käyttötapaukset ja niiden SQL-kyselyt

# Tietokannan alustus
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

## Käyttötapaukset

### Account (User)
Tietokantataulu Account vastaa sovelluksen rekisteröityneitä käyttäjiä (User). Account-tauluun liittyy toiminnallisuudet
- Create: Uusi käyttäjä lisätään tietokantaan, kun polussa /auth/new käyttäjä rekisteröityy syöttämällä nimen, käyttäjätunnuksen, salasanan ja aseman. Tämä hoidetaan kyselyllä 
    INSERT INTO account (name, username, password, position) VALUES (?, ?, ?, ?);
- Read: Kirjautumisen yhteydessä käyttäjää haetaan tietokannasta käyttäjätunnuksella, tähän käytetään kyselyä
    SELECT * FROM account WHERE account.username = :userparam;
Kirjatumisen yhteydessä tarkastetaan, että vastaako käyttäjän antamasta syötteestä muodostettu hajatusarvo tietokannassa käyttäjään liittyvää salasanaa. Tämä toteutetaan kyselyllä
    SELECT * FROM account WHERE account.password = :passwordparam;
Työnantaja-tyypin käyttäjän GET-pyyntö polkuun /users listaa kaikki sovellukseen rekisteröityneet käyttäjät. Täma toteutetaan kyselyllä
    SELECT * FROM account;
Työntekijän asema haetaan polussa /users kyselyllä
    SELECT position FROM account WHERE account.id = :param;
Työnantajan päivittäessä työntekijän viikkotuntimäärää (ks. Update), työntekijän sen hetkinen viikkotuntiminimi ja -maksimi haetaan kyselyllä
    SELECT weekmin, weekmax from account WHERE account.id = :idparam;
- Update: Työnantaja-tyypin käyttäjä voi muuttaa työntekijän viikkotuntiminimiä ja -maksimia. Tiedon päivitys tapahtuu polussa users/<user_id> ja se tehdään kyselyllä
    UPDATE account set weekmin = :minparam, weekmax = :maxparam WHERE account.id = :idparam;

## Shift
Tietokantataulu Shift vastaa sovelluksessa olevia työvuoroja. Shift-tauluun liittyy täysi CRUD-toiminnallisuus, eli toiminnallisuudet
- Create: Työnantaja-tyypin käyttäjä voi lisätä uuden työvuoron tietokantaan polussa roster/new. tiedon lisäys toteutetaan kyselyllä
    INSERT INTO shift (name, username, password, weekmin, weekmax) VALUES (?, ?, ?, 0, 0);
- Read: Tietokannassa olevat työvuorot haetaan polussa /roster, tämä tapahtuu kyselyllä
    SELECT * FROM shift;
Työvuoroa haetaan tietokannasta sen id:llä polussa /roster. Tämä toteutetaan kyselyllä
    SELECT * FROM shift WHERE shift.id = :param;
Työvuoroon liittyvien työntekijöiden määrää haetaan polussa /roster. Esimerkiksi sairaanhoitajien määrä haetaan kyselyllä
    SELECT nurses_needed FROM shift WHERE shift.id = ?;
- Update: Työnantaja-tyypin käyttäjä voi päivittää työvuoroon tarvittavien työntekijöiden määriä polussa /roster. Esimerkiksi työvuoroon tarvittavien lääkäreiden määrä tapahtuu kyselyllä
    UPDATE shift set doctors_needed = :doctorsparam where shift.id = :shiftparam;
- Delete: Työnantaja-tyypin käyttäjä voi poistaa työvuoron polussa /roster. Tämä toteutetaan kyselyllä
    DELETE FROM shift WHERE shift.id = :param;

## Usershift
Usershift on liitostaulu taulujen Account ja Shift välillä. Siihen liittyy toiminnallisuudet
- Create: Kun käyttäjälle lisätään työvuoro polussa /roster, lisätään tauluun Usershift tätä vastaava rivi. Tämä toteutuu kyselyllä
    INSERT INTO usershift (account_id, shift_id) VALUES (?, ?);
- Read: Polussa /roster tarkastetaan, onko tietty työvuoro käyttäjän työvuoro. Taulusta Usershift haetaan riviä työntekijän ja työvuoron id:illä kyselyllä
    SELECT * FROM usershift WHERE account_id = ? AND shift_id = ?;
- Delete: Käyttäjä voi poistaa itseltään työvuoron polussa /rosterja tämä toteutuu kyselyllä
    DELETE FROM usershift WHERE account_id = ? AND shift_id = ?;

### Yhteenvetokyselyt
- Työvuoroon liittyvien työntekijöiden määrä haetaan polussa /roster kyselyllä
    SELECT COUNT(*) FROM (SELECT Account.name, Account.position
                    FROM Account, Usershift WHERE Usershift.shift_id = :shiftparam
                    AND Usershift.account_id = account.id AND Account.position = :positionparam
                    GROUP BY Account.name, Account.position) AS alias;

## Muut
- Työntekijälle näytetään hänen tietokantaan talletetuista tiedoista  työvuorot (date ja hour), ja ne haetaan polussa /users/get/<user_id> kyselyllä
    SELECT shift.day, shift.hour
            FROM shift JOIN usershift ON usershift.shift_id = shift.id
            JOIN account ON usershift.account_id = :param AND account.id = :param
            GROUP BY shift.day, shift.hour;
- Työvuoroon liittyvät työntekijät (name ja position) haetaan polussa /roster kyselyllä
    SELECT Account.name, Account.position
                    FROM account JOIN usershift ON usershift.account_id = account.id
                    JOIN shift ON usershift.shift_id = :param AND shift.id = :param
                    GROUP BY Account.name, Account.position;