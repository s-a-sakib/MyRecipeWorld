from rest_framework import serializers
from .models import Receipe
class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Receipe
        fields=['id','user','receipe_name','receipe_discription']
