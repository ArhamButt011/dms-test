from django.urls import path
from . import views

urlpatterns = [
    path('Project/',views.create_project,name='Project'), # type: ignore
    path('Project/<int:id>/', views.create_project, name='Project'),
    
    path('projectDrctory/<int:prjct_id>/',views.ProjectDetailListCreateView.as_view(),name='Project Directory'),
    path('delay/notice/', views.Delay_NoticeViews.as_view(),name='Delay notice'),

    path('delay/notice/<int:id>/', views.Delay_NoticeViews.as_view(),name='Delay notice'),
    
    path('delay_log/<int:id>/',views.Delay_LogViews.as_view(),name='Delay_log'),
    path('delay_log/',views.Delay_LogViews.as_view(),name='Delay_log'),
    
    path('rfi/',views.RFIViews.as_view(),name='RFI'),
    path('rfi/<int:id>/',views.RFIViews.as_view(),name='RFI'),
    
    path('pco/',views.pco_view,name='PCO'),
    path('pco/<int:id>/',views.pco_view,name='PCO'),
    
    path('pco_log/',views.Pco_LogView.as_view(),name='PCO Log'),
    path('pco_log/<int:id>/',views.Pco_LogView.as_view(),name='PCO Log'),

    
    path('rfi_log/',views.RFILogViews.as_view(),name='RFI_log'),

    path('rfi_log/<int:id>/',views.RFILogViews.as_view(),name='RFI_log'),
    
    path('tm/',views.tm_view,name='TM'),
    path('tm/<int:id>/',views.tm_view,name='TM'),
    
    path('send_email/<int:document_id>/',views.SendDocumentEmailView.as_view(),name='RFI_Email_send'),
    path('projectdashboard/', views.ProjectDashboardAPIView.as_view(), name='project-dashboard'),

    path('badging/', views.createBadging, name='Badging'), 
    path('badging/<int:id>/', views.createBadging, name='Badging'), 
    path('badging/<int:id>/<int:project_id>/', views.createBadging, name='create_badging_with_id_and_project_id'),


]