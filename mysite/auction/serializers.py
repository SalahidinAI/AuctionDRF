from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number', 'status', 'date_registered')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'role']


class UserProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'password',
                  'email', 'phone_number', 'role']


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']


class BrandNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['brand_name']


class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'brand_name']


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['image']


class ModelNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ['model_name']


class ModelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ['id', 'model_name']


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


class CarListSerializer(serializers.ModelSerializer):
    brand = BrandNameSerializer()
    model = ModelNameSerializer()
    seller = UserNameSerializer()
    created_date = serializers.DateTimeField(format='%d %B %Y %H:%M')

    class Meta:
        model = Car
        fields = ['id', 'car_image', 'brand', 'model', 'year',
                  'seller', 'created_date']


class CarDetailSerializer(serializers.ModelSerializer):
    brand = BrandNameSerializer()
    model = ModelNameSerializer()
    seller = UserNameSerializer()
    created_date = serializers.DateTimeField(format='%d %B %Y %H:%M')

    class Meta:
        model = Car
        fields = ['id', 'car_image', 'brand', 'model', 'description', 'mileage',
                  'year', 'fuel_type', 'transmission', 'seller', 'created_date']


class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = '__all__'


class AuctionEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ['status']


class AuctionListSerializer(serializers.ModelSerializer):
    car = CarListSerializer()
    start_time = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))
    end_time = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))

    class Meta:
        model = Auction
        fields = ['id', 'car', 'start_price', 'min_price', 'start_time', 'end_time',
                  'status']


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'


class BidListSerializer(serializers.ModelSerializer):
    buyer = UserProfileListSerializer()

    class Meta:
        model = Bid
        fields = ['id', 'buyer', 'auction', 'amount', 'created_at']


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class FeedbackListSerializer(serializers.ModelSerializer):
    buyer = UserProfileListSerializer()
    seller = UserProfileListSerializer()

    class Meta:
        model = Feedback
        fields = ['id', 'buyer', 'seller', 'star', 'comment']


class BrandDetailSerializer(serializers.ModelSerializer):
    brand_cars = CarListSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = ['brand_name', 'brand_cars']


class ModelDetailSerializer(serializers.ModelSerializer):
    model_cars = CarListSerializer(many=True, read_only=True)

    class Meta:
        model = Model
        fields = ['model_name', 'model_cars']
