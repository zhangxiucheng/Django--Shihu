from . import views
from django.urls import path

app_name = 'comments'
urlpatterns = [
    path('<int:id>/<int:reply>/', views.comment, name='reply'),
    path('<int:id>', views.comment, name='comment'),
]
