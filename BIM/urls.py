from django.urls import path
from . import views

urlpatterns = [
    path('BimData/',views.BIMViews.as_view(),name='BIM'),
    path('BimData/<int:id>/', views.BIMViews.as_view(), name='BIM'),
    ]