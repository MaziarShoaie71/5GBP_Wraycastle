from django.urls import path
from fiveGApp import views

urlpatterns = [
    path('', views.fiveGbpApp.as_view(), name = "fiveGbpApp"),
    path('ajax/ueUpdater/', views.ueUpdater, name = "ueUpdater"),
    path('ajax/gNBUpdater/', views.gNBUpdater, name = "gNBUpdater"),
    path('ajax/amfUpdater/', views.amfUpdater, name = "amfUpdater"),
    path('ajax/smfUpdater/', views.smfUpdater, name = "smfUpdater"),
    path('ajax/ausfUpdater/', views.ausfUpdater, name = "ausfUpdater"),
    path('ajax/nrfUpdater/', views.nrfUpdater, name = "nrfUpdater"),
    path('ajax/nrfConfigLoader/', views.nrfConfigLoader, name = "nrfConfigLoader"),
    path('ajax/pcfUpdater/', views.pcfUpdater, name = "pcfUpdater"),
    path('ajax/udmUpdater/', views.udmUpdater, name = "udmUpdater"),
    path('ajax/udrUpdater/', views.udrUpdater, name = "udrUpdater"),
    path('ajax/upfUpdater/', views.upfUpdater, name = "upfUpdater"),
    path('ajax/nssfUpdater/', views.nssfUpdater, name = "nssfUpdater"),
    path('ajax/ScenariosRun/', views.ScenariosRun, name = "ScenariosRun"),
    path('ajax/LogHandler', views.LogHandler, name = "LogHandler"),

    path('ajax/nodeLogLevelUpdater', views.nodeLogLevelUpdater, name = "nodeLogLevelUpdater"),
    path('ajax/nodeLogLevelEditor', views.nodeLogLevelEditor, name = "nodeLogLevelEditor"),
    path('ajax/nodeLogLevelReset', views.nodeLogLevelReset, name = "nodeLogLevelReset"),


    
]
