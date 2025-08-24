from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

import logging

from user_api.models import User

from user_api.serializers import TokenSerializer
from user_api.serializers import ChangePasswordSerializer


logger = logging.getLogger(__name__)


class LoginView(TokenObtainPairView):
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        request.data['username'] = request.data.get('credential', None)
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            response.data["message"] = "Login successful"

        return response


class TokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            response.data["message"] = "Access token refreshed successfully"

        return response


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({
                    "error": "Refresh token is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                "message": "Successfully logged out"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e)
            return Response({
                "error": "Invalid token or token already used"
            }, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
            Ensure user can only change their own password.
        """
        return self.request.user

    def patch(self, request, *args, **kwargs):
        """
            Handle partial updates for password change.
        """
        serializer = self.get_serializer(data=request.data, context={'request': request})   # noqa
        serializer.is_valid(raise_exception=True)
        self.get_object().set_password(serializer.validated_data['new_password'])   # noqa
        self.get_object().save()
        return Response({
            "message": "Password changed successfully!"
        }, status=status.HTTP_200_OK)
