from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator


RoleChoices = (
    ('seller', 'seller'),
    ('buyer', 'buyer'),
)


FuelTypeChoices = (
    ('benzine', 'benzine'),
    ('electro', 'electro'),
    ('gas', 'gas'),
)

TransmissionChoices = (
    ('auto', 'auto'),
    ('manually', 'manually'),
)


AuctionChoices = (
    ('Waiting', 'Waiting'),
    ('Active', 'Active'),
    ('Finished', 'Finished'),
    ('Canceled', 'Canceled'),
)


class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(null=True, blank=True)
    role = models.CharField(choices=RoleChoices, max_length=16)

    def __str__(self):
        return f'{self.username} - {self.role}'


class Brand(models.Model):
    brand_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return f'{self.brand_name}'


class Model(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_models')
    model_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return f'{self.brand} {self.model_name}'


class Car(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_cars')
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='model_cars')
    description = models.TextField(null=True, blank=True)
    mileage = models.PositiveSmallIntegerField()
    year = models.PositiveIntegerField(validators=[
        MinValueValidator(1900), MaxValueValidator(datetime.now().year)
    ])
    fuel_type = models.CharField(choices=FuelTypeChoices, max_length=16)
    transmission = models.CharField(choices=TransmissionChoices, max_length=16)
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='seller_cars')
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.model} {self.seller}'


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='car_image')
    image = models.ImageField(upload_to='car_images/')

    def __str__(self):
        return f'{self.car}'


class Auction(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_price = models.PositiveIntegerField(default=0)
    min_price = models.PositiveIntegerField()
    # constraint end_time cant be earlier start_time
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(choices=AuctionChoices, default='Waiting', max_length=16)

    def __str__(self):
        return f'{self.car} {self.status}'


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='auction_bids')
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='buyer_bids')
    amount = models.PositiveIntegerField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.auction} {self.buyer}'


class Feedback(models.Model):
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='seller_feedback')
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='buyer_feedback')
    # def clean
    star = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1), MaxValueValidator(5)
    ])
    comment = models.TextField()

    def __str__(self):
        return f'{self.buyer} > {self.seller}'
