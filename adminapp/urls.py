from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
        path('dashboard/', views.dashboard, name='admin-dashboard'),
        path('accounts/', views.accounts, name='admin-accounts'),
        path('standardfiles/', views.standardfiles, name='admin-standardfiles'),
        path('standardsteps/', views.standardsteps, name='admin-standardsteps'),
        path('standardworklows/', views.standardworkflows, name='admin-standardworkflows'),
]