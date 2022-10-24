from django.urls import include

from ViewLayer.views import show_task
from RelationAnalysis.router import urlpatterns as relation

test = {
    '/': show_task
}

urlpatterns = {
    "test": test,
    "relation": relation
}
