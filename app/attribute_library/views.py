
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Field
from .serializers import FieldSerializer

class FieldListCreateAPIView(APIView):
    def get(self, request):
        """

        """
        try:
            fields = Field.objects.all()
            serializer = FieldSerializer(fields, many=True)
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
            serializer = FieldSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response ({"data": str(e),
                             "message": "Something Went Wrong",
                             },
                            status=status.HTTP_400_BAD_REQUEST)

class FieldRetrieveUpdateAPIView(APIView):
    def get(self, request, pk):
        """

        """
        try:
            field = Field.objects.get(pk=pk)
        except Field.DoesNotExist:
            return Response({"data":None,"message": "Field not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = FieldSerializer(field)
        return Response(serializer.data)

    def put(self, request, pk):
        """

        """
        try:
            field = Field.objects.get(pk=pk)
        except Field.DoesNotExist:
            return Response({"data":None,"message": "Field not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = FieldSerializer(field, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
