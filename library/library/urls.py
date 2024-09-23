from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.urls import include, path

from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", RedirectView.as_view(url="/archive/", permanent=True)),
    path('archive/', include('archive.urls', namespace='archive')),
    # path('auth/', include('accounts.urls', namespace='accounts')),
    # path('lib-admin/', include('lib_admin.urls', namespace='lib-admin')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + debug_toolbar_urls()




