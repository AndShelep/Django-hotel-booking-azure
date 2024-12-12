from django.contrib.auth.models import User
from django.db import models

class Customer(models.Model):
    customer_name = models.CharField(max_length=25)
    customer_surname = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=12)
    customer_email = models.EmailField(max_length=64)

    class Meta:
        db_table = 'customer'


class RoomType(models.Model):
    room_type = models.CharField(max_length=20)
    number_of_beds = models.IntegerField()
    room_type_description = models.CharField(max_length=256)

    class Meta:
        db_table = 'room_type'

class Room(models.Model):
    room_number = models.IntegerField(primary_key=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'room'

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    in_date = models.DateField()
    out_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_status = models.CharField(max_length=20)

    class Meta:
        db_table = 'booking'

class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True)
    payment_method = models.CharField(max_length=10, choices=[('cash', 'Cash'), ('card', 'Card')])
    payment_date = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=15)

    class Meta:
        db_table = 'payment'

class Service(models.Model):
    service_name = models.CharField(max_length=20)
    service_description = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'service'

class BookingService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

    class Meta:
        db_table = 'booking_service'
        constraints = [
            models.UniqueConstraint(fields=['booking', 'service'], name='booking-service')
        ]