from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from .models import Title , Service , Testimonial, Portfolio, Video


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password']
        extra_kwargs = {
            'password' : {'write_only' : True}
        }
    def create(self, validated_data):
        raw_username = validated_data['username']
        email = validated_data['email']
        # Sanitize username: remove spaces to comply with Django User model validator
        clean_username = raw_username.replace(' ', '')
        if not clean_username:
            clean_username = email.split('@')[0]
            
        # Ensure unique username
        base_username = clean_username
        counter = 1
        while User.objects.filter(username=clean_username).exists():
            clean_username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create_user(
            username = clean_username,
            email= email,
            password=validated_data['password']
        )
        user.first_name = raw_username
        user.save()
        return user

from .models import Meeting


class MeetingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting
        fields = '__all__'
        read_only_fields = ['user']
        
from .models import Product

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
        
class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = '__all__'
        
class CartItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source='product.name',
        read_only=True
    )

    class Meta:
        model = CartItem
        fields = '__all__'
        


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'quote', 'name', 'position', 'metric']

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class WebsiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteSettings
        fields = '__all__'