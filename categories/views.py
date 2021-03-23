from django.utils.decorators import method_decorator
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from auth0authorization.decorators import permission_scope
from categories.serializers import CategorySerializer
from categories.models import Category
from products.models import Product


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @method_decorator(permission_scope(['Admin']))
    def list(self, request, **kwargs):
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    @method_decorator(permission_scope(['Admin']))
    def retrieve(self, request, pk=None, **kwargs):
        category = get_object_or_404(self.queryset, pk=pk)
        serializer = CategorySerializer(category)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(permission_scope(['Admin']))
    def create(self, request, **kwargs):
        data = request.data

        serializer = CategorySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @method_decorator(permission_scope(['Admin']))
    def update(self, request, pk=None, **kwargs):
        category = get_object_or_404(self.queryset, pk=pk)

        serializer = CategorySerializer(instance=category, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)

    @method_decorator(permission_scope(['Admin']))
    def partial_update(self, request, pk=None, **kwargs):
        category = get_object_or_404(self.queryset, pk=pk)

        serializer = CategorySerializer(instance=category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)

    @method_decorator(permission_scope(['Admin']))
    def destroy(self, request, pk=None, **kwargs):
        category = get_object_or_404(self.queryset, pk=pk)
        products = Product.objects.filter(category=pk).first()

        if products is not None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        category.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
