from django.urls import path, include

from RelationAnalysis import views

relation_schedule_urls = [
    path('start/', views.schedule_start),
    path('stop/', views.schedule_stop),
    path('show/', views.schedule_status),
    # path('relation_schedule/', include(distribute_task)),
]

urlpatterns = [
    path('relationSchedule/', include(relation_schedule_urls)),
    path('resolveAnn', views.resolve_ann)
]
