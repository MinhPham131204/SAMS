from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from django.http import JsonResponse
from .models import IrrigateDaily, VentilateDaily, Device_state, Schedule
import pytz
from django.utils import timezone
from datetime import timedelta
from apscheduler.triggers.cron import CronTrigger
def checkIrrigateTime():
    #print("Job checkIrrigateTime is running...")
    vn_tz = pytz.timezone('UTC')
    current_time = timezone.now().astimezone(vn_tz)
    current_time = current_time.replace(second=0, microsecond=0)
    
    # Check if irrigation time matches the current time
    schedule = Schedule.objects.filter(irrigatedTime=current_time).first()
    if schedule:
        #print("set water pump")
        Device_state.objects.filter(device_name="water_pump").update(state=True)
        # Tự động tắt sau duration nếu có
        if schedule.irrigatedDuration:
            turn_off_time = current_time + timedelta(minutes=schedule.irrigatedDuration)
            _scheduler.add_job(
                lambda: Device_state.objects.filter(device_name="water_pump").update(state=False),
                'date',
                run_date=turn_off_time,
                id=f"turn_off_pump_{current_time}",
                replace_existing=True
            )

        return JsonResponse({
            'success': True,
            'data': 1,
        })

    irrigateTime = IrrigateDaily.objects.filter(
        startTime__hour=current_time.hour,
        startTime__minute=current_time.minute
    ).values()
    if len(irrigateTime) > 0:
        Device_state.objects.filter(device_name="water_pump").update(state=True)
        return JsonResponse({
            'success': True,
            'data': 1,
        })
    else:
        endTime = IrrigateDaily.objects.filter(
            endTime__hour=current_time.hour,
            endTime__minute=current_time.minute
        )
        if len(endTime) > 0:
            Device_state.objects.filter(device_name="water_pump").update(state=False)
            return JsonResponse({
                'success': True,
                'data': 0,
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'No irrigation schedule found',
            })
        
def checkVentilateTime():
    #print("Job checkVentilateTime is running...")
    vn_tz = pytz.timezone('UTC')
    current_time = timezone.now().astimezone(vn_tz)
    current_time = current_time.replace(second=0, microsecond=0)
    schedule = Schedule.objects.filter(ventilatedTime=current_time).first()
    if schedule:
        #print("set fan")
        Device_state.objects.filter(device_name="mini_fan").update(state=True)
        # Tự động tắt sau duration nếu có
        if schedule.ventilatedDuration:
            turn_off_time = current_time + timedelta(minutes=schedule.ventilatedDuration)
            _scheduler.add_job(
                lambda: Device_state.objects.filter(device_name="mini_fan").update(state=False),
                'date',
                run_date=turn_off_time,
                id=f"turn_off_fan_{current_time}",
                replace_existing=True
            )

        return JsonResponse({
            'success': True,
            'data': 1,
        })
    
    ventilateTime = VentilateDaily.objects.filter(
        startTime__hour=current_time.hour,
        startTime__minute=current_time.minute
    ).values()
    if len(ventilateTime) > 0:
        Device_state.objects.filter(device_name="mini_fan").update(state=True)
        return JsonResponse({
            'success': True,
            'data': 1,
        })
    else:
        endTime = VentilateDaily.objects.filter(
            endTime__hour=current_time.hour,
            endTime__minute=current_time.minute
        )
        if len(endTime) > 0:
            Device_state.objects.filter(device_name="mini_fan").update(state=False)
            return JsonResponse({
                'success': True,
                'data': 0,
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'No ventilation schedule found',
            })

_scheduler = None

def start():
    global _scheduler
    # Don't start a new scheduler if one is already running
    if _scheduler is not None and _scheduler.running:
        return
    
    # Create scheduler with memory storage instead of database
    _scheduler = BackgroundScheduler()
    _scheduler.add_jobstore(MemoryJobStore(), 'default')
    
    # Add the irrigation check job
    _scheduler.add_job(
        checkIrrigateTime,
        trigger=CronTrigger(second=0),
        id='check_irrigate_time',
        replace_existing=True
    )
    _scheduler.add_job(
        checkVentilateTime,
        trigger=CronTrigger(second=0),
        id='check_ventilate_time',
        replace_existing=True
    )
    
    _scheduler.start()
    print("Scheduler started successfully!")