from django.urls import path
from traces import views

urlpatterns = [
    path('', views.TraceView.as_view(), name = "traces"),
    path('ajax/TraceUpdater', views.TraceUpdater, name = "TraceUpdater"),
    path('ajax/TraceDelete', views.TraceDelete, name = "TraceDelete"),
    path('ajax/loadTraceSVG', views.loadTraceSVG, name = "loadTraceSVG"),
    path('ajax/downloadTrace', views.downloadTrace, name = "downloadTrace"),
    path('ajax/loadSeqLinkText', views.loadSeqLinkText, name = "loadSeqLinkText"),
]
