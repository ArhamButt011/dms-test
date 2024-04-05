from django.urls import path
from . import views



urlpatterns = [
    path('Urllist/',views.UrlsListViews.as_view(),name='Url View'),
    path('Urllist/<int:id>/',views.UrlsListViews.as_view(),name='Url View'),



    path('company/',views.CompanyListView.as_view(),name='Company Detail'),
    path('company/<int:id>/',views.CompanyListView.as_view(),name='Company Detail'),

    path('Addendum/',views.AddendumView.as_view(),name='addendum'),
    path('estimating/',views.EstimatingListView.as_view(),name='estimating list'),
    path('estimating/<int:id>/', views.EstimatingListView.as_view(), name='estimating-detail'),



    path('proposals/', views.create_proposal, name='proposal-list'),
    path('proposals/<int:proposal_id>/', views.create_proposal, name='update-delete-proposal'),

    path('sendEmail/<int:estimating_id>/<int:gc_id>/', views.SendEmailView.as_view(), name='send-Email'),


    path('Qualification/',views.QualificationView.as_view(),name='Qualification list'),
    path('Qualification/<int:id>/',views.QualificationView.as_view(),name='Qualification detail'),


    # path('service/',views.ServiceViews.as_view(),name='service list'),
    # path('service/<int:id>/',views.ServiceViews.as_view(),name='service'),



    path('location/',views.LocationViews.as_view(),name='location list'),
    path('location/<int:id>/',views.LocationViews.as_view(),name='Location Detail'),


    path('Estimating_detail/',views.Estimating_detailView.as_view(),name='Estimating_detail list'),
    path('Estimating_detail/<int:id>/',views.Estimating_detailView.as_view(),name='Estimating_deatail'),


    #Dashboard urls 

    path('api/estimators/summary/', views.EstimatorSummaryView.as_view(), name='estimators-summary'),

    path('company_won_bashboard/', views.CompanyWonEstimates.as_view(), name='company-won-bashboard'),

    path('dmsDrectory/',views.DMS_DertoryView.as_view(),name='DMS-Derctory'),
    path('dmsDrectory/<int:id>/',views.DMS_DertoryView.as_view(),name='DMS-Derctory'),

    path('specificationDetail/',views.SpecificationDetailViews.as_view(),name='SpecificationDetail'),

    path('specification/',views.SpecificationViews.as_view(),name='SpecificationDetail'),

    path('jobtitle/',views.Job_titleViews.as_view(),name='job-tile'),
    path('Department/',views.DepartmentViews.as_view(),name='Department'),
    # path('GrandTotle/', views.Grand_totleSummaryView.as_view(), name='estimators-summary'),



]
