from django.urls import path

from db_init import views

urlpatterns = [
    path('ads/', views.AddAdsData.as_view()),
    path('cat/', views.AddCatData.as_view()),
    path('loc/', views.AddLocData.as_view()),
    path('user/', views.AddUserData.as_view()),
]

