from RelationAnalysis import views as relation_views

urlpatterns = {
    'relationSchedule': {
        '/': relation_views.schedule_status,
        'start': relation_views.schedule_start,
        'stop': relation_views.schedule_stop,
        'addJob': relation_views.add_job,
        'deleteJob': relation_views.delete_job,
        'updateJob': relation_views.update_job,
        'pauseJob': relation_views.pause_job,
        'show': relation_views.schedule_status,
    },
    'resolveAnn': relation_views.resolve_ann
}
