from django.urls import path
from .controllers import authentication, enviroment, control, scheduler, disease, others

urlpatterns = [
    path('authentication/login', authentication.login, name='login'),
    path('authentication/signup', authentication.signup, name='signup'),

    path('enviroment/get', enviroment.get, name='enviroment_get'),
    path('enviroment/update', enviroment.update, name='enviroment_update'),

    path('control/get', control.get, name='control_get'),
    path('control/mode/update', control.updateMode, name='control_mode_update'),
    path('control/device_state/update', control.updateDeviceState, name='control_device_state_update'),
    path('control/threshold/update', control.updateThreshold, name='control_threshold_update'),

    path('schedule/<str:id>', scheduler.getSchedule, name='schedule'),
    path('irrigate-schedule', scheduler.irrigateSchedule, name='irrigateSchedule'),
    path('ventilate-schedule', scheduler.ventilateSchedule, name='ventilateSchedule'),
    path('irrigateDaily', scheduler.irrigateDaily, name='irrigateDaily'),
    path('ventilateDaily', scheduler.ventilateDaily, name='ventilateDaily'),

    # path('disease/predict', disease.predict, name='disease_predict'),
]