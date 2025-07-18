# ALX Travel App - Database Modeling & Seeding

A Django-based travel booking application with comprehensive database modeling, API serialization, and data seeding capabilities.

## Project Structure

```
alx_travel_app_0x00/
├── alx_travel_app/
│   ├── listings/
│   │   ├── models.py                    # Database models
│   │   ├── serializers.py               # API serializers
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── seed.py              # Database seeding command
│   │   └── ...
│   ├── manage.py
│   └── ...
└── README.md
```

## Database Models

### Listing Model
Represents travel accommodations with the following features:
- **Primary Key**: UUID-based `listing_id`
- **Basic Info**: Title, description, location, pricing
- **Property Details**: Bedrooms, bathrooms, max guests, category
- **Amenities**: WiFi, parking, pool, kitchen, A/C
- **Relationships**: Foreign key to User (host)
- **Validation**: Price validation, guest capacity limits
- **Methods**: Average rating calculation, review count

### Booking Model
Manages reservation data with:
- **Primary Key**: UUID-based `booking_id`
- **Relationships**: Foreign keys to Listing and User
- **Booking Details**: Check-in/out dates, guest count, total price
- **Status Tracking**: Pending, confirmed, cancelled, completed
- **Validation**: Date constraints, guest limits, overlap prevention
- **Methods**: Duration calculation, price computation

### Review Model
Handles user feedback with:
- **Primary Key**: UUID-based `review_id`
- **Relationships**: Foreign keys to Listing, User, and Booking
- **Review Data**: Rating (1-5), comment text
- **Constraints**: Unique user-listing reviews, completed bookings only
- **Validation**: Rating range, booking completion verification

## API Serializers

### ListingSerializer
- **Read Operations**: Full listing details with computed fields
- **Computed Fields**: Average rating, total reviews
- **Validation**: Price and guest count validation
- **Relationships**: Nested host information

### BookingSerializer
- **Create Operations**: Booking creation with validation
- **Date Validation**: Past date prevention, logical date ordering
- **Availability Check**: Overlap detection, listing availability
- **Price Calculation**: Automatic total price computation
- **Guest Validation**: Capacity limit enforcement

### ReviewSerializer
- **User Constraints**: Only completed booking reviews allowed
- **Uniqueness**: One review per user per listing
- **Rating Validation**: 1-5 range enforcement
- **Authorization**: User authentication required

## Database Seeding

### Management Command: `seed.py`

**Usage:**
```bash
python manage.py seed [options]
```

**Options:**
- `--listings N`: Number of listings to create (default: 20)
- `--bookings N`: Number of bookings to create (default: 50)
- `--reviews N`: Number of reviews to create (default: 30)
- `--clear`: Clear existing data before seeding

**Sample Data Created:**
- **Users**: 8 sample users with different roles (hosts, guests, travelers)
- **Listings**: Diverse properties across major US cities
- **Bookings**: Realistic booking patterns with various statuses
- **Reviews**: Balanced review distribution with authentic comments

## Installation & Setup

### Prerequisites
- Python 3.8+
- Django 4.0+
- Django REST Framework
- PostgreSQL (recommended) or SQLite

### Installation Steps

1. **Clone the Repository:**
```bash
git clone <repository-url>
cd alx_travel_app_0x00
```

2. **Create Virtual Environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies:**
```bash
pip install django djangorestframework psycopg2-binary
```

4. **Configure Database:**
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'alx_travel_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

5. **Run Migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create Superuser:**
```bash
python manage.py createsuperuser
```

7. **Seed Database:**
```bash
python manage.py seed --listings 25 --bookings 60 --reviews 40
```

## Database Schema

### Key Relationships
- **One-to-Many**: User → Listings (host relationship)
- **One-to-Many**: User → Bookings (guest relationship)
- **One-to-Many**: Listing → Bookings
- **One-to-Many**: Listing → Reviews
- **One-to-One**: Booking → Review (optional)

### Indexes
- Location-based searches
- Price range queries
- Availability status
- Date range lookups
- Rating-based filtering

### Constraints
- Check-out after check-in dates
- Guest count within listing capacity
- Unique user-listing review combinations
- Rating range validation (1-5)

## API Endpoints Structure

Based on the serializers, the following endpoints would be available:

### Listings
- `GET /api/listings/` - List all listings
- `POST /api/listings/` - Create new listing
- `GET /api/listings/{id}/` - Retrieve specific listing
- `PUT /api/listings/{id}/` - Update listing
- `DELETE /api/listings/{id}/` - Delete listing

### Bookings
- `GET /api/bookings/` - List user's bookings
- `POST /api/bookings/` - Create new booking
- `GET /api/bookings/{id}/` - Retrieve specific booking
- `PUT /api/bookings/{id}/` - Update booking
- `DELETE /api/bookings/{id}/` - Cancel booking

### Reviews
- `GET /api/reviews/` - List reviews
- `POST /api/reviews/` - Create new review
- `GET /api/reviews/{id}/` - Retrieve specific review
- `PUT /api/reviews/{id}/` - Update review
- `DELETE /api/reviews/{id}/` - Delete review

## Testing the Seeded Data

### Verify Data Creation
```bash
# Check created records
python manage.py shell
```

```python
from listings.models import Listing, Booking, Review
from django.contrib.auth.models import User

# Verify counts
print(f"Users: {User.objects.count()}")
print(f"Listings: {Listing.objects.count()}")
print(f"Bookings: {Booking.objects.count()}")
print(f"Reviews: {Review.objects.count()}")

# Sample queries
print("\nSample listings:")
for listing in Listing.objects.all()[:3]:
    print(f"- {listing.title} in {listing.location} (${listing.price_per_night}/night)")

print("\nSample bookings:")
for booking in Booking.objects.all()[:3]:
    print(f"- {booking.user.username} booked {booking.listing.title} ({booking.status})")
```

### Admin Interface
Access the Django admin at `/admin/` to browse and manage the seeded data.

## Model Features

### Advanced Validation
- **Date Logic**: Prevents past bookings, ensures logical date ordering
- **Capacity Management**: Enforces guest limits per listing
- **Availability Tracking**: Prevents double bookings
- **Review Authorization**: Links reviews to completed bookings

### Performance Optimization
- **Database Indexes**: Optimized for common query patterns
- **Computed Fields**: Cached average ratings and review counts
- **Efficient Queries**: Minimized N+1 query problems

### Data Integrity
- **UUID Primary Keys**: Globally unique identifiers
- **Referential Integrity**: Proper foreign key relationships
- **Constraint Validation**: Database-level constraint enforcement
- **Transaction Safety**: Atomic operations for data consistency

## Development Notes

### Model Relationships
The models use Django's ORM relationships effectively:
- `ForeignKey` for many-to-one relationships
- `OneToOneField` for booking-review links
- `related_name` for reverse lookups

### Serializer Patterns
- **Nested Serializers**: For related object representation
- **Method Fields**: For computed values
- **Validation**: Custom validation methods
- **Context Usage**: Request-based data handling

### Command Design
The seed command follows Django best practices:
- **Argument Parsing**: Flexible parameter handling
- **Data Relationships**: Realistic data connections
- **Error Handling**: Graceful failure management
- **Progress Reporting**: User feedback during execution

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is created for educational purposes as part of the ALX Software Engineering program.
