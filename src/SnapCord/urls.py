from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from SnapCord import settings

urlpatterns = [
    path('staff/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('customer-service', include('customer_service.urls')),
    path('', include('home.urls')),
    path('publication/', include('publication.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
