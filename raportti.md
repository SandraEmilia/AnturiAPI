# AnturiAPI - Loppuraportti

## 1. Johdanto

Tämän lopputyön tarkoituksena oli suunnitella ja toteuttaa REST API kuvitteellisen tehdashallin lämpötila-anturidatan keräämiseen. Rajapinnan tehtävänä oli hallita lämpötilasensoreita, niiden mittaustuloksia sekä sensoreihin liittyviä tilamuutoksia. REST-rajapinnan toteutus tehtiin Pythonilla ja FastAPI-kehyksellä. Dataa mallinnettiin ensin kovakoodatuilla listoilla ja myöhemmin käyttöön otettiin SQlite tietokanta. Tässä raportissa kerron APIN suunnittelusta sen toteutukseen sekä perustelen valitsemani ratkaisut ja reflektoin oppimaani. 

## 2. API:n suunnitteluvaihe ja rakenteellinen arkkitehtuuri

Lopputyön ohjeistus tuntui alkuunsa monimutkaiselta ja haastavalta, joten lähdin suunnittelemaan API:a hyvin pienin askelin perinteisesti paperille kirjoittaen. Aloitin siitä, että mietin mitä resursseja tarvitaan ja miten ne nimeän (Anturi = sensor, lohko = section, jne.). Mietin myös, mitä ominaisuuksia eri resursseilla on; esimerkiksi sensorilla on id, nimi, lohko ja status.  Seuraavaksi aloin miettiä vaadittuja toiminnallisuuksia ja muutin ne mielessäni funktioiksi. Kun paperilla oli lista erilaisia funktioita, mietin funktioille oikeat endpointit. 

Itse ohjelmaa aloin kirjoittamaan hyvin samalla kaavalla, jota olin tehnyt jo harjoittelutehtävissä. Datan jaoin kolmeen kovakoodattuun listaan; sensors, measurements ja status_changes. Kirjoitin ensin koko ohjelman main.py tiedostoon ja loin tarvittavat mallit models.py tiedostoon. Matkan varrella malleja kertyikin paljon enemmän, mitä osasin alun perin ajatella. Kun endpointit alkoivat olla hyvällä mallilla, aloin refaktoroimaan ohjelmaa. Olin alunperin ajatellut jakavani tietokantaoperaatiot useampaan crud-tiedostoon, kuten harjoitustehtävässä, mutta jako tuntui vaikealta, sillä moni funktio oli riippuvainen useammasta listasta samaan aikaan. Päädyin laittamaan kaikki operaatiot samaan crud-tiedostoon. Toki ne olisi voinut jakaa erilleen siinä kohtaa, kun listojen data oli siirretty tietokantaan, mutta koin, että tässä kohtaa ne voidaan jättää myös samaan tiedostoon. Tein jokaiselle resurssille oman router-tiedoston ja otin käyttöön APIrouterin. Myös endpointtien jako eri routereihin tuntui haastavalta, sillä useimmat endpointit alkoivat samalla prefixillä, vaikka toiminnallisuus ei olisi suoraan liittynyt juuri kyseiseen resurssiin. Lopuksi otin SQliten tietokannan käyttöön. Viimeisenä lisäsin ohjelmaan vielä CORS:in, sillä ohjeistuksessa luki, että "Anturien hallintaan ja datanäkymiä varten toteutetaan ainakin web-käyttöliittymä", joten ajattelin että ohjelma pitää olla käytettävissä muualtakin kuin local hostista. 

## 3. Valittujen Endpointtien perustelut

Ennen endpointtien suunnittelua, mietin mitkä resurssit kannattaa laittaa omiin listoihinsa. Sensorit -lista oli ratkaisuna selkeä, sillä niitä tarvitsisi monessa toiminnallisuudessa saada haettua ja käytettyä id:n perusteella. Mittauksille päädyin tekemään myös oman listan, sillä yksittäinen mittatulos piti saada poistettua ja se oli helpoin mielestäni tehdä id:n perusteella. Jos jokaisella mittauksella piti olla oma id, ne oli helpoin laittaa omaan listaansa. Myös tilamuutoksille päädyin tekemään oman listan, sillä jokaisen yksittäisen sensorin tilamuutokset piti olla haettavissa. Mietin myös aluksi pitäisikö myös lohkot olla omassa listassa, mutta koska lohkoja ei pitänyt saada haettua tai listattua, päädyin siihen, että riittää kun lohkon nimi on sensorin ominaisuutena ja sitä pystyy muuttamaan sensorin id:n perusteella. 

### Sensors endpointit
POST/sensors - Lisätään uusi sensori, sensorille asetetaan nimi (esim. sensor1), section (esim. A1) ja status (esim. online). Uusi sensori lisätään sensors-tauluun.

GET/sensors - Listaa joko kaikki anturit (Näytetään sensorin tunniste, lohko ja tila) tai voidaan suodattaa statuksen perusteella, jolloin ohjelma listaa kaikki sensorit, jotka ovat esim. offline tilassa.

PATCH/sensors/{sensor_id}/status - Voidaan muuttaa sensorin tilaa syöttämällä sensorin id ja haluttu uusi tila string muodossa. esim. online -> offline. Tilamuutos tallennetaan status_changes tauluun.

PATCH/sensors/{sensor_id}/section - Voidaan muuttaa lohkoa, johon sensori kuuluu, sensorin id:n perusteella.

GET/sensors/by-section - Listaa tietyn lohkon kaikki sensorit. Sensorista tuodaan tunniste, lohko, tila, viimeisin mittaus sekä aikaleima.

GET/sensors/{sensor_id} - Haetaan yksittäisen anturin kaikki tiedot id:n perusteella. Oletuksena näytetään 10 viimeisintä mittatulosta tai query parametrinä voidaan antaa start ja end datetime, jonka väliltä mittaukset näytetään. 

### Measurements endpointit
POST/measurements - Kyseinen endpoint on luotu ainoastaan ohjelman testausta varten. Todellisuudessa sensorit lähettäisivät mittausdataa suoraan selaimeen tietyin väliajoin, mutta testausta varten oli pakko luoda endpoint, jolla mittausdatan luomisen voi tehdä manuaalisesti. Olin alunperin ajatellut, että lämpötila ja timestamp lisätään vain siinä kohtaa kun luodaan uusi sensori, mutta sillä samalle sensorille pitää saada luotua useampi mittaustulos kyseinen ratkaisu ei olisi toiminut, vaan tarvittiin endpoint, jonka avulla voidaan tietylle sensorille lisätä niin monta mittatulosta, kuin halutaan. Jos mittaustulosta yritetään lisätä sensorille, joka on "error"-tilassa, mittausta ei voida lisätä, sillä ohjeistuksessa sanottiin, että virhetilassa anturi ei lähetä lämpötilatietoja. 

DELETE/measurements/{measurement_id} - Poistetaan yksittäinen mittaustulos id:n perusteella.

### Status-changes endpoint
GET/sensors/{sensor_id}/status_changes - Näyttää id:n perusteella yksittäisen anturin kaikki tilamuutokset ajankohtineen. 

### Stats endpoint
GET/stats/error-events - Tämä endpoint on luotu, jotta saadaan ulos sellaista dataa, jota voitaisiin käyttää graafin piirtämisessä. Endpoint palauttaa kaikki virhetilanteet (status = "error") aikaleimoineen tai sitten haku voidaan suodattaa tietyn sensorin id:llä, jolloin palautetaan yksittäisen sensorin virhetilanteet aikaleimoineen. 

## 4. Mitä opin projektin aikana?

Ensinnäkin oli hieno huomata, kuinka paljon oma osaaminen Pythonin parissa on kehittynyt lähiaikoina kun on tehnyt Backendiä juuri Pythonilla ja FastAPI:lla useampaankin projektiin. Syntaksi alkaa olla jo tuttua ja funktioita pystyy kirjoittamaan ilman suuria ponnisteluja. Tämän projektin aikana taito suunnitella REST API:n arkkitehtuuria kehittyi valtavasti. Päätin heti kunnianhimoisesti, että aion tehdä tämän Anturitehtävän, jossa itsellä on vapaammat kädet rajapinnan suunnittelun ja toteutuksen suhteen. Alkuun tehtävän ohjeistus herätti lähinnä kauhunsekaisia tunteita, mutta kun tehtävää lähti miettimään todella pienistä palasista eteenpäin kerrallaan, suunnitelma etenikin todella nopeasti ja sopivat endpointit oli jopa helppo miettiä. FastAPI:a olen nyt päässyt hyödyntämään jo parissakin eri projektissa ja mielestäni se on loistava ja helposti käytettävä kehys REST-rajapinnan toteutukseen.  Opin mielestäni myös hyvin hyödyntämään query parametrejä, jonka avulla vältyttiin turhilta endpointeilta. Erityisen ylpeä olen siitä, miten oma looginen ajattelu on kehittynyt sekä tämän projektin, että muutenkin opintojen aikana.

## 5. Tekoälyn käyttö

Jo projektin alussa päätin, että tulen hyödyntämään tekoälyä mahdollisimman vähän, sillä en halua jättää ohjelmointitaitojani tekoälyn varaan, kuitenkin projektin aikana tuli tilanteita, joissa hyödynsin chatGPT:tä työkaluna. Kuten muissakin projekteissa myös tässä käytin tekoälyä auttamaan selvittämään virheitä, joihin itse jäin jumiin, usein ne olivat pieniä syntaksivirheitä tai kirjoitusvirheitä, mutta parissa kohtaa itse koodissa oli käynyt ajatusvirhe. Olin myös pahasti jumissa siinä kohtaa kun refaktoroin ohjelmaa ja jaoin toiminnallisuuksia crudiin ja endpointteja routereihin, joten hain varmistusta siihen, että voin jättää kaikki funktiot samaan crud-tiedostoon ja siihen, miten endpointit kannattaa jaotella. Suoraan koodiin, en kokenut tarvitsevani apua juuri ollenkaan, sillä tämä tehtävä oli hyvin mallinnettavissa opintojakson aiemmin tehdyistä harjoituksista. Sparrauskaverina tekoäly on myös hyvä, ja kerron usein, miten olen ajatellut jonkun asian toteuttaa ja kysyn mielipidettä siihen. 
