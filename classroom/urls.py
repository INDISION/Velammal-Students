from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.attendence, name="attendence"),
    path("results", views.results, name="results"),
    path("upload-results/<str:year>/<str:sem>", views.upload_results, name="upload-results"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
