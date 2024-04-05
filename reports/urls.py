from django.urls import path
from . import views


urlpatterns = [
    path('wagerate/', views.create_wagerate, name='wage-rate-title'),
    path('wagerate/<int:pk>/', views.create_wagerate, name='wage-rate-title-detail'),
]