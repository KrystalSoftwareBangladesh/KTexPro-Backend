# from django.urls import path
from rest_framework.routers import DefaultRouter

from buyer_api.views import v1


router = DefaultRouter()


router.register(r'buyers', v1.BuyerViewSet, basename='buyers')


urlpatterns = []

urlpatterns += router.urls
