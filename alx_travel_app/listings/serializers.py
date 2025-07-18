from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Listing, Booking


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model - used in nested relationships"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class ListingSerializer(serializers.ModelSerializer):
    """Serializer for Listing model"""
    
    host = UserSerializer(read_only=True)
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Listing
        fields = [
            'listing_id', 'title', 'description', 'location', 
            'price_per_night', 'max_guests', 'bedrooms', 'bathrooms',
            'wifi', 'parking', 'pool', 'kitchen', 'air_conditioning',
            'is_available', 'category', 'host', 'average_rating', 
            'total_reviews', 'created_at', 'updated_at'
        ]
        read_only_fields = ['listing_id', 'host', 'created_at', 'updated_at']
    
    def get_average_rating(self, obj):
        """Get average rating for the listing"""
        return round(obj.get_average_rating(), 1)
    
    def get_total_reviews(self, obj):
        """Get total number of reviews for the listing"""
        return obj.get_total_reviews()
    
    def validate_price_per_night(self, value):
        """Validate price per night is positive"""
        if value <= 0:
            raise serializers.ValidationError("Price per night must be greater than 0.")
        return value
    
    def validate_max_guests(self, value):
        """Validate max guests is at least 1"""
        if value <= 0:
            raise serializers.ValidationError("Max guests must be at least 1.")
        return value
    
    def create(self, validated_data):
        """Create a new listing with the current user as host"""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['host'] = request.user
        return super().create(validated_data)


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model"""
    
    listing = ListingSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    listing_id = serializers.UUIDField(write_only=True)
    duration_days = serializers.ReadOnlyField()
    
    class Meta:
        model = Booking
        fields = [
            'booking_id', 'listing', 'user', 'listing_id', 
            'check_in_date', 'check_out_date', 'num_guests', 
            'total_price', 'status', 'special_requests',
            'duration_days', 'created_at', 'updated_at'
        ]
        read_only_fields = ['booking_id', 'user', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate booking data"""
        check_in = data.get('check_in_date')
        check_out = data.get('check_out_date')
        num_guests = data.get('num_guests')
        listing_id = data.get('listing_id')
        
        # Validate dates
        if check_in and check_out:
            if check_out <= check_in:
                raise serializers.ValidationError(
                    "Check-out date must be after check-in date."
                )
            
            from django.utils import timezone
            if check_in < timezone.now().date():
                raise serializers.ValidationError(
                    "Check-in date cannot be in the past."
                )
        
        # Validate guest count against listing capacity
        if listing_id and num_guests:
            try:
                listing = Listing.objects.get(listing_id=listing_id)
                if num_guests > listing.max_guests:
                    raise serializers.ValidationError(
                        f"Number of guests ({num_guests}) exceeds maximum allowed ({listing.max_guests})."
                    )
                
                # Check if listing is available
                if not listing.is_available:
                    raise serializers.ValidationError(
                        "This listing is currently not available for booking."
                    )
                
                # Check for overlapping bookings
                overlapping_bookings = Booking.objects.filter(
                    listing=listing,
                    status__in=['pending', 'confirmed'],
                    check_in_date__lt=check_out,
                    check_out_date__gt=check_in
                )
                
                if overlapping_bookings.exists():
                    raise serializers.ValidationError(
                        "The selected dates are not available for this listing."
                    )
                
            except Listing.DoesNotExist:
                raise serializers.ValidationError("Invalid listing ID.")
        
        return data
    
    def create(self, validated_data):
        """Create a new booking"""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        
        # Get listing and calculate total price
        listing_id = validated_data.pop('listing_id')
        listing = Listing.objects.get(listing_id=listing_id)
        validated_data['listing'] = listing
        
        # Calculate total price if not provided
        if 'total_price' not in validated_data:
            check_in = validated_data['check_in_date']
            check_out = validated_data['check_out_date']
            duration = (check_out - check_in).days
            validated_data['total_price'] = listing.price_per_night * duration
        
        return super().create(validated_data)
