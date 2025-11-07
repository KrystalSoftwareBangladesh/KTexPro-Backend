from rest_framework.routers import DefaultRouter

from style_api.views import v1

router = DefaultRouter()
router.register('style-status', v1.StyleStatusViewSet, basename='style-status')

urlpatterns = router.urls
