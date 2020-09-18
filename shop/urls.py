from django.urls import include, path
from django.contrib import admin
from .api import router

app_name = 'shop'
urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('', include(router.urls)),
]
