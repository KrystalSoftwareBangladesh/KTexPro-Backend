from rest_framework.routers import DefaultRouter

from supplier_api.views import v1


router = DefaultRouter()


router.register(
    r'capability-types',
    v1.SupplierCapabilityTypeViewSet,
    basename='supplier-capability-types'
)
router.register(
    r'suppliers',
    v1.SupplierViewSet,
    basename='suppliers'
)

urlpatterns = []

urlpatterns += router.urls
