from django.contrib import admin
from django.urls import path

from RelationAnalysisDjango import views
from ViewLayer.util.ControlView import ControlView

urlpatterns = [
    path('', admin.site.urls),
    # path('admin/', admin.site.urls),
    path('upload/pdfFile/', views.pdfFile),
    path('<path:url>', ControlView.as_view)
]
