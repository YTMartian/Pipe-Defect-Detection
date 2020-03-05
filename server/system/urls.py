from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  url(r'^index/$', views.index, name='index'),
                  url(r'^handle/$', views.handle, name='handle'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
