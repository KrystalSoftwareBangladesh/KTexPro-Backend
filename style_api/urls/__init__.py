from django.urls import path, include

from style_api.urls import v1


urlpatterns = [
    path('v1/', include(v1)),
]
