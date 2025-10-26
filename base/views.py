from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response

from .exceptions import ExternalAPIUnavailable
from .filters import CountryFilter, CountrySortFilter
from .machine import RefreshCountryMachine
from .models import Country, CountryMeta
from .serializers import CountrySerializer


class CountryRefreshView(APIView):

    def post(self, request):
        
        machine = RefreshCountryMachine()
        try:
            machine.refresh_countries()
        except ExternalAPIUnavailable as e:
            return Response({
                'error': 'External data source unavailable',
                'details': f'Could not fetch data from {e.api_name}'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
        return Response({
            'status': 'success',
            'message': 'Countries refreshed successfully.'
        }, status=status.HTTP_200_OK)


class SummaryImageView(APIView):
    def get(self, request):
        from django.conf import settings
        file_path = settings.BASE_DIR / 'cache/summary.png'
        if not file_path.exists():
            return Response({
                'error': 'Summary image not found'
            }, status=status.HTTP_404_NOT_FOUND)
        return FileResponse(open(file_path, 'rb'), content_type='image/png')


class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = [DjangoFilterBackend, CountrySortFilter]
    filterset_class = CountryFilter


class CountryRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    lookup_field = 'name'
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    
    def get_object(self):
        name = self.kwargs.get(self.lookup_field)
        try:
            return self.queryset.get(name__iexact=name)
        except Country.DoesNotExist:
            raise NotFound({'error': 'Country not found'})
    
    
class StatusView(APIView):
    def get(self, request):
        c_meta = CountryMeta.objects.first()

        return Response({
            'total_countries': c_meta.total_countries if c_meta else 0,
            'last_refreshed_at': c_meta.last_refreshed_at if c_meta else None
        })