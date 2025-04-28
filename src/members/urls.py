# myapp/urls.py
from django.urls import path, include
from members.views.certivicate_view import *
from members.views.ikt_view import *
from members.views.perguruan_view import *
from members.views.views import *

urlpatterns = [
    path("members/", include([
        path('', MembersListView.as_view(), name='member-list'),
        path('create/', MemebersAdminCreateView.as_view(), name='member-create'),
        path('update/<uuid:pk>/', MembersUpdateView.as_view(), name='member-update'),
        path('detail/<uuid:pk>/', MemberDetailView.as_view(), name='member-detail'),
        path('delete/<uuid:pk>/', MembersDeleteView.as_view(), name='member-delete'),
        path('download/<uuid:pk>/', MemberPDFView.as_view(), name='member-download'),
    ])),

    path("ikt/", include([
        path('', IKTListView.as_view(), name='ikt-list'),
        path('create/', IKTCreateView.as_view(), name='ikt-create'),
        path('update/<uuid:pk>/', IKTUpdateView.as_view(), name='ikt-update'),
        path('detail/<uuid:pk>/', IKTDetailView.as_view(), name='ikt-detail'),
        path('delete/<uuid:pk>/', IKTDeleteView.as_view(), name='ikt-delete'),
    ])),

    path("certificate/", include([
        path('', CertificateListView.as_view(), name='certificate-list'),
        path('create/', CertificateCreateView.as_view(), name='certificate-create'),
        path('update/<uuid:pk>/', CertificateUpdateView.as_view(), name='certificate-update'),
        path('delete/<uuid:pk>/', CertificateDeleteView.as_view(), name='certificate-delete'),
    ])),

    path("perguruan/", include([
        path('', PerguruanListView.as_view(), name='perguruan-list'),
        path('create/', PerguruanCreateView.as_view(), name='perguruan-create'),
        path('update/<uuid:pk>/', PerguruanUpdateView.as_view(), name='perguruan-update'),
        path('delete/<uuid:pk>/', PerguruanDeleteView.as_view(), name='perguruan-delete'),
    ])),

    path('bulk-upload/', MembersBulkUploadView.as_view(), name='member-bulk-upload'),
    path('download-template/', DownloadMemberTemplateView.as_view(), name='download-member-template'),


    path("api/", include([
        path('search/pelatih-cabang/', pelatih_cabang_list, name='pelatih_cabang_list'),
    ]))
    
]
