from django.db.models import fields
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"
        
class QtyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QtyType
        fields = "__all__"
        
class OffersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offers
        fields = "__all__"
        # fields = ('oid','name','image','status','category_id','user_id','last_date','created_at')
        
