# COUNTRY CURRENCY AND EXCHANGE 

## Overview
A backend service that interfaces with external API services to retrieve list of countries and get their respective exchange rates. 
### External APIs
* Countries - https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies
* Exchange Rates - https://open.er-api.com/v6/latest/USD


## Installation

* Clone the repository:
```bash
git clone https://github.com/Tha-Orakkle/country_currency_and_exchange.git
cd country_currency_and_exchange
```
* Create and activate virtual env
```bash
python3 -m venv venv
source venv/bin/activate # Linux/MacOs
venv\bin\activate.bat # Windows
```
* Install dependencies
```bash
pip install -r requirements.txt
```
* set environmnet variables

Add the following variables to your `.env` file
```bash
SECRET_KEY='your_secret_key'
DEBUG=True
```
* Run server
```bash
python manage.py runserver
```
* Start celery worker

run these in separate terminals
```bash
redis-sever #termial 1
```
```bash
celery -A core worker --loglevel=info #termial 2
```

## Endpoints
* **POST** `/countries/refresh` - Hits both APIs to refresh the countries in the db and calculate teh estimated GDP of each country.

    * Response 503 External API Service Unavailable
```json
{
    "error": "External data source unavailable",
    "details": "Could not fetch data from [API name]"
}
```

* **GET** `/countries` - Get all countries. Supports filters and sorting - `?region=Africa` | `?currency=NGN` | `?sort=gdp_desc`
  * Response 200
```json
[
    {
        "id": 1,
        "name": "Nigeria",
        "capital": "Abuja",
        "region": "Africa",
        "population": 206139589,
        "currency_code": "NGN",
        "exchange_rate": 1600.23,
        "estimated_gdp": 25767448125.2,
        "flag_url": "https://flagcdn.com/ng.svg",
        "last_refreshed_at": "2025-10-22T18:00:00Z"
    },
    {
        "id": 2,
        "name": "Ghana",
        "capital": "Accra",
        "region": "Africa",
        "population": 31072940,
        "currency_code": "GHS",
        "exchange_rate": 15.34,
        "estimated_gdp": 3029834520.6,
        "flag_url": "https://flagcdn.com/gh.svg",
        "last_refreshed_at": "2025-10-22T18:00:00Z"
    }
]
```
* **GET** `countries/:name` - Get a specifi country by name (case-insensitive)
    - Response 200
```json
{
    "id": 1,
    "name": "Nigeria",
    "capital": "Abuja",
    "region": "Africa",
    "population": 206139589,
    "currency_code": "NGN",
    "exchange_rate": 1600.23,
    "estimated_gdp": 25767448125.2,
    "flag_url": "https://flagcdn.com/ng.svg",
    "last_refreshed_at": "2025-10-22T18:00:00Z"
}
```

* **DELETE** `countries/:name` - Delete a specifi country by name (case-insensitive)

    * Response 404 
```json
{
    "error": "Country not found"
}
```

* **GET**  `/status` - Show total countries and last refresh timestamp
    * Response 200
```json
{
  "total_countries": 250,
  "last_refreshed_at": "2025-10-22T18:00:00Z"
}
```

* **GET**  `/countries/image` - serve summary image that contains total number of countries and top 5 countries based on GDP


## Author
username: tha_orakkle <br>
email: adegbiranayinoluwa.paul@yahoo.com