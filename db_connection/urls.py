from django.urls import path
from django.views.generic import TemplateView
from .views import DatabaseMetadataAPIView

urlpatterns = [
    path('', TemplateView.as_view(template_name="home.html"), name='home'),  # Root URL
    path('api/database-metadata/', DatabaseMetadataAPIView.as_view(), name='database-metadata'),
]
