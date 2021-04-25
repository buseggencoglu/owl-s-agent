import django_filters
from .models import Job_Offer



class Job_Offer_Filter(django_filters.FilterSet):
    class Meta:
        model = Job_Offer
        fields = ['title','location','company','type']
