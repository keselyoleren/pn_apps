# myapp/urls.py
from django.urls import path, include
from members.views import *

urlpatterns = [
    path("members/", include([
        path('', MembersListView.as_view(), name='member-list'),
        path('create/', MemebersAdminCreateView.as_view(), name='member-create'),
        path('update/<uuid:pk>/', MembersUpdateView.as_view(), name='member-update'),
        path('delete/<uuid:pk>/', MembersDeleteView.as_view(), name='member-delete'),
    ])),
]
