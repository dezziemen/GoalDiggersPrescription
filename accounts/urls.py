from . import views
from django.urls import path, include

app_name = 'accounts'

# Create your views here.
urlpatterns = [
    path('create_user/', views.create_user, name='create_user'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]