from rest_framework import routers
from knox import views as knox_views
from django.urls import re_path, path, include

from . import views

__user_router = routers.DefaultRouter()

#__user_router.register(r'users', views.UserViewSet)


__auth_urls = [
     path(r'login/', views.LoginView.as_view(), name='knox_login'),
     path(r'logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
     path(r'logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
     path(r'check_email', views.EmailCheckView.as_view(), name='check_username'),
     re_path(r'check_telephone', views.TelephoneCheckView.as_view(), name='check_telephone'),
     path('verify_phone', views.PhoneNumberVerifyView.as_view(), name='phone_verification'),
     path('resend_phone_code', views.PhoneCodeRenew.as_view(), name='resend_phone_code'),
     path('change_password', views.ChangePasswordView.as_view(), name='change_password'),

     
]

reset_password = [
     path('send_code/', views.ForgotPasswordView.as_view()),
     path('reset_password/', views.ResetPasswordView.as_view()),
    
]

user_management = [
     path('register',views.RegistrationView.as_view(),name = 'register' ),
     path('all_users', views.ListUsers.as_view(),name='users'),
     path('user', views.CurrentUser.as_view(),name='user'),
     path('update_user',views.UpdateUserViews.as_view(),name = 'update_user' ),
     path('delete/<int:pk>', views.DeleteUser.as_view()),
    
]



user_urls = [
    # path('', include(__user_router.urls)),
     path('auth/', include(__auth_urls)),
     path('users/',include(user_management)),
     path('reset_password/',include(reset_password))
     #path('register',views.UserViewSet.as_view(),name = 'register' ),
    ]

