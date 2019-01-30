from rest_framework import serializers
from . import models

class AccountSerializer(serializers.ModelSerializer):
    #ingredients = IngredientSerializer(many=True, read_only=True)
    class Meta:
        model = models.User
        fields = ('id', 'username', 'pin')

class DweetSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Dweet
		fields = ('content', 'comments')