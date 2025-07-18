from rest_framework import serializers
from .models import Listing, Booking
from django.contrib.auth.models import User

# Serializer for User model (to use it in Listing and Booking serializers)
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model - used in nested relationships"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']

# Serializer for Listing model
class ListingSerializer(serializers.ModelSerializer):
    """Serializer for Listing model"""
    
    host = UserSerializer(read_only=True)  # Nested UserSerializer for the host
    
    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'location', 
            'price_per_night', 'max_guests', 'bedrooms', 'bathrooms',
            'is_available', 'created_at', 'updated_at', 'host'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

# Serializer for Booking model
class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model"""
    
    listing = ListingSerializer(read_only=True)  # Nested ListingSerializer
    user = UserSerializer(read_only=True)  # Nested UserSerializer

    class Meta:
        model = Booking
        fields = [
            'id', 'listing', 'user', 'check_in_date', 'check_out_date', 
            'num_guests', 'total_price', 'status', 'special_requests', 
            'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']

    def validate(self, data):
        """
        Custom validation for booking data, e.g., validating the booking
        dates, guest count, and availability.
        """
        # Validate that check-out is after check-in
        check_in = data.get('check_in_date')
        check_out = data.get('check_out_date')
        num_guests = data.get('num_guests')
        listing = data.get('listing')

        if check_in and check_out:
            if check_out <= check_in:
                raise serializers.ValidationError("Check-out date must be after check-in date.")
        
        if listing and num_guests:
            if num_guests > listing.max_guests:
                raise serializers.ValidationError(f"Number of guests exceeds the maximum allowed ({listing.max_guests}).")
        
        return data
