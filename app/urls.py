from django.urls import path
from . import views

urlpatterns = [
    path('getData/', views.getData, name='getData'),
    path('manualWatering/', views.manualWatering, name='manualWatering'),
    path('manualVentilate/', views.manualVentilate, name='manualVentilate'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('threshold/<str:id>/', views.getThreshold, name='threshold'),
    path('configThreshold/', views.config, name='configThreshold'),
    path('schedule/<str:id>/', views.getSchedule, name='schedule'),
    path('irrigate-schedule/', views.irrigateSchedule, name='irrigateSchedule'),
    path('ventilate-schedule/', views.ventilateSchedule, name='ventilateSchedule'),
    path('irrigateDaily/', views.irrigateDaily, name='irrigateDaily'),
    path('ventilateDaily/', views.ventilateDaily, name='ventilateDaily'),
]