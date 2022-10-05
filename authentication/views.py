# users/views.py
from authentication.models import Booking
from authentication.serializers import UserSerializer, EmptySerializer, LogoutSerializer, BookingSerializer
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = EmptySerializer

    serializer_classes = {
        'logout': LogoutSerializer,
        'profile': UserSerializer,
        'register': UserSerializer,
    }

    @action(methods=['POST', ], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = user = User.objects.create_user(**serializer.validated_data)
        if user is None:
            data = {'message': 'User not created!'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=['POST', ], detail=False, permission_classes=[IsAuthenticated, ])
    def logout(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            token = RefreshToken(serializer.validated_data['refresh'])
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET', ], detail=False, permission_classes=[IsAuthenticated, ])
    def profile(self, request):
        user_profile = User.objects.get(email=request.user.email)
        serializer = self.get_serializer(user_profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['GET', ], detail=False)
    def tutors(self, request, *args, **kwargs):
        queryset = User.objects.exclude(user_type='learner')
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, ]

    def list(self, request, *args, **kwargs):
        if request.user.user_type == 'learner':
            queryset = Booking.objects.filter(learner=request.user)
            serializer = BookingSerializer(queryset, many=True)
            return Response(serializer.data)
        elif request.user.user_type == 'instructor':
            queryset = Booking.objects.filter(instructor=request.user)
            serializer = BookingSerializer(queryset, many=True)
            return Response(serializer.data)