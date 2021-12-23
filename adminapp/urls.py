from django.urls import path
from . import views

urlpatterns = [
        path('dashboard/', views.dashboard, name='admin-dashboard'),
        path('accounts/', views.accounts, name='admin-accounts'),
        path('standardfiles/', views.standardfiles, name='admin-standardfiles'),
        path('standardsteps/', views.standardsteps, name='admin-standardsteps'),
        path('standardworklows/', views.standardworkflows, name='admin-standardworkflows'),
        path('customerworklows/', views.customerworkflows, name='admin-customerworkflows'),
        path('customerworklowsteps/', views.customersteps, name='admin-customerworkflowsteps'),
        path('customers/', views.customers, name='admin-customers'),
]