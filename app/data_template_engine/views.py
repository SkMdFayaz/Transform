from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import DataTemplate, FieldMapping, Field
from .serializers import DataTemplateSerializer, FieldMappingSerializer
from rest_framework.exceptions import ValidationError 

class DataTemplateListCreateAPIView(APIView):
    """
    API View to handle the retrieval and creation of Data Templates in the Data Template Engine.

    *** GET Method ***
    Retrieve a list of all Data Templates stored in the database.

    *** POST Method ***
    Create a new Data Template along with its field mappings.
    """
    def get(self, request):
        """
        HTTP Method: GET

        Purpose:
            Retrieve all Data Templates from the database.
            Fetches a list of all templates in the DataTemplate table of the database.

        Returns:
            - 200 OK: A JSON response containing the list of data templates and their associated mappings.
            - 400 Bad Request: A JSON response with an error message if something goes wrong.

        Return Data on Success:
                [
                    {
                        "id": 1,
                        "name": "Template 1",
                        "mappings": [
                            {
                                "id": 1,
                                "source_field": {
                                    "id": 1,
                                    "name": "Field 1",
                                    "visible_name": "Field One",
                                    "data_type": "String"
                                },
                                "destination_field": {
                                    "id": 2,
                                    "name": "Field 2",
                                    "visible_name": "Field Two",
                                    "data_type": "String"
                                }
                            }
                        ]
                    }
                ]
        """
        try:
            templates = DataTemplate.objects.all()
            serializer = DataTemplateSerializer(templates, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response ({"data": str(e),
                             "message": "Something Went Wrong",
                             },
                            status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """

        """
        try:
            serializer = DataTemplateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response ({"data": str(e),
                             "message": "Something Went Wrong",
                             },
                            status=status.HTTP_400_BAD_REQUEST)

class DataTemplateRetrieveUpdateAPIView(APIView):
    """
    API View to retrieve or update a Data Template instance.
    
    GET Method:
        - Retrieves a Data Template by its primary key.
        - Returns 404 if not found.
    
    PUT Method:
        - Updates the Data Template and its associated mappings.
        - Raises an error if a mapping does not exist instead of creating new mappings.
    """
    def get(self, request, pk):
        """
        Http Method: GET
        
        Purpose:
            To retrieve the DataTemplate instance by its primary key.
            
        Returns:
            - 200 OK: JSON response containing the template data if it exists.
            - 404 Not Found: If the DataTemplate is not found.
        """
        try:
            template = DataTemplate.objects.get(pk=pk)
        except DataTemplate.DoesNotExist:
            return Response({"data":None,"message": "Template not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = DataTemplateSerializer(template)
        return Response(serializer.data)

    
    def put(self, request, pk):
        """
        Http Method: PUT
        
        Purpose:
            To update the DataTemplate and its mappings.
            
        Behavior:
            - If any mapping does not exist, returns an error without creating new mappings.
            
        Returns:
            - 200 OK: If the DataTemplate and mappings are successfully updated.
            - 400 Bad Request: If the provided data is invalid or any mapping does not exist.
            - 404 Not Found: If the DataTemplate is not found.
        """
        try:
            template = DataTemplate.objects.get(pk=pk)
        except DataTemplate.DoesNotExist:
            return Response({"data": None, "message": "Template not found"}, status=status.HTTP_404_NOT_FOUND)

        # Pass the data to the serializer for validation and update
        serializer = DataTemplateSerializer(template, data=request.data)
        
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValidationError as e:  # Catch ValidationError from the serializer
                return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)