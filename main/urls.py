from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.home, name='home'),
    path('search_user/', views.search_user, name='search_user'),
    path('user/edit/<user_id>/', views.edit_user, name='edit_user'),
    path('user/delete/<user_id>/', views.delete_user, name='delete_user'),
]