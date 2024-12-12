from .models import Customer, RoomType, Room, Booking, Payment, Service, BookingService

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_all(self):
        return self.model.objects.all()

    def get_by_id(self, id):
        return self.model.objects.get(pk=id)

    def create(self, **kwargs):
        return self.model.objects.create(**kwargs)

    def update(self, id, **kwargs):
        instance = self.get_by_id(id)
        for field, value in kwargs.items():
            setattr(instance, field, value)
        instance.save()
        return instance

    def delete(self, id):
        instance = self.get_by_id(id)
        instance.delete()

class CustomerRepository(BaseRepository):
    def __init__(self):
        super().__init__(Customer)

class RoomTypeRepository(BaseRepository):
    def __init__(self):
        super().__init__(RoomType)

class RoomRepository(BaseRepository):
    def __init__(self):
        super().__init__(Room)

class BookingRepository(BaseRepository):
    def __init__(self):
        super().__init__(Booking)

class PaymentRepository(BaseRepository):
    def __init__(self):
        super().__init__(Payment)

class ServiceRepository(BaseRepository):
    def __init__(self):
        super().__init__(Service)

class BookingServiceRepository(BaseRepository):
    def __init__(self):
        super().__init__(BookingService)

class HotelBookingManager:
    def __init__(self):
        self.customer_repository = CustomerRepository()
        self.room_type_repository = RoomTypeRepository()
        self.room_repository = RoomRepository()
        self.booking_repository = BookingRepository()
        self.payment_repository = PaymentRepository()
        self.service_repository = ServiceRepository()
        self.booking_service_repository = BookingServiceRepository()