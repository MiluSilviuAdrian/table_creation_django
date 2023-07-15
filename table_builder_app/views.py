from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Table, TableRow
from .serializers import TableSerializer, TableRowSerializer

def get_field_type_from_table(field_type):
    if field_type == "string":
        return str
    elif field_type == "number":
        return int
    elif field_type == "boolean":
        return bool
    else:
        return str

def get_default_value_for_field_type(field_type):
    if field_type == "string":
        return ""
    elif field_type == "number":
        return 0
    elif field_type == "boolean":
        return False
    else:
        return None

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
    data = request.data.get("fields")

    if not data:
        return Response({"error": "No fields provided."}, status=status.HTTP_400_BAD_REQUEST)

    # Clear all existing rows for the table
    table.rows.all().delete()

    # Update the table fields
    table.fields = data
    table.save()

    return Response({"success": "Table updated successfully."}, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_table_row(request, pk):
    table = get_object_or_404(Table, pk=pk)
    data = request.data.get("data")

    # Validate the data against the table fields
    required_fields = {field["name"] for field in table.fields}

    # Check if any extra fields are present in the data
    extra_fields = set(data.keys()) - required_fields
    if extra_fields:
        return Response({"error": f"Extra fields not allowed: {', '.join(extra_fields)}"}, status=status.HTTP_400_BAD_REQUEST)

    # Check if any required fields are missing
    missing_fields = required_fields - set(data.keys())
    if missing_fields:
        return Response({"error": f"Required fields missing: {', '.join(missing_fields)}"}, status=status.HTTP_400_BAD_REQUEST)

    # Validate the data types of the fields
    for field in table.fields:
        field_name = field["name"]
        field_type = field["type"]
        field_value = data[field_name]
        expected_field_type = get_field_type_from_table(field_type)

        # Check if the field value is of the expected field type
        if not isinstance(field_value, expected_field_type):
            return Response({"error": f"Invalid value '{field_value}' for field '{field_name}'. Expected type: {expected_field_type.__name__}."}, status=status.HTTP_400_BAD_REQUEST)

    table_row = TableRow.objects.create(table=table, data=data)
    serializer = TableRowSerializer(table_row)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_table_rows(request, pk):
    table = get_object_or_404(Table, pk=pk)
    table_rows = table.rows.all()
    serializer = TableRowSerializer(table_rows, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

def index(request):
    return render(request, 'index.html')
