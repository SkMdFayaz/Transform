from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/fields/', include('attribute_library.urls')),  # URLs for Attribute Library (Fields)
    path('api/templates/', include('data_template_engine.urls')),  # URLs for Data Template Engine
    path('api/', include('transformer.urls')),  # URLs for the Transformer API
]
