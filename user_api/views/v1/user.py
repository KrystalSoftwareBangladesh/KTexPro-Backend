from rest_framework import generics, permissions

from user_api.models import User

from user_api.serializers import UserProfileSerializer
from user_api.serializers import AssignGroupSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
            Return the authenticated user.
        """
        return self.request.user

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UserListView(generics.ListAPIView):
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class AssignGroupView(generics.UpdateAPIView):
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = AssignGroupSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    ]
