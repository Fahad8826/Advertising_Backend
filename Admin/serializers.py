from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone', 'email', 'is_active', 'is_staff', 'profile_image', 'logo']


class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone', 'email', 'is_active', 'is_staff', 'profile_image', 'logo']
       

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_staff = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ['username', 'phone', 'email', 'password', 'is_staff', 'profile_image', 'logo']

    def create(self, validated_data):
        is_staff = validated_data.pop('is_staff', False)

        # Extract image fields if provided
        profile_image = validated_data.pop('profile_image', None)
        logo = validated_data.pop('logo', None)

        # Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            phone=validated_data.get('phone'),
            email=validated_data.get('email'),
            password=validated_data['password'],
        )

        # Assign optional fields
        user.is_staff = is_staff
        if profile_image:
            user.profile_image = profile_image
        if logo:
            user.logo = logo

        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()  # Can be username, email, or phone
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        identifier = data.get('identifier')
        password = data.get('password')

        # Allow login via username, email, or phone
        user = None
        if '@' in identifier:  # likely email
            user = User.objects.filter(email=identifier).first()
        elif identifier.isdigit():  # likely phone
            user = User.objects.filter(phone=identifier).first()
        else:  # fallback to username
            user = User.objects.filter(username=identifier).first()

        if user and user.check_password(password):
            if not user.is_active:
                raise serializers.ValidationError("User is inactive")
            data['user'] = user
            return data

        raise serializers.ValidationError("Invalid credentials")

#---------------------------------------------------

from rest_framework import serializers
from .models import Category, SubCategory, ImageUpload

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class ImageUploadSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)

    class Meta:
        model = ImageUpload
        fields = '__all__'
        
