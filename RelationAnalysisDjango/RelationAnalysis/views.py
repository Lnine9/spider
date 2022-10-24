import json

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from RelationAnalysis.server.central_control import CentralControl, RelationType
from RelationAnalysis.tool.create_ann_obj import create_ann
from RelationAnalysis.tool.dbobj_json import to_json
from RelationAnalysis.server.job_method import get_job_method


def schedule_status():
    return JsonResponse({'job': str(
        [{'id': job.id, 'name': job.name, 'pending': job.pending, 'trigger': job.trigger} for job in
         CentralControl.scheduler.get_jobs()])})


def schedule_start():
    CentralControl.schedule_start()
    return schedule_status()


def schedule_stop():
    CentralControl.schedule_stop()
    return schedule_status()


@csrf_exempt
def resolve_ann(data):
    announcement = create_ann(data['ann_type'], data['ann'])
    announcement = CentralControl().resolver(announcement, RelationType.immediate)
    json_str = json.dumps(announcement, ensure_ascii=False, default=lambda x: to_json(x))
    return HttpResponse(json_str)


def add_job(data):
    job_id = data['jobId']
    params = [data.get('params', None), ]
    job_method = get_job_method(job_id)
    if job_method:
        CentralControl.add_job(job_id, job_method, minutes=int(data.get('minutes', 4)), args=params)
    return schedule_status()


def delete_job(data):
    CentralControl.delete_job(data['jobId'])
    return schedule_status()


def update_job():
    return None


def pause_job(data):
    CentralControl.pause_job(data['jobId'])
    return schedule_status()
