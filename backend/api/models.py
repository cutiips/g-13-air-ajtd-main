from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

def validate_end_date(value):
    if value < timezone.now().date():
        raise ValidationError("An error occurred while validating your reservation date")

class Picture(models.Model):
    room = models.ForeignKey('Room', related_name='pictures', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='room_pictures')

class Room(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pets_allowed = models.BooleanField(default=False)
    smoking_allowed = models.BooleanField(default=False)
    has_elevator = models.BooleanField(default=False)


class Address(models.Model):
    user = models.ForeignKey(User, related_name='address', null=True, blank=True, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='address', null=True, blank=True, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    streetname = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

class Reservation(models.Model):
    user = models.ForeignKey(User, related_name='reservation', on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Room, related_name='reservation', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(validators=[validate_end_date])
    guests = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, default='pending')
    is_rated = models.BooleanField(default=False)
    is_reviewed = models.BooleanField(default=False)
    is_renter_rated = models.BooleanField(default=False)

    def is_past_due(self):
        return self.end_date < timezone.now().date()

class Favorite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='reviews', on_delete=models.CASCADE, null=True, blank=True)
    reviewer = models.ForeignKey(User, related_name='given_reviews', on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)

    class Meta:
        unique_together = ['user', 'room', 'reservation']

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='ratings', on_delete=models.CASCADE, null=True, blank=True)
    reviewer = models.ForeignKey(User, related_name='given_ratings', on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='ratings', null=True, blank=True)

    class Meta:
        unique_together = ['user', 'room', 'reservation']

class RenterRating(models.Model):
    owner = models.ForeignKey(User, related_name='given_renter_ratings', on_delete=models.CASCADE)
    renter = models.ForeignKey(User, related_name='received_renter_ratings', on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, related_name='renter_ratings', on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('owner', 'renter', 'reservation')

class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message
