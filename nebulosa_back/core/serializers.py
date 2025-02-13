from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    """
    Base serializer class for all serializers in the project.
    """
    def flatten_data(self, data: dict, prefix: str) -> dict:
        """
        Flattens the representation of the 'prefix' field by merging its data in the same position in the main dictionary.
        """

        position = list(data.keys()).index(prefix)
        prefix_data = data.pop(prefix, {})

        result = {}
        for i, key in enumerate(data.keys()):
            if i == position:
                for prefix_key, prefix_value in prefix_data.items():
                    result[prefix_key] = prefix_value
            if key != prefix:
                result[key] = data[key]
        return result

    def unflatten_data(self, flattened_data: dict, related_keys: list, prefix_key: str) -> dict:
        """
        Unflattens the representation of the 'prefix_key' field by creating a dictionary with the prefix_key as key.
        """

        nested_data = {}
        unflattened_data = {}
        for key, value in flattened_data.items():
            if key in related_keys:
                nested_data[key] = value
            else:
                unflattened_data[key] = value
        unflattened_data[prefix_key] = nested_data
        return unflattened_data