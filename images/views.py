from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from auth0authorization.decorators import permission_scope
from images.models import Image
from images.serializers import ImageSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser)

    @method_decorator(permission_scope(['Admin']))
    def list(self, request, **kwargs):
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    @method_decorator(permission_scope(['Admin']))
    def create(self, request, **kwargs):
        serializer = ImageSerializer(data=request.data)

        image = request.data['image']

        if validate_size_of_image(image):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if validate_format_of_image(image):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @method_decorator(permission_scope(['Admin']))
    def retrieve(self, request, pk=None, **kwargs):
        image = get_object_or_404(self.queryset, pk=pk)
        serializer = ImageSerializer(image)

        return Response(serializer.data)

    @method_decorator(permission_scope(['Admin']))
    def update(self, request, pk=None, **kwargs):
        image = get_object_or_404(self.queryset, pk=pk)

        serializer = ImageSerializer(instance=image, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)

    @method_decorator(permission_scope(['Admin']))
    def partial_update(self, request, pk=None, **kwargs):
        image = get_object_or_404(self.queryset, pk=pk)

        serializer = ImageSerializer(instance=image, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)

    @method_decorator(permission_scope(['Admin']))
    def destroy(self, request, pk=None, **kwargs):
        product = get_object_or_404(self.queryset, pk=pk)
        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


def validate_size_of_image(image):
    max_file_size = 5242880
    if image.size > max_file_size:
        return True


def validate_format_of_image(image):
    image_format = str(image)[-3:]
    if image_format.upper() == 'JPG' or image_format.upper() == 'PNG':
        return False
    return True
