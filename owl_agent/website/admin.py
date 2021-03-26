from django.contrib import admin
from .models import Job_Seeker_Profile,Company_Profile,CV,Application,Job_Offer,User_Profile

# Register your models here.


admin.site.register(Job_Seeker_Profile)
admin.site.register(Company_Profile)
admin.site.register(CV)
admin.site.register(Application)
admin.site.register(Job_Offer)
admin.site.register(User_Profile)
