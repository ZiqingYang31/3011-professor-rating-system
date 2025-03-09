from rest_framework import serializers
from .models import Professor, Module, ModuleInstance, Rating

class ProfessorSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField() 

    def get_average_rating(self, obj):
        ratings = Rating.objects.filter(professor=obj)
        if ratings.exists():
            return round(sum(r.rating for r in ratings) / ratings.count())
        return "No Ratings"

    class Meta:
        model = Professor
        fields = ['id', 'name', 'average_rating'] 

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['code', 'name']

class ModuleInstanceSerializer(serializers.ModelSerializer):
    module = ModuleSerializer()
    professors = ProfessorSerializer(many=True)

    class Meta:
        model = ModuleInstance
        fields = ["id", "module", "year", "semester", "professors"] 

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  

    class Meta:
        model = Rating
        fields = ['id', 'professor', 'module_instance', 'rating', 'user']
        read_only_fields = ['user'] 


