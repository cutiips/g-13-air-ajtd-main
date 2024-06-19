from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings
from .api.views import (RatingViewSet, ReviewViewSet, index_view, UserViewSet, GroupViewSet, PictureViewSet,
                        RoomViewSet, AddressViewSet, ReservationViewSet, CustomVerifyEmailView,
                        password_reset_redirect, create_folder, FavoriteViewSet, NotificationViewSet, RenterRatingViewSet, PublicProfileView)

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('groups', GroupViewSet)
router.register('pictures', PictureViewSet)
router.register('rooms', RoomViewSet)
router.register('address', AddressViewSet)
router.register('reservations', ReservationViewSet)
router.register('favorites', FavoriteViewSet)
router.register('reviews', ReviewViewSet)
router.register('ratings', RatingViewSet)
router.register('notifications', NotificationViewSet)
router.register(r'renter-ratings', RenterRatingViewSet, basename='renter-rating')

urlpatterns = [
    re_path(r'^api/dj-rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$', CustomVerifyEmailView.as_view(), name='account_confirm_email'),
    path('', index_view, name='index'),
    path('api/', include(router.urls)),
    path('api/create-folder/', create_folder, name='create-folder'),
    path('api/explorer/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/dj-rest-auth/', include('dj_rest_auth.urls')),
    path('api/dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/dj-rest-auth/reset/confirm/', password_reset_redirect, name='password_reset_confirm'),
    path('api/dj-rest-auth/reset/<uidb64>/<token>/', password_reset_redirect, name='password_reset_confirm'),
    path('api/rooms/ownerid/<int:owner_id>/', RoomViewSet.as_view({'get': 'rooms_by_owner'}), name='rooms_by_owner'),
    path('api/reservation/userid/<int:user_id>/', ReservationViewSet.by_user),
    path('api/reservations/current/', ReservationViewSet.as_view({'get': 'current'}), name='current-reservations'),
    path('api/reservations/past/', ReservationViewSet.as_view({'get': 'past'}), name='past-reservations'),
    path('api/reservations/<int:pk>/mark_as_reviewed/', ReservationViewSet.as_view({'post': 'mark_as_reviewed'}), name='mark_as_reviewed'),
    path('api/reservations/<int:pk>/mark_as_rated/', ReservationViewSet.as_view({'post': 'mark_as_rated'}), name='mark_as_rated'),
    path('api/public-profile/<int:renter_id>/', PublicProfileView.as_view(), name='public-profile'),
    path('api/reservations/past_by_owner/', ReservationViewSet.as_view({'get': 'past_reservations_by_owner'}), name='past-reservations-by-owner'),
    path('api/reservations/<int:pk>/mark_as_renter_rated/', ReservationViewSet.as_view({'post': 'mark_as_renter_rated'}), name='mark_as_renter_rated'),
    path('api/reservations/past_by_owner/<int:owner_id>/', ReservationViewSet.as_view({'get': 'past_by_owner'}), name='past-reservations-by-owner'),
    path('api/notifications/recent/', NotificationViewSet.as_view({'get': 'recent'}), name='recent-notifications'),

    path('api/admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
