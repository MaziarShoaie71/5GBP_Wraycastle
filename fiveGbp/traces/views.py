from django.shortcuts import render
from django.views.generic import TemplateView, View
from traces.models import GeneratedTracesModel
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.forms.models import model_to_dict
from django.conf import settings
from os import path, system, chdir
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
import pymongo
connectionToMongo = 'mongodb://localhost:27017/'


class TraceView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = "traces/traces.html"

    def get(self, request, *args, **kwargs):
        allTraces = GeneratedTracesModel.objects.order_by('-created_at').all()
        records = len(allTraces)
        RecInPage = 8 # if change it here, change it in TraceUpdater as well
        paginator = Paginator(allTraces, RecInPage)
        # page_ranges = range(1, paginator.num_pages+1)
        page_ranges = paginator.page_range
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, self.template_name, {'page_obj': page_obj,'page_ranges': page_ranges, 'records': records})



def TraceUpdater(request):
    page_number = request.GET.get('page_number')

    allTraces = GeneratedTracesModel.objects.order_by('-created_at').all()
    records = len(allTraces)
    RecInPage = 8 # if change it here, change it in TraceView as well
    paginator = Paginator(allTraces, RecInPage)
    page_nums = paginator.num_pages
    page_obj = paginator.get_page(page_number)
    doc = []
    for element in  page_obj:
        doc.append(model_to_dict(element))
    data = {"status": True, "payload": doc, "records": records, "page_nums": page_nums}
    return JsonResponse(data)



def TraceDelete(request):
    TestName = request.GET.get('TestName')
    TestName = TestName[4:] # to remove del_ from first of id of li in html

    try:
        GeneratedTracesModel.objects.filter(TestName=TestName).delete()
        TraceSeqDiagramPath = path.join(settings.BASE_DIR, 'analyzer/traces/')
        traceFileName = TraceSeqDiagramPath + TestName + '.*'
        system('sudo rm -f ' +  traceFileName)
        data = {"status": True, "error": TestName + " is removed"}
        # Todo: delete files .pcap and .svg as well
    except:
        data = {"status": False, "error": "Unable to remove " + TestName}
    return JsonResponse(data)



def loadTraceSVG(request):
    TestName = request.GET.get('TestName')

    traceSeqDiagramFilesPath = path.join(settings.BASE_DIR, 'analyzer/traces/')
    analyzerPath = path.join(settings.BASE_DIR, 'analyzer/')
    fileName = TestName + ".svg"
    ImageFileExists = path.isfile(traceSeqDiagramFilesPath + fileName)
    if not (ImageFileExists):
        chdir(analyzerPath)
        system('sudo ../../.env/bin/python3 main.py '+ traceSeqDiagramFilesPath + TestName + '.pcap')
        # cmdDocker = 'docker container run --rm -v ' + traceSeqDiagramFilesPath + ':/app/traceFiles sadeghkarimi/fivegseqdiagram:v1.1 traceFiles/' +  TestName + '.pcap'
    
    imageFile = open(traceSeqDiagramFilesPath + fileName, "rb")

    response = HttpResponse(imageFile)
    # As response is not json, dataType: 'json' is commented in Ajax 
    return response



def downloadTrace(request):

    TestName = request.GET.get('TestName')
    TestName = TestName[9:] # to remove download_ from first of id of li in html
    downloadFilesPath = path.join(settings.BASE_DIR, 'analyzer/traces/')
    fileName = TestName + '.pcap'
    print(fileName)
    fileContent = open(downloadFilesPath + fileName, 'rb')
    # response = HttpResponse(fileContent, content_type='application/force-download')
    # response['Content-Disposition'] = 'attachment; filename="{}"'.format(fileName)

    # return response



def loadSeqLinkText(request):
    frameId = str(request.POST.get('id'))
    testName = request.POST.get('testName')
    client = pymongo.MongoClient(connectionToMongo)
    db = client['traces_sequence_data']
    col = db['data']
    data = col.find_one({'name': testName, 'packetNumber': frameId}, {"_id": 0})
    client.close()
    return JsonResponse(data)

