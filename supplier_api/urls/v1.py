from rest_framework.routers import DefaultRouter

from supplier_api.views import v1


router = DefaultRouter()


router.register(
    r'capability-types',
    v1.SupplierCapabilityTypeViewSet,
    basename='suppliers'
)


urlpatterns = []

urlpatterns += router.urls
