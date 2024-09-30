from attribute_library.models import Field

class Transformer:
    def transform(self, input_data, template):
        """
        Main method to transform input_data based on a template.
        
        Purpose:
            This method reads the input data and transforms it based on the mappings defined in the template.
            For each mapping, it takes a value from a source field in the input data and places it in the destination
            field in the output data.

        Parameters:
            - input_data (dict): The original data that needs to be transformed. 
                                 Example: {'candidate': {'first_name': 'John', 'last_name': 'Doe'}}
            - template (DataTemplate): The template that defines the mapping rules between source fields and destination fields.
        
        Returns:
            - output_data (dict): The transformed data after applying the mappings from the template.
                                  Example: {'Candidate Details': {'First Name': 'John'}}
        """
        output_data = {}  # Initialize an empty dictionary for storing the transformed output
        
        print("Starting transformation...")
        print(f"Input Data: {input_data}")  # Debugging statement to show input data
        print(f"Template Mappings: {template.mappings.all()}")  # Debugging to show mappings in the template
        
        # Loop through each mapping in the template to transform the data
        for mapping in template.mappings.all():
            # Fetch the source and destination fields using their IDs and get the field names
            source_field = Field.objects.get(pk=mapping.source_field.id).name  # Example: 'candidate.first_name'
            destination_field = Field.objects.get(pk=mapping.destination_field.id).visible_name  # Example: 'Candidate Details.First Name'
            
            print(f"Processing mapping: {source_field} -> {destination_field}")  # Debugging statement to show current mapping
            
            # Extract value from input_data using the source field path (e.g., 'candidate.first_name')
            value = self._get_value_by_path(input_data, source_field.split('.'))
            print(f"Extracted value: {value} from {source_field}")  # Debugging to show the extracted value
            
            # If a value was successfully extracted, set it in the output data at the destination path
            if value is not None:
                print(f"Setting value at {destination_field}")
                self._set_value_by_path(output_data, destination_field.split('.'), value)
                print(f"Set value: {value} at {destination_field}")
            else:
                print(f"Value for {source_field} not found in input data.")  # Debugging if value is not found
        
        print(f"Transformed Output: {output_data}")  # Debugging to show the final transformed output
        return output_data

    def _get_value_by_path(self, data, path):
        """
        Helper method to extract a value from the input data by navigating a specific path.

        Purpose:
            This method takes a path (e.g., ['candidate', 'first_name']) and follows it step by step in the input data
            to retrieve the final value.

        Parameters:
            - data (dict or Django model): The input data or a Django model instance that needs to be traversed.
            - path (list): A list of strings representing the path to the value in the data. 
                           Example: ['candidate', 'first_name']
        
        Returns:
            - value: The extracted value at the specified path, or None if the path doesn't exist in the data.
        """
        for part in path:
            # Check if data is a dictionary (common for JSON-like structures)
            if isinstance(data, dict):
                data = data.get(part)  # Move to the next level in the dictionary
            # Check if data is a Django model instance (e.g., if part is a field in a model)
            elif hasattr(data, part):
                data = getattr(data, part)  # Get the attribute value from the model
                # Handle related fields like ForeignKey or ManyToMany
                if isinstance(data, models.Manager) or isinstance(data, models.QuerySet):
                    data = data.all()  # For many-to-many relationships
                elif isinstance(data, models.Model):
                    data = data  # For foreign key relationships
            else:
                data = None  # If the part does not exist, set data to None and break
            
            # If at any point data becomes None, stop the loop
            if data is None:
                break
        return data

    def _set_value_by_path(self, data, path, value):
        """
        Helper method to set a value in the output data by navigating a specific path.

        Purpose:
            This method takes a path (e.g., ['Candidate Details', 'First Name']) and places the value at the 
            appropriate location in the output data structure.

        Parameters:
            - data (dict): The output data where the value will be inserted.
            - path (list): A list of strings representing the path where the value should be set. 
                           Example: ['Candidate Details', 'First Name']
            - value: The value to be set at the specified path.
        
        Returns:
            None
        """
        print(f"Setting value {value} at path {path}")  # Debugging to show the value and path being processed
        
        # If we are at the last element of the path, set the value
        if len(path) == 1:
            data[path[0]] = value
        else:
            # If the current part of the path doesn't exist, create a new dictionary
            if path[0] not in data:
                data[path[0]] = {}
            # Recursively set the value in the nested dictionary structure
            self._set_value_by_path(data[path[0]], path[1:], value)
