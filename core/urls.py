from django.urls import path

from base.views import CountryRefreshView

urlpatterns = [
    path('countries/refresh', CountryRefreshView.as_view(), name='country-refresh')
]
