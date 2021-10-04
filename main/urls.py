from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.home, name='home'),
    path('user/edit/<user_id>/', views.edit_user, name='edit_user'),
]