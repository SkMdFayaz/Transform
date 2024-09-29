
from rest_framework.response import Response
from rest_framework.views import APIView
from data_template_engine.models import DataTemplate  # Assuming this is your model
from .transformer import Transformer  # Your Transformer class

class TransformAPIView(APIView):
    """

    """

    def post(self, request, template_id):
        try:
            # Access the template_id from the URL
            template_id = self.kwargs.get('template_id')
            
            # Get the input data from the request body
            input_data = request.data

            # Fetch the data template using template_id
            try:
                data_template = DataTemplate.objects.get(id=template_id)
            except DataTemplate.DoesNotExist:
                return Response({"error": "Data template not found"}, status=404)

            # Initialize the transformer and transform the data
            transformer = Transformer()
            output_data = transformer.transform(input_data, data_template)

            # Return the transformed data
            return Response(output_data)
        except Exception as e:
            return Response ({"data": str(e),
                             "message": "Something Went Wrong",
                             },
                            status=status.HTTP_400_BAD_REQUEST)
