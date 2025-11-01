from django.urls import path, include

from supplier_api.urls import v1


urlpatterns = [
    path('v1/', include(v1)),
]
