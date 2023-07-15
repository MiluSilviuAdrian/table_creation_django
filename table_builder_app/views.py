from django.shortcuts import render

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Table, TableRow
from .serializers import TableSerializer, TableRowSerializer


@api_view(['POST'])
def create_table(request):
    serializer = TableSerializer(data=request.data)
    if serializer.is_valid():
        table = serializer.save()
        return Response(TableSerializer(table).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_table(request, pk):
    table = get_object_or_404(Table, pk=pk)
    serializer = TableSerializer(table, data=request.data)
    if serializer.is_valid():
        table = serializer.save()
        return Response(TableSerializer(table).data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_table_row(request, pk):
    table = get_object_or_404(Table, pk=pk)
    serializer = TableRowSerializer(data=request.data)
    if serializer.is_valid():
        table_row = serializer.save(table=table)
        return Response(TableRowSerializer(table_row).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_table_rows(request, pk):
    table = get_object_or_404(Table, pk=pk)
    table_rows = table.rows.all()
    serializer = TableRowSerializer(table_rows, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def index(request):
    return render(request, 'index.html')
