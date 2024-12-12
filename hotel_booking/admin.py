from django.contrib import admin
from .models import Customer, RoomType, Room, Booking, Payment, Service, BookingService

admin.site.register(Customer)
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Service)
admin.site.register(BookingService)