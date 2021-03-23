from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.helpers import Auth0Helper
from users.models import Admin
from users.serializers import AdminSerializer

helper = Auth0Helper()


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up_user(request):
    if validate_sign_up_request_data_keys(request.data.keys()) is True:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    email = request.data['email']
    name = request.data['name']
    password = request.data['password']
    role = request.data['role']

    if role.upper() == 'ADMIN':
        is_admin = Admin.objects.first()

        if is_admin is None:
            serializer = AdminSerializer(data={'is_registered_admin': False})
            serializer.is_valid()
            serializer.save()

        if is_admin.is_registered_admin is True:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            is_admin.is_registered_admin = True
            is_admin.save()

    try:
        helper.create_user(email, name, password, role)
        return Response(status=status.HTTP_201_CREATED)
    except:
        is_admin.is_registered_admin = False
        is_admin.save()
        return Response(status=status.HTTP_400_BAD_REQUEST)


def validate_sign_up_request_data_keys(request_data):
    keys = ['email', 'name', 'password', 'role']

    if len(request_data) > 4:
        return True

    for key in keys:
        if key not in request_data:
            return True
