from django.forms import ValidationError
from django.utils import timezone
import os
from django.contrib.auth.models import User, Group
from django.contrib.auth import login
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from .models import Picture, Rating, RenterRating, Review, Room, Address, Reservation, Favorite, Notification
from .serializers import (
    RatingSerializer, RenterRatingSerializer, ReviewSerializer, UserSerializer, GroupSerializer,
    PictureSerializer, RoomSerializer, AddressSerializer, ReservationSerializer,
    VerifyEmailSerializer, FavoriteSerializer, NotificationSerializer
)
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.db.models import Avg
from django.views import generic

index_view = never_cache(TemplateView.as_view(template_name='index.html'))

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj == request.user

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all().order_by('-date_joined')
        return User.objects.filter(id=self.request.user.id)

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]

class PictureViewSet(viewsets.ModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        data = request.data
        room_id = data.get('room')
        images = data.getlist('image')

        if not room_id or not images:
            return Response({'error': 'room and images are required fields.'}, status=status.HTTP_400_BAD_REQUEST)

        room = Room.objects.get(id=room_id)
        for image in images:
            Picture.objects.create(room=room, image=image)

        return Response({'message': 'Pictures uploaded successfully'}, status=status.HTTP_201_CREATED)

class RoomViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @action(detail=True, methods=['get'])
    def pictures(self, request, pk=None):
        room = self.get_object()
        pictures = room.pictures.all()
        serializer = PictureSerializer(pictures, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def address(self, request, pk=None):
        room = self.get_object()
        address = room.address
        serializer = AddressSerializer(address)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reservations(self, request, pk=None):
        room = self.get_object()
        reservations = Reservation.objects.filter(room=room)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = Room.objects.all()
        user_id = self.request.query_params.get('user', None)
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        return queryset

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def rooms_by_owner(self, request, owner_id=None):
        if owner_id is not None:
            queryset = Room.objects.filter(owner_id=owner_id)
            serializer = RoomSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "No owner_id provided."}, status=400)

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class CustomVerifyEmailView(APIView):
    permission_classes = (AllowAny,)

    def get_object(self, key):
        confirmation = EmailConfirmationHMAC.from_key(key)
        if confirmation and not confirmation.email_address.verified:
            return confirmation

        confirmation = EmailConfirmation.objects.filter(key=key).first()
        if confirmation and not confirmation.email_address.verified:
            return confirmation

        return None

    def get(self, request, *args, **kwargs):
        key = kwargs.get('key')
        if not key:
            return Response({'detail': _('Key not provided.')}, status=status.HTTP_400_BAD_REQUEST)

        serializer = VerifyEmailSerializer(data={'key': key})
        serializer.is_valid(raise_exception=True)

        confirmation = self.get_object(serializer.validated_data['key'])
        if confirmation is None:
            return redirect('/#/profile?already_confirmed=true')

        try:
            confirmation.confirm(self.request)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        user = confirmation.email_address.user
        if hasattr(user, 'backend'):
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

        return redirect('/#/profile?confirmed=true')

def password_reset_redirect(request, uidb64, token):
    return redirect(f'/#/new-password/{uidb64}/{token}')

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    @action(detail=False, methods=['get'])
    def past_by_owner(self, request, owner_id=None):
        owner_id = owner_id if owner_id else request.user.id
        rooms = Room.objects.filter(owner_id=owner_id)
        reservations = Reservation.objects.filter(room__in=rooms, end_date__lt=timezone.now().date())
        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def perform_create(self, serializer):
        reservation_data = self.request.data
        user_id = reservation_data.get('user')

        user = None
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"error": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            reservation = serializer.save(user=user)
            owner = reservation.room.owner
            Notification.objects.create(
                user=owner,
                title=_("Reservation Created"),
                message=f"A new reservation has been made for your room: {reservation.room.room_name}",
                created_at=timezone.now(),
                is_read=False
            )
        except Exception as e:
            print(f"Error creating reservation: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    @transaction.atomic
    def perform_update(self, serializer):
        instance = serializer.save()

        if 'status' in serializer.validated_data:
            new_status = serializer.validated_data['status']
            if new_status == 'accepted':
                Notification.objects.create(
                    user=instance.user,
                    title="Reservation Accepted",
                    message=f"Your reservation for the room {instance.room.room_name} has been accepted.",
                    created_at=timezone.now(),
                    is_read=False
                )
            elif new_status == 'rejected':
                Notification.objects.create(
                    user=instance.user,
                    title="Reservation Rejected",
                    message=f"Unfortunately, your reservation for the room {instance.room.room_name} has been rejected.",
                    created_at=timezone.now(),
                    is_read=False
                )

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def mark_as_renter_rated(self, request, pk=None):
        reservation = self.get_object()
        reservation.is_renter_rated = True
        reservation.save()
        return Response({'status': 'reservation marked as renter rated'})

    @action(detail=False, methods=['get'])
    def past_reservations_by_owner(self, request):
        owner_id = request.user.id
        rooms = Room.objects.filter(owner_id=owner_id)
        reservations = Reservation.objects.filter(room__in=rooms, end_date__lt=timezone.now().date())
        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def mark_as_reviewed(self, request, pk=None):
        reservation = self.get_object()
        reservation.is_reviewed = True
        reservation.save()
        return Response({'status': 'reservation marked as reviewed'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def mark_as_rated(self, request, pk=None):
        reservation = self.get_object()
        reservation.is_rated = True
        reservation.save()
        return Response({'status': 'reservation marked as rated'})

    @action(detail=False, methods=['get'])
    def current(self, request):
        reservations = Reservation.objects.filter(user=request.user, end_date__gte=timezone.now().date())
        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def past(self, request):
        reservations = Reservation.objects.filter(user=request.user, end_date__lt=timezone.now().date())
        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data)

    @api_view(['GET'])
    def by_user(request, user_id):
        if user_id is not None:
            reservations = Reservation.objects.filter(user_id=user_id)
            serializer = ReservationSerializer(reservations, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "user_id parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

def create_folder(request):
    if request.method == 'POST':
        folder_path = request.POST.get('folderPath')
        try:
            os.makedirs(folder_path, exist_ok=True)
            return JsonResponse({'message': 'Folder created successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class FavoriteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, pk=None):
        favorite = self.get_object()
        self.perform_destroy(favorite)
        return Response(status=status.HTTP_204_NO_CONTENT)

class PublicReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        room_id = self.request.query_params.get('room', None)
        if room_id:
            return Review.objects.filter(room_id=room_id)
        return Review.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.request.user and self.request.user.is_staff:
            self.permission_classes = [IsAdminOrReadOnly]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def perform_create(self, serializer):
        room_id = self.request.data.get('room')
        reservation_id = self.request.data.get('reservation')
        if not room_id:
            raise ValidationError('Room ID is required')

        if Review.objects.filter(room_id=room_id, reviewer=self.request.user, reservation_id=reservation_id).exists():
            raise ValidationError('You have already reviewed this reservation.')

        serializer.save(reviewer=self.request.user, user=self.request.user, room_id=room_id, reservation_id=reservation_id)

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        room_id = self.request.query_params.get('room', None)
        if room_id:
            return Rating.objects.filter(room_id=room_id)
        return Rating.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.request.user and self.request.user.is_staff:
            self.permission_classes = [IsAdminOrReadOnly]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def perform_create(self, serializer):
        room_id = self.request.data.get('room')
        reservation_id = self.request.data.get('reservation')
        if not room_id:
            raise ValidationError('Room ID is required')

        if Rating.objects.filter(room_id=room_id, reviewer=self.request.user, reservation_id=reservation_id).exists():
            raise ValidationError('You have already rated this reservation.')

        serializer.save(reviewer=self.request.user, user=self.request.user, room_id=room_id, reservation_id=reservation_id)

class RenterRatingViewSet(viewsets.ModelViewSet):
    queryset = RenterRating.objects.all()
    serializer_class = RenterRatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return RenterRating.objects.all()
        return RenterRating.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        owner = self.request.user
        renter_id = self.request.data.get('renter')
        reservation_id = self.request.data.get('reservation')

        try:
            renter = User.objects.get(id=renter_id)
        except User.DoesNotExist:
            raise ValidationError('Renter does not exist.')

        try:
            reservation = Reservation.objects.get(id=reservation_id)
        except Reservation.DoesNotExist:
            raise ValidationError('Reservation does not exist.')

        if reservation.room.owner != owner:
            raise ValidationError('You can only rate renters who have reserved your rooms.')

        if reservation.end_date >= timezone.now().date():
            raise ValidationError('You can only rate renters after the reservation has ended.')

        if RenterRating.objects.filter(owner=owner, renter=renter, reservation=reservation).exists():
            raise ValidationError('You have already rated this renter for this reservation.')

        serializer.save(owner=owner, renter=renter, reservation=reservation)

class RenterProfileView(generic.DetailView):
    model = User
    template_name = 'renter_profile.html'
    context_object_name = 'renter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        renter = self.get_object()
        average_rating = RenterRating.objects.filter(renter=renter).aggregate(Avg('score'))['score__avg']
        context['average_rating'] = average_rating
        return context

class PublicProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, renter_id):
        try:
            renter = User.objects.get(id=renter_id)
            average_rating = RenterRating.objects.filter(renter=renter).aggregate(Avg('score'))['score__avg']
            response_data = {
                'id': renter.id,
                'username': renter.username,
                'email': renter.email,
                'first_name': renter.first_name,
                'last_name': renter.last_name,
                'average_rating': average_rating
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'notification marked as read'})

    @action(detail=False, methods=['get'])
    def recent(self, request):
        recent_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
        serializer = NotificationSerializer(recent_notifications, many=True)
        return Response(serializer.data)
