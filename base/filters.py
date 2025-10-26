from rest_framework.filters import OrderingFilter
import django_filters

from .models import Country

class CountryFilter(django_filters.FilterSet):
    region = django_filters.CharFilter(field_name='region', lookup_expr='iexact')
    currency = django_filters.CharFilter(field_name='currency_code', lookup_expr='iexact')
    
    class Meta:
        model = Country
        fields = ['region', 'currency']
        
        
class CountrySortFilter(OrderingFilter):
    ordering_param = 'sort'
    
    SORTING_MAP = {
        'gdp_desc': '-estimated_gdp',
        'gdp_asc': 'estimated_gdp'
    }
    
    def get_ordering(self, request, queryset, view):
        sort_value = request.query_params.get(self.ordering_param)
        if sort_value:
            mapped = self.SORTING_MAP.get(sort_value)
            if mapped:
                return [mapped]
            
        return super().get_ordering(request, queryset, view)