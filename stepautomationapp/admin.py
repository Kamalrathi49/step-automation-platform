from django.contrib import admin
from .models import *
from .models import Country
from .models import City
from accountsapp.models import *

admin.site.register(UserData)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(ProjectTemplate)
admin.site.register(Steps)
admin.site.register(Documents)
admin.site.register(Customers)
admin.site.register(CustomerWorkflow)
admin.site.register(CustomerSteps)
admin.site.register(GuideeProflie)

# Register your models here.
