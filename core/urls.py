from django.urls import path

from base.views import (
    CountryRefreshView,
    CountryListView,
    CountryRetrieveDestroyView,
    SummaryImageView
)

urlpatterns = [
    path('countries/refresh', CountryRefreshView.as_view(), name='country-refresh'),
    path('countries/image', SummaryImageView.as_view(), name='countries-image'),
    path('countries', CountryListView.as_view(), name='countries'),
    path('countries/<str:name>', CountryRetrieveDestroyView.as_view(), name='country-retrieve-destroy'),
]
