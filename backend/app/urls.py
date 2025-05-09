from django.urls import path
from . import views
# from controllers import disease_detection
from .controllers import authentication, enviroment, control, schedulter

urlpatterns = [
    path('authentication/login', authentication.login, name='login'),
    path('authentication/signup', authentication.signup, name='signup'),

    path('enviroment/get', enviroment.get, name='enviroment_get'),
    path('enviroment/update', enviroment.update, name='enviroment_update'),

    path('control/get', control.get, name='control_get'),
    path('control/mode/update', control.updateMode, name='control_mode_update'),
    path('control/device_state/update', control.updateDeviceState, name='control_device_state_update'),
    path('control/threshold/update', control.updateThreshold, name='control_threshold_update'),

    path('schedule/<str:id>', schedulter.getSchedule, name='schedule'),
    path('irrigate-schedule', schedulter.irrigateSchedule, name='irrigateSchedule'),
    path('ventilate-schedule', schedulter.ventilateSchedule, name='ventilateSchedule'),
    path('irrigateDaily', schedulter.irrigateDaily, name='irrigateDaily'),
    path('ventilateDaily', schedulter.ventilateDaily, name='ventilateDaily'),

    # path('disease-detection', views.diseaseDetection, name='diseaseDetection'),
]