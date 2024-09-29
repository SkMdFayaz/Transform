class Transformer:
    def transform(self, input_data, data_template):
        output = {}
        for mapping in data_template.mappings.all():
            source_field_name = mapping.source_field.name
            dest_field_name = mapping.destination_field.visible_name
            output[dest_field_name] = input_data.get(source_field_name, None)
        return output
