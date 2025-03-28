# myapp/urls.py
from django.urls import path, include
from members.views import *

urlpatterns = [
    path("memners/", include([
        path('', MembersListView.as_view(), name='member-list'),
        path('create/', MembersCreateView.as_view(), name='member-create'),
        path('update/<uuid:pk>/', MembersUpdateView.as_view(), name='member-update'),
        path('delete/<uuid:pk>/', MembersDeleteView.as_view(), name='member-delete'),
    ])),
]
