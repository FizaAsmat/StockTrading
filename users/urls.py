from django.urls import path
from .views import AdminLoginView, UserLoginView,SignUpView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/',SignUpView.as_view(),name='singup'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/',TokenRefreshView.as_view(),name='logout'),
    path('admin/',AdminLoginView.as_view(),name='admin'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]