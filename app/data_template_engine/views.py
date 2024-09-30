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
        HTTP Method: POST

        Purpose:
            Create a new Data Template in the database.
            Accepts data for creating a new template, including its associated field mappings.
            Each mapping specifies how fields from the source structure should be transformed to the destination structure.

        Input:
            A JSON request body with the following structure:
            {
                "name": "Template Name",
                "mappings": [
                    {
                        "source_field": 1,  # The ID of the source field
                        "destination_field": 2  # The ID of the destination field
                    }
                ]
            }

        Returns:
            - 201 Created: A JSON response containing the newly created data template and its associated mappings.
            - 400 Bad Request: A JSON response with an error message if the input data is invalid or if something goes wrong.

        Example Request Body:
        {
            "name": "Candidate Mapping",
            "mappings": [
                {
                    "source_field": 1,
                    "destination_field": 2
                }
                
            ]
        }

        Example Response on Success (201 Created):
        {
            "id": 2,
            "name": "Candidate Template 2",
            "mappings": [
                {
                    "source_field": 1,
                    "destination_field": 1
                }
            ]
        }

        Example Response on Error (400 Bad Request):
        {
            "data": "Field with ID 999 does not exist",
            "message": "Something Went Wrong"
        }
        """
        try:
            # Attempt to deserialize the input data and create a new DataTemplate
            serializer = DataTemplateSerializer(data=request.data)
            
            # Check if the provided data is valid according to the serializer
            if serializer.is_valid():
                # If valid, save the new template and return the data
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            # If validation fails, return the errors with a 400 status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            # Handle any unexpected exceptions that might occur
            return Response(
                {
                    "data": str(e),
                    "message": "Something Went Wrong",
                },
                status=status.HTTP_400_BAD_REQUEST
            )


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
            - 400 Bad Request: If the provided data is invalid or any mapping does not exist.

        Example Response:
            {
                "id": 1,
                "name": "Candidate Template",
                "mappings": [
                    {
                        "source_field": 1,
                        "destination_field": 1
                    }
                ]
            }
        """
        try:
            template = DataTemplate.objects.get(pk=pk)
        except DataTemplate.DoesNotExist:
            return Response({"data":None,"message": "Template not found"}, status=status.HTTP_400_BAD_REQUEST)
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

        Request Body:
            {
                "name": "Candidate Template 37",
                "mappings": [
                    {
                        "source_field": 2,
                        "destination_field": 2
                    }
                ]
            }
            
        """
        try:
            template = DataTemplate.objects.get(pk=pk)
        except DataTemplate.DoesNotExist:
            return Response({"data": None, "message": "Template not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Pass the data to the serializer for validation and update
        serializer = DataTemplateSerializer(template, data=request.data)
        
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValidationError as e:  # Catch ValidationError from the serializer
                return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)