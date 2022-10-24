import os

from django.http import HttpResponse

from RelationAnalysisDjango import settings
from RelationAnalysisDjango.server.solvePDF import input_pdf


def pdfFile(request):
    try:
        if request.method == 'POST':
            pdfFile = request.FILES['pdfFile']
            pdfFile = os.path.join(settings.MEDIA_ROOT, pdfFile.name)
            with open(pdfFile, 'wb') as f:
                for pdfFile_Part in request.FILES['pdfFile'].chunks():
                    f.write(pdfFile_Part)
            mes = input_pdf(pdfFile)
            os.remove(pdfFile)
            return HttpResponse(mes)
        else:
            return HttpResponse('识别文件失败')
    except Exception:
        return HttpResponse('识别文件失败')