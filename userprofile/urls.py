from django.urls import path
from . import views

app_name = 'user_profile'
urlpatterns = [
    path('edit/<int:id>/', views.profile_edit, name='edit'),
    path('home/<int:id>/', views.profile_home, name='home'),
]
