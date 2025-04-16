from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('user/', UserProfileListAPIView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserProfileEditAPIView.as_view(), name='user_edit'),

    path('brand/', BrandListAPIView.as_view(), name='brand_list'),
    path('brand/<int:pk>/', BrandDetailAPIView.as_view(), name='brand_detail'),

    path('model/', ModelListAPIView.as_view(), name='model_list'),
    path('model/<int:pk>/', ModelDetailAPIView.as_view(), name='model_detail'),

    path('car/', CarListAPIView.as_view(), name='car_list'),
    path('car/<int:pk>/', CarDetailAPIView.as_view(), name='car_detail'),
    # check model and brand when u create
    path('car_list/', CarOwnListAPIView.as_view(), name='car_own_create'),
    path('car_list/create/', CarCreateAPIView.as_view(), name='car_create'),
    path('car_list/<int:pk>/', CarEditAPIView.as_view(), name='car_edit'),

    path('auction/', AuctionListAPIView.as_view(), name='auction_list'),
    path('auction_list/', AuctionOwnListAPIView.as_view(), name='auction_own_create'),
    path('auction_list/create/', AuctionCreateAPIView.as_view(), name='auction_create'),
    path('auction_list/<int:pk>/', AuctionEditAPIView.as_view(), name='auction_own_edit'),

    path('bid/', BidListAPIView.as_view(), name='bid_list'),
    path('bid/create/', BidCreateAPIView.as_view(), name='bid_create'),

    path('feedback/', FeedbackListAPIView.as_view(), name='feedback_list'),
    path('feedback/create/', FeedbackCreateAPIView.as_view(), name='feedback_create'),
]
