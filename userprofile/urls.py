from django.urls import path
from . import views

urlpatterns = [
    path('edit/<int:id>/', views.profile_edit, name='edit'),
]