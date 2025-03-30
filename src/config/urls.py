"""
URL configuration for src project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from members.views.views import IndexPage, MembersCreateView, anggota_stats
from users.views.login_views import ChangePasswordAdminView, CustomPasswordChangeView, LogoutView, ProfileUserApiView, UserLoginView

urlpatterns = [
    path("", IndexPage.as_view()),
    path('api/anggota-stats/', anggota_stats, name='anggota_stats'),
    path("form-daftar/", MembersCreateView.as_view(), name="members-register"),
    path("admin/", admin.site.urls),
    path("", include('users.urls'), name="users"),
    path("", include('members.urls'), name="members"),
    path("auth/", include([
        path("login/", UserLoginView.as_view(), name="login"),
        path("logout/", LogoutView.as_view(), name="logout"),
        path("change-password/", CustomPasswordChangeView.as_view(), name="change-password"),
        path('change-password-admin/<uuid:user_id>/', ChangePasswordAdminView.as_view(), name="change-password-admin"),
        path('profile/', ProfileUserApiView.as_view(), name='profile'),
    ])),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
