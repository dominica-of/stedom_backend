from django.urls import path
from rest_framework import routers

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authentication.views import AuthViewSet, BookingViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('', AuthViewSet, basename='auth')
router.register('bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = urlpatterns + router.urls
