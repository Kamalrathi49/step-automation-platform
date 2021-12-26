from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('stepautomationapp.urls')),
    path('adminuser/', include('adminapp.urls')),
    # path('auth/', include('accountsapp.urls')),
    path('forms/',include('userforms.urls')),
]

handler404 = 'stepautomationapp.views.error_404'
# handler500 = 'stepautomationapp.views.error_500'
# handler403 = 'stepautomationapp.views.error_403'
# handler400 = 'stepautomationapp.views.error_400'