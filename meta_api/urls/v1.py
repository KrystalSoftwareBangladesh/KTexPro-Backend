from django.urls import path
from rest_framework.routers import DefaultRouter

from meta_api.views import v1


router = DefaultRouter()


urlpatterns = [
    path('seasons/', v1.SeasonListAPIView.as_view(), name='season-list'),
    path('departments/', v1.DepartmentListAPIView.as_view(), name='department-list'),   # noqa
]

urlpatterns += router.urls
