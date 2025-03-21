from django.urls import path
from . import views

urlpatterns = [
    path('getData/', views.getData, name='getData'),
    path('manualWatering/', views.turnOnWatering, name='manualWatering'),
    path('turnOffWatering/', views.turnOffWatering, name='turnOffWatering'),
    path('manualVentilate/', views.turnOnVentilate, name='manualVentilate'),
    path('turnOffVentilate/', views.turnOffVentilate, name='turnOffVentilate'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('smart/general/', views.getThreshold, name='threshold'),
    path('configThreshold/', views.config, name='configThreshold'),
    path('schedule/<str:id>/', views.getSchedule, name='schedule'),
    path('irrigate-schedule/', views.irrigateSchedule, name='irrigateSchedule'),
    path('ventilate-schedule/', views.ventilateSchedule, name='ventilateSchedule'),
    path('irrigateDaily/', views.irrigateDaily, name='irrigateDaily'),
    path('ventilateDaily/', views.ventilateDaily, name='ventilateDaily'),
    path('handleHumidity/', views.handleHumidity, name='handleHumidity'),
    path('handleTemperature/', views.handleTemperature, name='handleTemperature'),
    path('yolobit_api', views.yolobit_api, name='yolobit_api'),
    path('smart/mode/', views.updateMode, name='updateMode'),
    path('smart/state/', views.updateState, name='updateState'),
]