from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from auth0authorization.decorators import permission_scope
from tables.models import Table
from tables.serializers import TableSerializer


# This endpoint is for homework 8
@api_view(['GET'])
@permission_scope(['Admin'])
def list_tables(request):
    tables = [{"number": 1, "capacity": 2, "created_at": "2021-02-02 12:20:20", "updated_at": "2021-02-02 12:20:20",
               "created_by": 1, "updated_by": 1},
              {"number": 2, "capacity": 4, "created_at": "2021-02-02 12:20:20", "updated_at": "2021-02-02 12:20:20",
               "created_by": 1, "updated_by": 1},
              {"number": 3, "capacity": 10, "created_at": "2021-02-02 12:20:20", "updated_at": "2021-02-02 12:20:20",
               "created_by": 1, "updated_by": 1},
              {"number": 4, "capacity": 5, "created_at": "2021-02-02 12:20:20", "updated_at": "2021-02-02 12:20:20",
               "created_by": 1, "updated_by": 1},
              {"number": 5, "capacity": 6, "created_at": "2021-02-02 12:20:20", "updated_at": "2021-02-02 12:20:20",
               "created_by": 1, "updated_by": 1}]
    return Response(tables)


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
