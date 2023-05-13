from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from exchange import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.exchange_view, name='view'),



] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)