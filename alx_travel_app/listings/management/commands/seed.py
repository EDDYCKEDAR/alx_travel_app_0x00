from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
import random
from datetime import date, timedelta
from listings.models import Listing, Booking, Review


class Command(BaseCommand):
    help = 'Seed the database with sample travel listings, bookings, and reviews'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--listings',
            type=int,
            default=20,
            help='Number of listings to create (default: 20)'
        )
        parser.add_argument(
            '--bookings',
            type=int,
            default=50,
            help='Number of bookings to create (default: 50)'
        )
        parser.add_argument(
            '--reviews',
            type=int,
            default=30,
            help='Number of reviews to create (default: 30)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding'
        )
    
    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Review.objects.all().delete()
            Booking.objects.all().delete()
            Listing.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))
        
        self.create_users()
        self.create_listings(options['listings'])
        self.create_bookings(options['bookings'])
        self.create_reviews(options['reviews'])
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully seeded database with:\n'
            f'- {User.objects.count()} users\n'
            f'- {Listing.objects.count()} listings\n'
            f'- {Booking.objects.count()} bookings\n'
            f'- {Review.objects.count()} reviews'
        ))
    
    def create_users(self):
        """Create sample users"""
        self.stdout.write('Creating users...')
        
        # Sample user data
        users_data = [
            {
                'username': 'alice_host',
                'email': 'alice@example.com',
                'first_name': 'Alice',
                'last_name': 'Johnson',
                'password': 'password123'
            },
            {
                'username': 'bob_traveler',
                'email': 'bob@example.com',
                'first_name': 'Bob',
                'last_name': 'Smith',
                'password': 'password123'
            },
            {
                'username': 'charlie_host',
                'email': 'charlie@example.com',
                'first_name': 'Charlie',
                'last_name': 'Brown',
                'password': 'password123'
            },
            {
                'username': 'diana_guest',
                'email': 'diana@example.com',
                'first_name': 'Diana',
                'last_name': 'Wilson',
                'password': 'password123'
            },
            {
                'username': 'eve_explorer',
                'email': 'eve@example.com',
                'first_name': 'Eve',
                'last_name': 'Davis',
                'password': 'password123'
            },
            {
                'username': 'frank_host',
                'email': 'frank@example.com',
                'first_name': 'Frank',
                'last_name': 'Miller',
                'password': 'password123'
            },
            {
                'username': 'grace_nomad',
                'email': 'grace@example.com',
                'first_name': 'Grace',
                'last_name': 'Taylor',
                'password': 'password123'
            },
            {
                'username': 'henry_backpacker',
                'email': 'henry@example.com',
                'first_name': 'Henry',
                'last_name': 'Anderson',
                'password': 'password123'
            }
        ]
        
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name']
                }
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
        
        self.stdout.write(f'Created {len(users_data)} users.')
    
    def create_listings(self, count):
        """Create sample listings"""
        self.stdout.write(f'Creating {count} listings...')
        
        # Sample listing data
        listings_data = [
            {
                'title': 'Cozy Downtown Apartment',
                'description': 'A beautiful apartment in the heart of the city with modern amenities and stunning views.',
                'location': 'New York, NY',
                'price_per_night': Decimal('120.00'),
                'category': 'apartment',
                'bedrooms': 2,
                'bathrooms': 1,
                'max_guests': 4,
                'amenities': {'wifi': True, 'kitchen': True, 'air_conditioning': True}
            },
            {
                'title': 'Beachfront Villa Paradise',
                'description': 'Luxury villa with direct beach access, perfect for a relaxing getaway.',
                'location': 'Miami, FL',
                'price_per_night': Decimal('350.00'),
                'category': 'villa',
                'bedrooms': 4,
                'bathrooms': 3,
                'max_guests': 8,
                'amenities': {'wifi': True, 'pool': True, 'parking': True, 'kitchen': True}
            },
            {
                'title': 'Mountain Cabin Retreat',
                'description': 'Rustic cabin surrounded by nature, ideal for hiking and outdoor activities.',
                'location': 'Aspen, CO',
                'price_per_night': Decimal('180.00'),
                'category': 'cabin',
                'bedrooms': 3,
                'bathrooms': 2,
                'max_guests': 6,
                'amenities': {'wifi': True, 'parking': True, 'kitchen': True}
            },
            {
                'title': 'Modern Studio Loft',
                'description': 'Stylish studio perfect for solo travelers or couples.',
                'location': 'San Francisco, CA',
                'price_per_night': Decimal('95.00'),
                'category': 'studio',
                'bedrooms': 1,
                'bathrooms': 1,
                'max_guests': 2,
                'amenities': {'wifi': True, 'kitchen': True, 'air_conditioning': True}
            },
            {
                'title': 'Historic Townhouse',
                'description': 'Charming historic home with modern updates in a quiet neighborhood.',
                'location': 'Boston, MA',
                'price_per_night': Decimal('160.00'),
                'category': 'house',
                'bedrooms': 3,
                'bathrooms': 2,
                'max_guests': 6,
                'amenities': {'wifi': True, 'parking': True, 'kitchen': True}
            },
            {
                'title': 'Luxury Penthouse Suite',
                'description': 'High-end penthouse with panoramic city views and premium amenities.',
                'location': 'Chicago, IL',
                'price_per_night': Decimal('275.00'),
                'category': 'apartment',
                'bedrooms': 3,
                'bathrooms': 2,
                'max_guests': 6,
                'amenities': {'wifi': True, 'pool': True, 'air_conditioning': True, 'parking': True}
            },
            {
                'title': 'Seaside Cottage',
                'description': 'Quaint cottage just steps from the beach with ocean views.',
                'location': 'Myrtle Beach, SC',
                'price_per_night': Decimal('140.00'),
                'category': 'house',
                'bedrooms': 2,
                'bathrooms': 1,
                'max_guests': 4,
                'amenities': {'wifi': True, 'kitchen': True, 'parking': True}
            },
            {
                'title': 'Urban Condo with City Views',
                'description': 'Modern condo in the financial district with great city views.',
                'location': 'Seattle, WA',
                'price_per_night': Decimal('110.00'),
                'category': 'condo',
                'bedrooms': 2,
                'bathrooms': 1,
                'max_guests': 4,
                'amenities': {'wifi': True, 'kitchen': True, 'air_conditioning': True}
            }
        ]
        
        # Get all users to assign as hosts
        users = list(User.objects.all())
        
        # Create the predefined listings
        for i, listing_data in enumerate(listings_data):
            if i >= count:
                break
                
            amenities = listing_data.pop('amenities', {})
            listing = Listing.objects.create(
                host=random.choice(users),
                **listing_data,
                **amenities
            )
        
        # Create additional random listings if needed
        locations = [
            'Austin, TX', 'Portland, OR', 'Denver, CO', 'Nashville, TN',
            'Las Vegas, NV', 'Phoenix, AZ', 'San Diego, CA', 'Atlanta, GA',
            'New Orleans, LA', 'Orlando, FL', 'Minneapolis, MN', 'Detroit, MI'
        ]
        
        categories = ['apartment', 'house', 'villa', 'condo', 'cabin', 'studio']
        
        for i in range(len(listings_data), count):
            listing = Listing.objects.create(
                title=f'Amazing {random.choice(categories).title()} #{i+1}',
                description=f'A wonderful place to stay in {random.choice(locations)}.',
                location=random.choice(locations),
                price_per_night=Decimal(str(random.randint(50, 300))),
                category=random.choice(categories),
                bedrooms=random.randint(1, 4),
                bathrooms=random.randint(1, 3),
                max_guests=random.randint(1, 8),
                host=random.choice(users),
                wifi=random.choice([True, False]),
                parking=random.choice([True, False]),
                pool=random.choice([True, False]),
                kitchen=random.choice([True, False]),
                air_conditioning=random.choice([True, False])
            )
        
        self.stdout.write(f'Created {count} listings.')
    
    def create_bookings(self, count):
        """Create sample bookings"""
        self.stdout.write(f'Creating {count} bookings...')
        
        listings = list(Listing.objects.all())
        users = list(User.objects.all())
        
        statuses = ['pending', 'confirmed', 'cancelled', 'completed']
        
        for i in range(count):
            listing = random.choice(listings)
            user = random.choice(users)
            
            # Ensure user is not the host of the listing
            while user == listing.host:
                user = random.choice(users)
            
            # Generate random dates
            start_date = date.today() + timedelta(days=random.randint(-30, 60))
            duration = random.randint(1, 14)  # 1-14 days
            end_date = start_date + timedelta(days=duration)
            
            # Calculate total price
            total_price = listing.price_per_night * duration
            
            # Create booking
            booking = Booking.objects.create(
                listing=listing,
                user=user,
                check_in_date=start_date,
                check_out_date=end_date,
                num_guests=random.randint(1, min(listing.max_guests, 6)),
                total_price=total_price,
                status=random.choice(statuses),
                special_requests=random.choice([
                    '', 'Early check-in please', 'Late checkout requested',
                    'Ground floor preferred', 'Quiet room please',
                    'Extra towels needed', 'Vegetarian breakfast'
                ])
            )
        
        self.stdout.write(f'Created {count} bookings.')
    
    def create_reviews(self, count):
        """Create sample reviews"""
        self.stdout.write(f'Creating {count} reviews...')
        
        # Get completed bookings for realistic reviews
        completed_bookings = list(Booking.objects.filter(status='completed'))
        
        if not completed_bookings:
            self.stdout.write('No completed bookings found. Creating some completed bookings first...')
            # Create some completed bookings
            listings = list(Listing.objects.all())
            users = list(User.objects.all())
            
            for i in range(min(count, 10)):
                listing = random.choice(listings)
                user = random.choice(users)
                
                while user == listing.host:
                    user = random.choice(users)
                
                start_date = date.today() - timedelta(days=random.randint(30, 90))
                duration = random.randint(1, 7)
                end_date = start_date + timedelta(days=duration)
                
                booking = Booking.objects.create(
                    listing=listing,
                    user=user,
                    check_in_date=start_date,
                    check_out_date=end_date,
                    num_guests=random.randint(1, min(listing.max_guests, 4)),
                    total_price=listing.price_per_night * duration,
                    status='completed'
                )
                completed_bookings.append(booking)
        
        # Sample review comments
        positive_comments = [
            "Amazing place! The host was very welcoming and the location was perfect.",
            "Beautiful property with all the amenities we needed. Would definitely stay again!",
            "Clean, comfortable, and exactly as described. Great value for money.",
            "Perfect for our family vacation. The kids loved the space and amenities.",
            "Fantastic location and the host provided excellent recommendations for local attractions.",
            "The property exceeded our expectations. Everything was spotless and well-maintained.",
            "Great communication from the host and seamless check-in process.",
            "Lovely place with stunning views. We had a wonderful time here."
        ]
        
        neutral_comments = [
            "Nice place overall. A few minor issues but nothing major.",
            "Good location and decent amenities. Pretty much what we expected.",
            "Clean and comfortable. Could use some updates but served our needs.",
            "Average experience. The place was fine for our short stay.",
            "Decent value for the price. Some areas could be improved.",
            "Acceptable accommodation. Met our basic needs for the trip."
        ]
        
        negative_comments = [
            "Place was not as clean as expected and some amenities weren't working.",
            "Location was good but the property needs maintenance and updates.",
            "Had some issues with the booking but the host was responsive.",
            "The place was smaller than expected and could use better cleaning.",
            "Some inconveniences during our stay but manageable overall."
        ]
        
        # Create reviews
        created_reviews = 0
        used_bookings = set()
        
        for booking in completed_bookings:
            if created_reviews >= count:
                break
            
            # Skip if this booking already has a review
            if booking.booking_id in used_bookings:
                continue
            
            # Skip if user already reviewed this listing
            if Review.objects.filter(user=booking.user, listing=booking.listing).exists():
                continue
            
            # Determine rating and corresponding comment
            rating = random.choices([1, 2, 3, 4, 5], weights=[5, 10, 20, 35, 30])[0]
            
            if rating >= 4:
                comment = random.choice(positive_comments)
            elif rating == 3:
                comment = random.choice(neutral_comments)
            else:
                comment = random.choice(negative_comments)
            
            try:
                review = Review.objects.create(
                    listing=booking.listing,
                    user=booking.user,
                    booking=booking,
                    rating=rating,
                    comment=comment
                )
                used_bookings.add(booking.booking_id)
                created_reviews += 1
            except Exception as e:
                self.stdout.write(f'Error creating review: {e}')
                continue
        
        # If we need more reviews, create some without linking to bookings
        if created_reviews < count:
            listings = list(Listing.objects.all())
            users = list(User.objects.all())
            
            for i in range(count - created_reviews):
                listing = random.choice(listings)
                user = random.choice(users)
                
                # Skip if user is the host or already reviewed
                if user == listing.host or Review.objects.filter(user=user, listing=listing).exists():
                    continue
                
                rating = random.choices([1, 2, 3, 4, 5], weights=[5, 10, 20, 35, 30])[0]
                
                if rating >= 4:
                    comment = random.choice(positive_comments)
                elif rating == 3:
                    comment = random.choice(neutral_comments)
                else:
                    comment = random.choice(negative_comments)
                
                try:
                    Review.objects.create(
                        listing=listing,
                        user=user,
                        rating=rating,
                        comment=comment
                    )
                    created_reviews += 1
                except Exception as e:
                    continue
        
        self.stdout.write(f'Created {created_reviews} reviews.')
