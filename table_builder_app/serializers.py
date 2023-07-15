from rest_framework import serializers
from .models import Table, TableRow


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = "__all__"


class TableRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableRow
        fields = "__all__"
