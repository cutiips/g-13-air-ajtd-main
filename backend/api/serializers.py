from django.contrib.auth.models import User, Group
from .models import Picture, Rating, RenterRating, Review, Room, Address, Reservation, Favorite, Notification
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'first_name', 'last_name']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ['id', 'room', 'image']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'user', 'room', 'country', 'city', 'streetname', 'postal_code']

class ReservationSerializer(serializers.ModelSerializer):
    userId = serializers.ReadOnlyField(source='user.id')
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    is_past_due = serializers.ReadOnlyField()

    def validate_user(self, value):
        if value == '':
            return None
        return value

    class Meta:
        model = Reservation
        fields = ['id', 'userId', 'user', 'room', 'start_date', 'end_date', 'guests', 'status', 'is_reviewed', 'is_rated', 'is_past_due', 'is_renter_rated']

class RoomSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=True, read_only=True)
    pictures = PictureSerializer(many=True, read_only=True)
    reservation = ReservationSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'owner', 'room_name', 'description', 'price', 'address', 'pictures', 'reservation', 'pets_allowed', 'smoking_allowed', 'has_elevator']

class VerifyEmailSerializer(serializers.Serializer):
    key = serializers.CharField(write_only=True)

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'room']

class ReviewerPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class ReviewSerializer(serializers.ModelSerializer):
    reviewer_id = serializers.ReadOnlyField(source='reviewer.id')
    reviewer = serializers.ReadOnlyField(source='reviewer.username')
    room = RoomSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['room', 'reviewer', 'comment', 'reviewer_id']

class RatingPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class RatingSerializer(serializers.ModelSerializer):
    reviewer = serializers.ReadOnlyField(source='reviewer.username')

    class Meta:
        model = Rating
        fields = ['room', 'reviewer', 'score']

class RenterRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RenterRating
        fields = ['id', 'owner', 'renter', 'score', 'comment', 'created_at', 'reservation']
        read_only_fields = ['id', 'created_at', 'owner']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'user', 'message', 'created_at', 'is_read']
