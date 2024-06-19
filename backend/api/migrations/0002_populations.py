from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import migrations, transaction
from django.utils import timezone
import os
import shutil
from datetime import date, timedelta
from django.contrib.auth.models import User
from backend.api.models import Room, Reservation, Review, Rating, RenterRating
import random

def create_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    users = [
        {'username': 'test2_user', 'email': 'user@test2.com', 'password': 'password'},
        {'username': 'student1', 'email': 'user1@student.com', 'password': 'password'},
        {'username': 'student2', 'email': 'user2@student.com', 'password': 'password'},
        {'username': 'owner1', 'email': 'user3@owner.com', 'password': 'password'},
        {'username': 'owner2', 'email': 'user4@owner.com', 'password': 'password'},
        {'username': 'student3', 'email': 'user3@student.com', 'password': 'password'},
        {'username': 'owner3', 'email': 'user5@owner.com', 'password': 'password'},
    ]

    for user in users:
        User.objects.create_superuser(username=user['username'], email=user['email'], password=user['password'], last_login=timezone.now())

def create_rooms_with_addresses_and_pictures(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Address = apps.get_model('api', 'Address')
    Room = apps.get_model('api', 'Room')
    Picture = apps.get_model('api', 'Picture')

    example_user = User.objects.get(username='test2_user')
    owner1 = User.objects.get(username='owner1')
    owner2 = User.objects.get(username='owner2')

    addresses = [
        {'country': 'Switzerland', 'city': 'Neuchâtel', 'streetname': 'Rue de l’Hôpital 11', 'postal_code': '2000'},
        {'country': 'Switzerland', 'city': 'Neuchâtel', 'streetname': 'Faubourg de l’Hôpital 6', 'postal_code': '2000'},
        {'country': 'Switzerland', 'city': 'Sion', 'streetname': 'Avenue de la Gare 19', 'postal_code': '1950'},
        {'country': 'Switzerland', 'city': 'Sion', 'streetname': 'Rue du Rhône 9', 'postal_code': '1950'},
        {'country': 'Switzerland', 'city': 'Geneva', 'streetname': 'Rue du Mont-Blanc 18', 'postal_code': '1201'},
        {'country': 'Switzerland', 'city': 'Geneva', 'streetname': 'Rue de Lausanne 15', 'postal_code': '1201'},
        {'country': 'Switzerland', 'city': 'Lausanne', 'streetname': 'Place de la Gare 2', 'postal_code': '1003'},
        {'country': 'Switzerland', 'city': 'Bern', 'streetname': 'Kramgasse 49', 'postal_code': '3011'},
        {'country': 'Switzerland', 'city': 'Zurich', 'streetname': 'Bahnhofstrasse 22', 'postal_code': '8001'},
        {'country': 'Switzerland', 'city': 'Lucerne', 'streetname': 'Hertensteinstrasse 34', 'postal_code': '6004'},
        {'country': 'Switzerland', 'city': 'Basel', 'streetname': 'Steinenvorstadt 53', 'postal_code': '4051'},
    ]

    room_names = [
        'Cozy Loft', 'Sunny Studio', 'Modern Apartment', 'Quiet Retreat', 'Urban Oasis',
        'Countryside Escape', 'Lakeview Room', 'Mountain Hideaway', 'Historic Home', 'Charming Flat',
        'Spacious Suite', 'Luxury Penthouse'
    ]

    descriptions = [
        'A cozy loft with modern amenities and a great view.',
        'A sunny studio perfect for a short stay in the city.',
        'A modern apartment with all the comforts of home.',
        'A quiet retreat away from the hustle and bustle.',
        'An urban oasis in the heart of the city.',
        'A peaceful countryside escape with beautiful surroundings.',
        'A room with a stunning lake view.',
        'A hideaway in the mountains, perfect for relaxation.',
        'A historic home with plenty of character.',
        'A charming flat in a convenient location.',
        'A spacious suite with luxurious furnishings.',
        'A penthouse with panoramic city views.'
    ]

    image_directory = r'media/room_pictures'
    all_images = [f'Room{num}.jpg' for num in range(1, 49)]

    owners = [example_user, owner1, owner2]

    for i in range(60):
        with transaction.atomic():
            address = addresses[i % len(addresses)]
            room_name = room_names[i % len(room_names)]
            description = descriptions[i % len(descriptions)]
            owner = owners[i % len(owners)]
            room = Room.objects.create(
                owner=owner,
                room_name=room_name,
                description=description,
                price=random.randint(100, 200),
                pets_allowed=True if i % 2 == 0 else False,
                smoking_allowed=True if i % 2 == 1 else False,
                has_elevator=True if i % 2 == 0 else False,
            )

            Address.objects.create(
                room=room,
                country=address['country'],
                city=address['city'],
                streetname=address['streetname'],
                postal_code=address['postal_code']
            )

            room_folder = os.path.join(image_directory, f'Room_{i+1}')
            os.makedirs(room_folder, exist_ok=True)

            selected_images = random.sample(all_images, 3)
            for j, image in enumerate(selected_images):
                src_image_path = os.path.join(image_directory, image)
                dest_image_path = os.path.join(room_folder, image)

                shutil.copy(src_image_path, dest_image_path)

                relative_image_path = f'room_pictures/Room_{i+1}/{image}'
                Picture.objects.create(
                    room=room,
                    image=relative_image_path
                )

def create_old_reservations(apps, schema_editor):
    Room = apps.get_model('api', 'Room')
    Reservation = apps.get_model('api', 'Reservation')
    User = apps.get_model('auth', 'User')
    Review = apps.get_model('api', 'Review')
    Rating = apps.get_model('api', 'Rating')

    room_ids = list(Room.objects.values_list('id', flat=True))
    users = User.objects.filter(username__in=['student1', 'student2', 'student3'])
    start_date = date(2024, 5, 1)
    end_date = date(2024, 5, 3)
    guests = [1, 2, 3, 4]
    status = ['accepted', 'declined', 'completed', 'cancelled']

    for i, room_id in enumerate(room_ids):
        room = Room.objects.get(pk=room_id)
        user = users[i % len(users)]
        reservation = Reservation.objects.create(
            room=room,
            user=user,
            start_date=start_date + timedelta(days=i),
            end_date=end_date + timedelta(days=i),
            guests=guests[i % len(guests)],
            status=status[i % len(status)]
        )

        Review.objects.create(
            reviewer=user,
            room=room,
            reservation=reservation,
            user=user,
            comment=f'Great stay at {room.room_name}. Highly recommend!'
        )

        Rating.objects.create(
            reviewer=user,
            room=room,
            reservation=reservation,
            user=user,
            score=random.randint(3, 5)
        )

def create_reservations(apps, schema_editor):
    Room = apps.get_model('api', 'Room')
    Reservation = apps.get_model('api', 'Reservation')
    User = apps.get_model('auth', 'User')
    Review = apps.get_model('api', 'Review')
    Rating = apps.get_model('api', 'Rating')
    RenterRating = apps.get_model('api', 'RenterRating')

    room_ids = list(Room.objects.values_list('id', flat=True))
    users = User.objects.filter(username__in=['student1', 'student2', 'student3'])
    start_date = date.today()
    end_date = start_date + timedelta(days=7)
    guests = [1, 2, 3]
    status = ['pending', 'confirmed']

    for i, room_id in enumerate(room_ids):
        room = Room.objects.get(pk=room_id)
        user = users[i % len(users)]
        reservation = Reservation.objects.create(
            room=room,
            user=user,
            start_date=start_date + timedelta(days=i),
            end_date=end_date + timedelta(days=i),
            guests=guests[i % len(guests)],
            status=status[i % len(status)]
        )

        Review.objects.create(
            reviewer=user,
            room=room,
            reservation=reservation,
            user=user,
            comment=f'Lovely stay at {room.room_name}. Would book again!'
        )

        Rating.objects.create(
            reviewer=user,
            room=room,
            reservation=reservation,
            user=user,
            score=random.randint(3, 5)
        )

        RenterRating.objects.create(
            owner=room.owner,
            renter=user,
            reservation=reservation,
            score=random.randint(3, 5),
            comment=f'Good renter. Left the place clean and tidy.'
        )

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
        migrations.RunPython(create_rooms_with_addresses_and_pictures),
        migrations.RunPython(create_old_reservations),
        migrations.RunPython(create_reservations),
    ]
