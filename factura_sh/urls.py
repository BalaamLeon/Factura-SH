from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.views.i18n import set_language

urlpatterns = [
    # path("select2/", include("django_select2.urls")),
    path('set_language/<language_id>/', set_language, 'set_language'),
    # Needed for locale change
    path('i18n/', include('django.conf.urls.i18n')),
]


urlpatterns += i18n_patterns(
    # Put translatable views here
    path('admin/', admin.site.urls),
    path('', include('apps.base.urls')),
)

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
