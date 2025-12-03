**AnturiAPI - Sensor management REST API**

AnturiAPI on FastAPI-pohjainen REST-rajapinta, jonka avulla voidaan hallita antureita, niiden mittaustuloksia sekä tilamuutoksia.

-----------------------------------------------------------------------------------------------------------------------------------

**Käytetyt teknologiat:**
- Python 3.13
- FastAPI 
- Uvicorn
- SQLModel
- SQLite
- Pydantic

- Venv
- Git & Github
- Vscode

------------------------------------------------------------------------------------------------------------------------------------

**Asennusohjeet:**

**1. Kloonaa projekti**
- Avaa terminaali ja siirry kansioon, johon haluat kloonata koodin
- Suorita kloonaus: git clone TÄHÄN LINKKI
- Siirry kloonattuun kansioon: cd AnturiAPI
  
**2. Luo ja aktivoi virtuaaliympäristö**

**Windows:**
  
  python -m venv .venv
  
  .venv\Scripts\Activate

 **Mac/Linux:**
  
  python3 -m venv .venv
  
  source .venv/bin/activate

**3. Asenna riippuvuudet:**

  pip install -r requirements.txt

**4. Käynnistä sovellus:**

  uvicorn app.main:app --reload

---------------------------------------------------------------------------------------------------------------------------------------

Palvelu käynnistyy osoitteeseen: 

http://127.0.0.1:8000

Swagger UI:

http://127.0.0.1:8000/docs

-----------------------------------------------------------------------------------------------------------------------------------------

**Käyttöohjeet/API Endpointit:**

**Sensors:**

**-POST/sensors:** Lisää uusi anturi (Anturin nimi, lohko & tila)

**-GET/sensors:** Listaa kaikki sensorit tai suodata statuksen perusteella

**-PATCH/sensors/{sensor_id}/status:** Päivitä sensorin status

**-PATCH/sensors/{sensor_id}/section:** Päivitä sensorin lohko

**-GET/sensors/by-section:** Hae tietyn lohkon sensorit + sensorin viimeisin mittaus

**-GET/sensors/{sensor_id}:** Hae yksittäisen anturin kaikki tiedot. Oletuksena näytetään 10 uusinta mittausta tai voit valita näyttämään mitta-arvot tietyn ajankohdan väliltä

**Measurements:**


**-POST/measurements:** Lisää mittaus. (Kyseinen endpoint luotu testaustarkoitukseen. Todellisuudessa anturi lähettäisi mittaustiedot palvelimelle tietyin väliajoin.)

**-DELETE/measurements/{measurement_id}:** Poista yksittäinen mittaus


**Status-changes:**


**-GET/sensors/{sensor_id}/status_changes:** Hae yksittäisen sensorin tilamuutokset


**Stats:**


**-GET/stats/error-events:** Listaa kaikki virhetilanteet graafia varten tai suodata yksittäisen sensorin mukaan

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




