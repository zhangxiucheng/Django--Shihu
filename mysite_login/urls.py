"""mysite_login URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
import notifications.urls
from login import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", views.user_login),
    path("register/", views.register),
    path("logout/", views.user_logout),
    path("captcha/", include("captcha.urls")),
    path("blog/", include("blog.urls")),
    path("comments/", include("comments.urls")),
    path('reset_passowrd/', include('reset_passowrd.urls')),
    path('user_profile/', include('userprofile.urls')),
    path('mdeditor/', include('mdeditor.urls')),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('notice/', include('notice.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)