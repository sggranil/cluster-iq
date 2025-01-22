from django.urls import path

import geographical.views

app_name = 'geographic'

urlpatterns = [
    path('', geographical.views.index, name='index'),
]