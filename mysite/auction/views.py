from rest_framework import generics, status
from .serializers import *
from .paginations import TwoObject
from .permissions import *
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileListAPIView(generics.ListAPIView):
    serializer_class = UserProfileListSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class UserProfileEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileEditSerializer
    permission_classes = [UserEdit]


class BrandListAPIView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandListSerializer


class BrandDetailAPIView(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandDetailSerializer


class ModelListAPIView(generics.ListAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelsSerializer


class ModelDetailAPIView(generics.RetrieveAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelDetailSerializer


class CarCreateAPIView(generics.CreateAPIView):
    serializer_class = CarSerializer
    permission_classes = [CheckUserSeller]


class CarEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [CheckCarEdit, CheckUserSeller]


class CarOwnListAPIView(generics.ListAPIView):
    serializer_class = CarListSerializer
    permission_classes = [CheckUserSeller]

    def get_queryset(self):
        return Car.objects.filter(seller=self.request.user)


class CarListAPIView(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarListSerializer
    pagination_class = TwoObject


class CarDetailAPIView(generics.RetrieveAPIView):
    queryset = Car.objects.all()
    serializer_class = CarDetailSerializer


class AuctionCreateAPIView(generics.CreateAPIView):
    serializer_class = AuctionSerializer
    permission_classes = [CheckUserSeller]


class AuctionOwnListAPIView(generics.ListAPIView):
    serializer_class = AuctionListSerializer
    permission_classes = [CheckUserSeller]

    def get_queryset(self):
        return Auction.objects.filter(car__seller=self.request.user)


class AuctionEditAPIView(generics.RetrieveUpdateAPIView):
    queryset = Auction.objects.all()
    permission_classes = [CheckUserSeller, CheckAuctionEdit]

    def get_serializer_class(self):
        if self.request.method in ['PUT']:
            return AuctionEditSerializer
        return AuctionSerializer


class AuctionListAPIView(generics.ListAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionListSerializer


class BidCreateAPIView(generics.CreateAPIView):
    serializer_class = BidSerializer
    permission_classes = [CheckUserBuyer]


class BidListAPIView(generics.ListAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidListSerializer


class FeedbackCreateAPIView(generics.CreateAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [CheckUserBuyer]


class FeedbackListAPIView(generics.ListAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackListSerializer
    permission_classes = [CheckUserBuyer]
