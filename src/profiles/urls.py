
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.profile_list_view, name="profile-list"),
    path('<str:username>/', views.profile_detail_view, name="profile-view"),
    
]
