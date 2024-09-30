from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Field
from .serializers import FieldSerializer

class FieldListCreateAPIView(APIView):
    """
    APIView for listing all fields and creating a new field.

    Methods:
        - GET: Retrieve a list of all fields in the database.
        - POST: Create a new field in the database.

    Returns:
        - 200 OK: On successful retrieval of the list of fields.
        - 201 Created: On successful creation of a new field.
        - 400 Bad Request: If there is an error or invalid data.
    """
    
    def get(self, request):
        """
        Retrieve all fields from the database.

        Purpose:
            This method fetches all Field objects from the database and returns them as a list.

        Returns:
            - 200 OK: A JSON response with the list of all fields.
            - 400 Bad Request: A JSON response with an error message if something goes wrong.

        Example Response:
            [
                {
                    "id": 1,
                    "name": "Candidate",
                    "visible_name": "Candidate Name",
                    "data_type": "String"
                }
            ]
        """
        try:
            fields = Field.objects.all()
            serializer = FieldSerializer(fields, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"data": str(e), "message": "Something Went Wrong"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        """
        Create a new field in the database.

        Purpose:
            This method takes data from the request to create a new Field object in the database.

        Request Body:
            - name (str): The name of the field.
            - visible_name (str): The human-readable name of the field.
            - data_type (str): The data type of the field (e.g., String, Integer, etc.).

        Returns:
            - 201 Created: A JSON response with the details of the newly created field.
            - 400 Bad Request: A JSON response with an error message if the input data is invalid or something goes wrong.

        Example Request Body:
            {
                "name": "Candidate",
                "visible_name": "Candidate Name",
                "data_type": "String"
            }


        Example Response:
            {
                "id": 3,
                "name": "Candidate",
                "visible_name": "Candidate Name",
                "data_type": "String"
            }
        """
        try:
            serializer = FieldSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"data": str(e), "message": "Something Went Wrong"},
                status=status.HTTP_400_BAD_REQUEST
            )

class FieldRetrieveUpdateAPIView(APIView):
    """
    APIView for retrieving and updating a specific field.

    Methods:
        - GET: Retrieve details of a specific field by its primary key (pk).
        - PUT: Update a specific field by its primary key (pk).

    Returns:
        - 200 OK: On successful retrieval or update.
        - 404 Not Found: If the field with the specified pk does not exist.
        - 400 Bad Request: If there is an error or invalid data during update.
    """

    def get(self, request, pk):
        """
        Retrieve details of a specific field by its primary key (pk).

        Purpose:
            This method fetches the details of a specific Field object from the database using the primary key.

        Parameters:
            - pk (int): The primary key of the field to retrieve.

        Returns:
            - 200 OK: A JSON response with the details of the specified field.
            - 404 Not Found: A JSON response if the field with the specified pk does not exist.

        Example Response:
            {
                "id": 1,
                "name": "Candidate",
                "visible_name": "Candidate Name",
                "data_type": "String"
            }
        """
        try:
            field = Field.objects.get(pk=pk)
        except Field.DoesNotExist:
            return Response({"data": None, "message": "Field not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = FieldSerializer(field)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a specific field in the database.

        Purpose:
            This method takes new data from the request and updates the details of a Field object
            in the database based on its primary key.

        Parameters:
            - pk (int): The primary key of the field to update.

        Request Body:
            - name (str): The updated name of the field.
            - visible_name (str): The updated visible name of the field.
            - data_type (str): The updated data type of the field.

        Returns:
            - 200 OK: A JSON response with the updated details of the field.
            - 404 Not Found: A JSON response if the field with the specified pk does not exist.
            - 400 Bad Request: A JSON response with an error message if the input data is invalid.

        Example Request Body:
            {
               "name": "status",
                "visible_name": "Status",
                "data_type": "String"
            }

        Example Response:
            {
                "id": 4,
                "name": "status",
                "visible_name": "Status",
                "data_type": "String"
            }
        """
        try:
            field = Field.objects.get(pk=pk)
        except Field.DoesNotExist:
            return Response({"data": None, "message": "Field not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = FieldSerializer(field, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
