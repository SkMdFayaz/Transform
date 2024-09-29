from rest_framework import serializers
from .models import DataTemplate, FieldMapping
from attribute_library.models import Field
from rest_framework.exceptions import ValidationError 

class FieldMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldMapping
        fields = ['source_field', 'destination_field']

class DataTemplateSerializer(serializers.ModelSerializer):
    mappings = FieldMappingSerializer(many=True)

    class Meta:
        model = DataTemplate
        fields = ['id', 'name', 'mappings']

    def create(self, validated_data):
        mappings_data = validated_data.pop('mappings')
        template = DataTemplate.objects.create(**validated_data)
        for mapping_data in mappings_data:
            FieldMapping.objects.create(template=template, **mapping_data)
        return template

    def update(self, instance, validated_data):
        print(validated_data)
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
