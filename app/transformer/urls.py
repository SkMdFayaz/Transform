from django.urls import path
from .views import TransformAPIView

urlpatterns = [
    # API to transform input data using a specific data template
    path('transform/<int:template_id>/', TransformAPIView.as_view(), name='transform'),
]
