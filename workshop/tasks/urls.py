from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('projects/', project_list),
    path('projects/<int:pk>/', project_detail),
    #path('tasks/', task_list),
    #path('tasks/<int:pk>/', task_detail),
    #path('users/', user_list),
    #path('users/<int:pk>/', user_detail),
     path('auth/login/', TokenObtainPairView.as_view()),
     path('auth/refresh/', TokenRefreshView.as_view()),
     path('auth/verify/', TokenVerifyView.as_view()),
]