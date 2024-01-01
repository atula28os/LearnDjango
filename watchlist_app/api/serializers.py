from rest_framework import serializers
from watchlist_app.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        
    def validate(self, data):
        if data['name'] == data['description']:
            raise serializers.ValidationError("Name & Descriptions can't be same")
        return data


    def validate_name(self, value):
        """Field Level Validation (Name Field)"""
        if len(value) < 5: 
            raise serializers.ValidationError('Name should be greater than 5 characters')
        else:
            return value
        

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField()
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         response = Movie.objects.create(**validated_data)
#         return response
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Name & Descriptions can't be same")
#         return data


#     def validate_name(self, value):
#         """Field Level Validation (Name Field)"""
#         if len(value) < 5: 
#             raise serializers.ValidationError('Name should be greater than 5 characters')
#         else:
#             return value
