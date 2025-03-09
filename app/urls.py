from django.urls import path
from . import views

urlpatterns = [
    path('getData/', views.getData, name='getData'),
    path('manualWatering/', views.manualWatering, name='manualWatering'),
    path('manualVentilate/', views.manualVentilate, name='manualVentilate'),
]