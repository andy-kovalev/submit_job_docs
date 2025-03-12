from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.generic import TemplateView

from docs_metadata.views_api import ActionView, ParseModeView
from docs_metadata.views_api import CommandViewSet, CompanyWelcomeViewSet, DocumentViewSet
from docs_metadata.views import CommandListView, CommandCreateView
from submit_job_docs.urls import api_url_path, url_path

docs_metadata_url = 'metadata'

urlpatterns = [
    path(url_path(docs_metadata_url), login_required(TemplateView.as_view(template_name='docs_metadata/main.html'))),

    path(url_path(docs_metadata_url, 'commands'), CommandListView.as_view(), name='metadata_command_list'),
    path(url_path(docs_metadata_url, 'commands', 'add'), CommandCreateView.as_view(), name='metadata_command_add'),

    path(api_url_path(docs_metadata_url, 'actions'), ActionView.as_view()),
    path(api_url_path(docs_metadata_url, 'parsemodes'), ParseModeView.as_view()),

    path(api_url_path(docs_metadata_url, 'commands'), CommandViewSet.as_view({'get': 'list', 'post': 'create'})),
    path(api_url_path(docs_metadata_url, 'commands', '<int:pk>'),
         CommandViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'})),

    path(api_url_path(docs_metadata_url, 'company', 'welcome'),
         CompanyWelcomeViewSet.as_view({'get': 'retrieve', 'post': 'create', 'patch': 'partial_update'})),
    path(api_url_path(docs_metadata_url, 'company', 'welcome', '<int:pk>'),
         CompanyWelcomeViewSet.as_view({'delete': 'destroy'})),

    path(api_url_path(docs_metadata_url, 'documents'), DocumentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path(api_url_path(docs_metadata_url, 'documents', '<int:pk>'),
         DocumentViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'})),

    path(url_path(docs_metadata_url), include('django.contrib.auth.urls'))
]
