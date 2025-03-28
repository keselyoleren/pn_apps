# myapp/urls.py
from django.urls import path, include
from users.views.user_views import *

urlpatterns = [
    path("user/", include([
        path('', AccountUserListView.as_view(), name='user-list'),
        path('create/', AccountUserCreateView.as_view(), name='user-create'),
        path('update/<uuid:pk>/', AccountUserUpdateView.as_view(), name='user-update'),
        path('delete/<uuid:pk>/', AccountUserDeleteView.as_view(), name='user-delete'),
    ])),
]
