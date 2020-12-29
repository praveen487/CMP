import django_filters
from django_filters import DateFilter,CharFilter
from CRM_app.models import Order

class OrderFilter(django_filters.FilterSet):
    class Meta:
        start_date = DateFilter(field_name="date_created", lookup_expr = 'gte')
        end_date = DateFilter(field_name="date_created", lookup_expr = 'lte')

        note= CharFilter(field_name='note', lookup_expr='icontains')
        model = Order
        fields = '__all__'
        exclude = ['customer','date_created']
