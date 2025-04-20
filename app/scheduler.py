from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from django.http import JsonResponse
from .models import IrrigateDaily, Device_state
import pytz
from django.utils import timezone

def checkIrrigateTime():
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    current_time = timezone.now().astimezone(vn_tz)
    irrigateTime = IrrigateDaily.objects.filter(
        startTime__hour=current_time.hour,
        startTime__minute=current_time.minute
    ).values()
    if len(irrigateTime) > 0:
        Device_state.objects.filter(device_name="water_pump").update(state=1)
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
            Device_state.objects.filter(device_name="water_pump").update(state=0)
            return JsonResponse({
                'success': True,
                'data': 0,
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'No irrigation schedule found',
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
        'cron',
        minute='*',
        id='check_irrigate_time',
        replace_existing=True
    )
    
    _scheduler.start()
    print("Scheduler started successfully!")