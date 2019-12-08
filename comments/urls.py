from . import views
from django.urls import path

app_name = 'comments'
urlpatterns = [
    path('<int:post_pk>', views.comment, name='comment'),
]
