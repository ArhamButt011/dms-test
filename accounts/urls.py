from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [

    # User Registration, Login, and Profile URLs
    
    path('register/', views.UserRegistrationView.as_view(), name="register"),
    path('register/<int:id>/', views.UserRegistrationView.as_view(), name="register"),

    path('login/', views.UserLoginViews.as_view(), name="login"),
    path('profile/', views.UserProfileViews.as_view(), name="profile"),
    
    
    
    path('api/token/', views.UserLoginViews.as_view(), name='token-obtain-pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),


    # User Approval and Disapproval by Admin URLs   
    path('approve_user/<int:user_id>/', views.approve_user, name='approve_user'),

    path('disapprove_user/<int:user_id>/', views.disapprove_user, name='disapprove_user'),



    path('change_password/', views.UserChangePasswordViews.as_view(), name="change_password"),
    path('send_reset_password_email/', views.SendEmailResetPasswordViews.as_view(), name="send_reset_password_email"),
    path('password-reset-confirm/<uidb64>/<token>/', views.UserPasswordResetViews.as_view(), name='password-reset-confirm'),
    

]