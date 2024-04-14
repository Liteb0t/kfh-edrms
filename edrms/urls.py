from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('home.urls')),
    path("admin/", admin.site.urls),
]  # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# above code is commented so requests for files in "media" ...
# ... go through home.views.ViewProtectedFile instead