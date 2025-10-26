from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .exceptions import ExternalAPIUnavailable
from .machine import RefreshCountryMachine

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
