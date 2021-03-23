from django.utils.decorators import method_decorator
from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from auth0authorization.decorators import permission_scope
from auth0authorization.utils import get_decoded_token, get_user_id, get_user_role
from orders.models import Order, OrdersProducts
from orders.serializers import OrderSerializer, OrdersProductsSerializer, IsDeletedSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.filter(is_deleted=0)
    serializer_class = OrderSerializer
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)
    ordering_fields = ('status', 'table__id', 'user__id')
    search_fields = ('status', 'table__id', 'user__id')

    @method_decorator(permission_scope(['Admin', 'Bartender', 'Waiter']))
    def list(self, request, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    @method_decorator(permission_scope(['Admin', 'Bartender', 'Waiter']))
    def retrieve(self, request, pk=None, **kwargs):
        order = get_object_or_404(self.queryset, pk=pk)
        serializer = OrderSerializer(order)

        return Response(serializer.data)

    @method_decorator(permission_scope(['Admin', 'Bartender', 'Waiter']))
    def create(self, request, **kwargs):
        data = request.data
        table_key = data.get('table')
        queryset = Order.objects.filter(table=table_key, status='In progress').first()
        if queryset is not None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = OrderSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @method_decorator(permission_scope(['Admin', 'Bartender', 'Waiter']))
    def update(self, request, pk=None, **kwargs):
        order = get_active_order(pk)

        if order is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderSerializer(instance=order, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)

    @method_decorator(permission_scope(['Admin', 'Bartender', 'Waiter']))
    def partial_update(self, request, pk=None, **kwargs):
        order = get_active_order(pk)

        if order is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderSerializer(instance=order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)

    @method_decorator(permission_scope(['Admin']))
    def destroy(self, request, pk=None, **kwargs):
        order = Order.objects.filter(pk=pk)
        order.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class OrdersProductsViewSet(viewsets.ModelViewSet):
    queryset = OrdersProducts.objects.filter(order__is_deleted=0)
    serializer_class = OrdersProductsSerializer

    @method_decorator(permission_scope(['Admin', 'Bartender', 'Waiter']))
    def list(self, request, **kwargs):
        print(request.data)
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)

            return self.get_paginated_response(serializer.data)

    @method_decorator(permission_scope(['Admin', 'Bartender', 'Waiter']))
    def retrieve(self, request, pk=None, **kwargs):
        order_product = get_object_or_404(self.queryset, pk=pk)
        serializer = OrdersProductsSerializer(order_product)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(permission_scope(['Admin', 'Waiter']))
    def create(self, request, **kwargs):
        data = request.data

        serializer = OrdersProductsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @method_decorator(permission_scope(['Admin', 'Waiter']))
    def update(self, request, pk=None, **kwargs):
        order_product = get_object_or_404(self.queryset, pk=pk)

        serializer = OrdersProductsSerializer(instance=order_product, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)

    @method_decorator(permission_scope(['Admin', 'Waiter']))
    def partial_update(self, request, pk=None, **kwargs):
        order_product = get_object_or_404(self.queryset, pk=pk)

        serializer = OrdersProductsSerializer(instance=order_product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)

    @method_decorator(permission_scope(['Admin', 'Waiter']))
    def destroy(self, request, pk=None, **kwargs):
        order_product = get_object_or_404(self.queryset, pk=pk)

        token = get_decoded_token(request)
        request_user_id = get_user_id(decoded_token=token)

        if request_user_id != order_product.order.user.username and get_user_role(token) == 'Waiter':
            return Response(status=status.HTTP_400_BAD_REQUEST)

        order_product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_scope(['Admin', 'Bartender', 'Waiter'])
def get_active_orders_by_table_id(request, pk):
    orders = Order.objects.filter(table=pk, status='In progress')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_scope(['Admin', 'Bartender'])
def soft_delete(request, pk):
    queryset = Order.objects.all()

    if validate_soft_delete(request.data):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    order = get_object_or_404(queryset, pk=pk)
    serializer = IsDeletedSerializer(instance=order, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(status=status.HTTP_200_OK)


def get_active_order(pk):
    order = Order.objects.filter(pk=pk, status='In progress').first()
    return order


def validate_soft_delete(request_data):
    if 'is_deleted' not in request_data or len(request_data) > 1:
        return True
