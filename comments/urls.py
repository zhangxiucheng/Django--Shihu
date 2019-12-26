from . import views
from django.urls import path

app_name = 'comments'
urlpatterns = [
    path('<int:id>', views.comment, name='comment'),
]
