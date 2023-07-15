from django.db import models
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Table, TableRow
from django.core.management import call_command


class TableBuilderAppTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('migrate', interactive=False)

    def setUp(self):
        self.client = APIClient()

    def test_create_table(self):
        url = reverse('table_builder_app:create-table')
        data = {
            "fields": [
                {"name": "name", "type": "string"},
                {"name": "age", "type": "number"},
                {"name": "is_active", "type": "boolean"}
            ]
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Table.objects.count(), 1)
        self.assertEqual(len(response.data['fields']), 3)

    def test_update_table(self):
        table = Table.objects.create(fields=[
            {"name": "name", "type": "string"},
            {"name": "age", "type": "number"},
            {"name": "is_active", "type": "boolean"}
        ])
        url = reverse('table_builder_app:update-table', args=[table.id])
        data = {
            "fields": [
                {"name": "name", "type": "string"},
                {"name": "age", "type": "number"},
                {"name": "is_active", "type": "boolean"},
                {"name": "email", "type": "string"}
            ]
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Table.objects.count(), 1)
        self.assertEqual(len(response.data['fields']), 4)

    def test_create_table_row(self):
        table = Table.objects.create(fields=[{"name": "name", "type": "string"}])
        url = reverse('table_builder_app:create-table-row', kwargs={'pk': table.pk})
        data = {"table": table.pk, "data": {"name": "John Doe"}}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TableRow.objects.count(), 1)
        self.assertEqual(TableRow.objects.first().table, table)
        self.assertEqual(TableRow.objects.first().data, data["data"])

    def test_create_dynamic_table(self):
        url = reverse('table_builder_app:create-table')
        data = {
            "fields": [
                {"name": "name", "type": "string"},
                {"name": "age", "type": "number"},
                {"name": "is_active", "type": "boolean"}
            ]
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Table.objects.count(), 1)

        # Verify the dynamically created model
        dynamic_table = Table.objects.first()
        dynamic_model = dynamic_table.create_model()

        # Verify the model fields
        field_names = [field.name for field in dynamic_model._meta.get_fields()]
        self.assertIn("name", field_names)
        self.assertIn("age", field_names)
        self.assertIn("is_active", field_names)

        # Verify the model string representation
        dynamic_instance = dynamic_model(name="John Doe", age=30, is_active=True)
        self.assertEqual(str(dynamic_instance), str(dynamic_instance.id))
