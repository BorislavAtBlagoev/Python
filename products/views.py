from django.utils.decorators import method_decorator
from rest_framework import viewsets, filters, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from auth0authorization.decorators import permission_scope
from products.models import Product
from products.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    ordering_fields = ('name', 'category__name')
    search_fields = ('name', 'category__id')

    @method_decorator(permission_scope(['Admin']))
    def list(self, request, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    @method_decorator(permission_scope(['Admin']))
    def create(self, request, **kwargs):
        data = request.data

        serializer = ProductSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @method_decorator(permission_scope(['Admin']))
    def retrieve(self, request, pk=None, **kwargs):
        product = get_object_or_404(self.queryset, pk=pk)
        serializer = ProductSerializer(product)

        return Response(serializer.data)

    @method_decorator(permission_scope(['Admin']))
    def update(self, request, pk=None, **kwargs):
        product = get_object_or_404(self.queryset, pk=pk)

        serializer = ProductSerializer(instance=product, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)

    @method_decorator(permission_scope(['Admin']))
    def partial_update(self, request, pk=None, **kwargs):
        product = get_object_or_404(self.queryset, pk=pk)

        serializer = ProductSerializer(instance=product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)

    @method_decorator(permission_scope(['Admin']))
    def destroy(self, request, pk=None, **kwargs):
        product = get_object_or_404(self.queryset, pk=pk)
        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
