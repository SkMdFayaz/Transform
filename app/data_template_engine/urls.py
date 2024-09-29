from django.urls import path
from .views import DataTemplateListCreateAPIView, DataTemplateRetrieveUpdateAPIView

urlpatterns = [
    # API to create a data template and list all templates
    path('', DataTemplateListCreateAPIView.as_view(), name='template-list-create'),  
    
    # API to retrieve, update a specific data template
    path('<int:pk>/', DataTemplateRetrieveUpdateAPIView.as_view(), name='template-detail'),  
]
