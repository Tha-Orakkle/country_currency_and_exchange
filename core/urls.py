from django.urls import path

from base.views import (
    CountryRefreshView,
    CountryListView,
    SummaryImageView
)

urlpatterns = [
    path('countries/refresh', CountryRefreshView.as_view(), name='country-refresh'),
    path('countries/image', SummaryImageView.as_view(), name='countries-image'),
    path('countries', CountryListView.as_view(), name='countries')
]
