from django.urls import path

import consumer.views

app_name = 'consumer'

urlpatterns = [
    path('', consumer.views.index, name='index'),
]