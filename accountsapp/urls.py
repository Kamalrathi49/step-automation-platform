from django.urls import path
from accountsapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/<str:userdata_invite_code>', views.guiee_signup, name='guidee-signup'),
    path('dashboard/', views.guidee_dashboard, name='guidee-dashboard'),
    path('steps/<int:project_template_id>/', views.guidee_steps, name='guidee-steps'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)