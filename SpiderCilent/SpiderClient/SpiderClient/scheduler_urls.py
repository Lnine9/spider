from django.conf.urls import url

from . import view

urlpatterns = [
    url(r'^start/', view.scheduler_start),
    url(r'^close/', view.scheduler_shutdown),
    url(r'^add$', view.scheduler_add),
    url(r'^remove$', view.scheduler_remove),
    url(r'^list/', view.scheduler_list),
    url(r'^log/', view.scheduler_log),
]
