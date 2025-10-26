from django.utils.timezone import now
import requests
from requests.exceptions import RequestException


from .exceptions import ExternalAPIUnavailable
from .models import Country, CountryMeta

class RefreshCountryMachine:
    RC_URL = "https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies"
    ER_URL = "https://open.er-api.com/v6/latest/USD"
    
    def create_or_update_countries(self, countries_data, exchange_rates):
        existing = Country.objects.in_bulk(field_name='name')
        fields = [f.name for f in Country._meta.get_fields()
                  if f.name not in ['id', 'name', 'last_refreshed_at']]
        new_objs = []
        to_update = []

        for item in countries_data:
            name = item.get('name')
            if name in existing:
                country = existing[name]
                to_update.append(country)
            else: 
                country = Country(name=name)
                new_objs.append(country)

            country.capital = item.get('capital')
            country.region = item.get('region')
            country.population = item.get('population')
            country.flag_url = item.get('flag')
                
            currencies = item.get('currencies', [])
            c_code = currencies[0].get('code') if currencies else None
            country.currency_code = c_code

            if not c_code:
                country.exchange_rate = None
                country.estimated_gdp = 0
            elif c_code and not exchange_rates.get(c_code, None):
                country.exchange_rate = None
                country.estimated_gdp = None
            else:
                rate = exchange_rates[c_code]
                country.exchange_rate = rate
                country.estimated_gdp = self.calculate_gdp(country)
        
        Country.objects.bulk_create(new_objs)
        Country.objects.bulk_update(to_update, fields=fields)
     
    def calculate_gdp(self, country):
        from random import randint
        rdm = randint(1000, 2000)
        return (country.population * rdm) / country.exchange_rate
    
    def fetch_countries(self):
        try:
            res = requests.get(self.RC_URL, timeout=5)
            res.raise_for_status()
            res_json = res.json()
        except RequestException:
            raise ExternalAPIUnavailable(api_name='restcountries')

        return res_json

    def fetch_exchange_rates(self):
        try:
            res = requests.get(self.ER_URL, timeout=5)
            res.raise_for_status()
            res_json = res.json()
        except RequestException:
            raise ExternalAPIUnavailable(api_name='exchangerate-api')

        return res_json.get('rates', {})
   
    def update_countries_meta(self):
        c_meta = CountryMeta.objects.first()
        _now = now()
        count = Country.objects.count()

        if not c_meta:
            CountryMeta.objects.create(
                total_countries=count,
                last_refreshed_at=_now
            )
        else:
            c_meta.total_countries = count
            c_meta.last_refreshed_at = _now
            c_meta.save()
    
    def refresh_countries(self):
        countries = self.fetch_countries()
        exchange_rates = self.fetch_exchange_rates()
        
        self.create_or_update_countries(countries, exchange_rates)
        self.update_countries_meta()
        