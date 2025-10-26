from django.urls import path

from base.views import (
    CountryRefreshView,
    SummaryImageView
)

urlpatterns = [
    path('countries/refresh', CountryRefreshView.as_view(), name='country-refresh'),
    path('countries/image', SummaryImageView.as_view(), name='countries-image')
]
