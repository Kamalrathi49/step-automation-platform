from django.contrib import admin
from .models import CustomerSteps, CustomerWorkflow, Customers, Documents, ProjectTemplate, Steps, UserData
from .models import Country
from .models import City

admin.site.register(UserData)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(ProjectTemplate)
admin.site.register(Steps)
admin.site.register(Documents)
admin.site.register(Customers)
admin.site.register(CustomerWorkflow)
admin.site.register(CustomerSteps)

# Register your models here.
