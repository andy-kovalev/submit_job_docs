"""
URL configuration for submit_job_docs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url=settings.STATIC_URL + 'docs/img/favicon.ico', permanent=True)

urlpatterns = ([
    re_path(r'^favicon\.ico$', favicon_view),
    path('', include('docs_metadata.urls')),
    path('', include('docs_api.urls')),
    path('', include('docs_site.urls')),
    path('admin/', admin.site.urls),
])

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


def get_api_version(api_version=settings.DEFAULT_API_VERSION) -> str:
    if str(api_version).isdigit():
        return f'v{api_version}'
    else:
        return 'v1'


def correct_url_path(*args) -> str | list[str]:
    result = [u if u[-1] != '/' else u[:-1] for u in args]

    if len(args) == 1:
        return result[0]
    else:
        return result


def api_url_path(*args, **kwargs) -> str:
    _api_url = correct_url_path(settings.API_URL)
    if kwargs.get('api_version') is None:
        _api_version = get_api_version()
    else:
        _api_version = get_api_version(kwargs.get('api_version'))

    return '/'.join([_api_url, _api_version] + list(correct_url_path(args)) + [''])


def url_path(*args) -> str:
    return '/'.join(list(correct_url_path(args)) + [''])
