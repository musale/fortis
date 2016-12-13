from django.conf.urls import url
from django.contrib import admin
from core.views import IndexPageView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^', IndexPageView.as_view(), name='home'),
    url(r'^admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
