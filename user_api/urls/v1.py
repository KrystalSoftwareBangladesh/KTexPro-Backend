from django.urls import path
from rest_framework.routers import DefaultRouter

from user_api.views import v1


router = DefaultRouter()


router.register('roles', v1.GroupViewSet, basename='roles')


urlpatterns = [
    path('login', v1.LoginView.as_view(), name='login'),
    path('logout', v1.LogoutView.as_view(), name='logout'),
    path('refresh', v1.TokenRefreshView.as_view(), name='token-refresh'),
    path('change-password', v1.ChangePasswordView.as_view(), name='change-password'),   # noqa
    path('profile', v1.UserProfileView.as_view(), name='user-profile'),
    path('create', v1.CreateUserView.as_view(), name='create-user'),
    path('<int:pk>/assign-role', v1.AssignGroupView.as_view(), name='assign-role'),     # noqa
    path('list', v1.UserListView.as_view(), name='user-list'),
    path('permissions', v1.PermissionListView.as_view(), name='permission-list'),       # noqa
]

urlpatterns += router.urls
