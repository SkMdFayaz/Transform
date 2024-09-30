from rest_framework import serializers
from .models import DataTemplate, FieldMapping
from attribute_library.models import Field
from rest_framework.exceptions import ValidationError 

class FieldMappingSerializer(serializers.ModelSerializer):
    """
    This serializer handles the serialization and deserialization of FieldMapping objects.
    FieldMapping represents the connection between a source field and a destination field.
    """
    class Meta:
        model = FieldMapping
        fields = ['source_field', 'destination_field']


class DataTemplateSerializer(serializers.ModelSerializer):
    """
    This serializer handles the serialization and deserialization of DataTemplate objects.
    A DataTemplate contains a name and multiple field mappings, which tell us how to map fields
    from one structure to another.
    """
    mappings = FieldMappingSerializer(many=True)

    class Meta:
        model = DataTemplate
        fields = ['id', 'name', 'mappings']

    def create(self, validated_data):
        """
        Create a new DataTemplate instance along with its field mappings.

        Arguments:
        - validated_data: This contains the data that has been validated before saving.

        Steps:
        1. We extract the 'mappings' from the validated data, which includes how fields should be mapped.
        2. A new DataTemplate is created using the remaining validated data.
        3. We loop through each mapping (source field -> destination field) and create FieldMapping objects for each.
        4. Finally, we return the created template with its mappings.

        Returns:
        - The created DataTemplate object.
        """
        mappings_data = validated_data.pop('mappings')
        template = DataTemplate.objects.create(**validated_data)
        for mapping_data in mappings_data:
            FieldMapping.objects.create(template=template, **mapping_data)
        return template

    def update(self, instance, validated_data):
        """
        Update an existing DataTemplate along with its field mappings.

        Arguments:
        - instance: The existing DataTemplate object to be updated.
        - validated_data: This contains the new validated data for updating the DataTemplate.

        Steps:
        1. We extract the 'mappings' if they are provided in the validated data.
        2. The DataTemplate's 'name' is updated (if provided).
        3. If 'mappings' are provided:
           a. We go through each mapping and update the source and destination fields.
           b. For each mapping, we first check if the fields (source and destination) exist in the database.
           c. We then update the existing field mappings of the template or raise an error if no existing mapping is found.
        4. If any field does not exist or other issues arise, we raise a validation error.

        Returns:
        - The updated DataTemplate object.
        """
        mappings_data = validated_data.pop('mappings', None)

        # Update the DataTemplate instance fields
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        if mappings_data:
            for mapping_data in mappings_data:
                new_source_field_id = mapping_data.get('source_field').id
                new_destination_field_id = mapping_data.get('destination_field').id

                print(f"Updating to Source Field ID: {new_source_field_id}, Destination Field ID: {new_destination_field_id}", flush=True)

                try:
                    # Check if the new source and destination fields exist
                    new_source_field = Field.objects.get(id=new_source_field_id)
                    new_destination_field = Field.objects.get(id=new_destination_field_id)

                    # Fetch the current mapping based on the template and the current source field from the DB
                    existing_mapping = FieldMapping.objects.filter(template=instance).first()

                    if existing_mapping:
                        # Log the current fields before updating
                        print(f"Current Source Field: {existing_mapping.source_field.id}, Current Destination Field: {existing_mapping.destination_field.id}", flush=True)

                        # Update the existing mapping with new fields
                        existing_mapping.source_field = new_source_field
                        existing_mapping.destination_field = new_destination_field
                        existing_mapping.save()

                        print(f"Updated mapping: Source Field updated to {new_source_field_id}, Destination Field updated to {new_destination_field_id}", flush=True)
                    else:
                        raise ValidationError({
                            'detail': f"No existing mapping found for template ID {instance.id}."
                        })

                except Field.DoesNotExist:
                    # Raise an error if the new source or destination field doesn't exist
                    raise ValidationError({
                        'detail': f"Field with ID {new_source_field_id} or {new_destination_field_id} does not exist."
                    })

                except Exception as e:
                    # Handle any unexpected exceptions
                    raise ValidationError({
                        'detail': f"An unexpected error occurred: {str(e)}"
                    })

        return instance
