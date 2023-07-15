from django.urls import path
from . import views

app_name = 'table_builder_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/table/', views.create_table, name='create-table'),
    path('api/table/<int:pk>/', views.update_table, name='update-table'),
    path('api/table/<int:pk>/row/', views.create_table_row, name='create-table-row'),
    path('api/table/<int:pk>/rows/', views.get_table_rows, name='get-table-rows'),
]