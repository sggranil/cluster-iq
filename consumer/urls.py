from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import consumer.views

app_name = 'consumer'

urlpatterns = [
    path('', consumer.views.index, name='index'),
    path('upload_datasets/', consumer.views.upload_datasets, name='upload_datasets'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
