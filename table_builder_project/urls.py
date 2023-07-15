from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('table_builder_app.urls', namespace='table_builder_app')),
]
