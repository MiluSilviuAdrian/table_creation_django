from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Table, TableRow


class TableBuilderAppTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_table(self):
        url = reverse("table_builder_app:create-table")
        data = {
            "fields": [
                {"name": "name", "type": "string"},
                {"name": "age", "type": "number"},
                {"name": "active", "type": "boolean"},
            ]
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Table.objects.count(), 1)
        self.assertEqual(len(Table.objects.get().fields), 3)

    def test_get_table_rows(self):
        table = Table.objects.create(
            fields=[
                {"name": "name", "type": "string"},
                {"name": "age", "type": "number"},
                {"name": "active", "type": "boolean"},
            ]
        )
        TableRow.objects.create(
            table=table, data={"name": "John", "age": 25, "active": True}
        )
        TableRow.objects.create(
            table=table, data={"name": "Jane", "age": 30, "active": False}
        )

        url = reverse("table_builder_app:get-table-rows", args=[table.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_table(self):
        # Prepare the request data
        data = {
            "fields": [
                {"name": "field1", "type": "string"},
                {"name": "field2", "type": "number"},
                {"name": "field3", "type": "boolean"},
            ]
        }

        # Create a table with the initial fields
        table = Table.objects.create(
            fields=[
                {"name": "name", "type": "string"},
                {"name": "age", "type": "number"},
                {"name": "active", "type": "boolean"},
            ]
        )

        # Make a PUT request to update the table
        url = reverse("table_builder_app:update-table", args=[table.pk])
        response = self.client.put(url, data, format="json")

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Retrieve the updated table from the database
        updated_table = Table.objects.get(pk=table.pk)

        # Assert the updated fields
        self.assertEqual(updated_table.fields, data["fields"])

        # Assert that all previous rows are deleted
        self.assertEqual(updated_table.rows.count(), 0)

    def test_create_table_row(self):
        table = Table.objects.create(
            fields=[
                {"name": "name", "type": "string"},
                {"name": "age", "type": "number"},
                {"name": "active", "type": "boolean"},
            ]
        )

        data = {"data": {"name": "John", "age": 25, "active": True}}

        url = reverse("table_builder_app:create-table-row", args=[table.pk])
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TableRow.objects.count(), 1)
        self.assertEqual(TableRow.objects.get().table, table)
        self.assertEqual(TableRow.objects.get().data, data["data"])
