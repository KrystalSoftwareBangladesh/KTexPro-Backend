from django.urls import path, include
from rest_framework.routers import DefaultRouter

from lead_api.views import v1


router = DefaultRouter()
router.register(r'leads', v1.LeadViewSet, basename='lead')

urlpatterns = [
    path('', include(router.urls)),
]
