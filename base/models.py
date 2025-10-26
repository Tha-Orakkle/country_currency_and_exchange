from django.db import models

import uuid


class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True, null=False, blank=False)
    capital = models.CharField(max_length=64, null=True, blank=True)
    region = models.CharField(max_length=64, null=True, blank=True)
    population = models.IntegerField()
    currency_code = models.CharField(max_length=3, null=True, blank=True)
    exchange_rate = models.FloatField(null=True, blank=True)
    estimated_gdp = models.FloatField(null=True, blank=True)
    flag_url = models.URLField(null=True, blank=True)
    last_refreshed_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        """
        String representation of the Country Object
        """
        return(
            f"<Country - {self.id}> {self.name}"
            f"\n   Capital - {self.capital}"
            f"\n   Region - {self.region}"
            f"\n   Poulation - {self.population}"
            f"\n   Currency Code - {self.currency_code}"
            f"\n   Exchange Rate - {self.exchange_rate}"
            f"\n   Estimated GDP - {self.estimated_gdp}"
            f"\n   Last Refreshed At  - {self.last_refreshed_at}"
        )


class CountryMeta(models.Model):
    total_countries = models.IntegerField()
    last_refreshed_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        """
        Strng representation of the CountryMeta object
        """
        return (
            f"<CountryMeta> data as at {self.last_refreshed_at}"
            f"\n   Total Countries {self.total_countries}"
        )
