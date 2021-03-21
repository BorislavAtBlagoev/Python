from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from auth0authorization.decorators import permission_scope
from tables.models import Table
from tables.serializers import TableSerializer


class TableViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    @method_decorator(permission_scope(['Admin']))
    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    @method_decorator(permission_scope(['Admin']))
    def retrieve(self, request, pk=None, **kwargs):
        table = get_object_or_404(self.queryset, pk=pk)
        serializer = TableSerializer(table)

        return Response(serializer.data)
