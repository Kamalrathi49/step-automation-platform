from django.contrib import admin
from .models import ProjectTemplate, Steps, UserData
from .models import Country
from .models import City

admin.site.register(UserData)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(ProjectTemplate)
admin.site.register(Steps)

# Register your models here.
