from django.urls import path
from .views import FieldListCreateAPIView, FieldRetrieveUpdateAPIView

urlpatterns = [
    # API to create a field and list all fields
    path('', FieldListCreateAPIView.as_view(), name='field-list-create'),  
    
    # API to retrieve, update a specific field
    path('<int:pk>/', FieldRetrieveUpdateAPIView.as_view(), name='field-detail'),  
]
