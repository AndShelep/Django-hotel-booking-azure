from django.test import TestCase
from django.urls import reverse
from .models import Customer, Room, RoomType, Booking, Service
from datetime import datetime, timedelta


# class AddCustomerViewTest(TestCase):
#     def test_add_customer_view_success(self):
#         url = reverse('add_customer')
#         data = {
#             'name': 'Alice',
#             'surname': 'Smith',
#             'phone': '098765432109',
#             'email': 'alice@example.com'
#         }
#
#         response = self.client.post(url, data)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTrue(Customer.objects.filter(customer_name="Alice").exists())
#
#     def test_invalid_phone_number(self):
#         url = reverse('add_customer')
#         data = {
#             'name': 'John',
#             'surname': 'Doe',
#             'phone': '12345',
#             'email': 'johndoe@example.com'
#         }
#
#         response = self.client.post(url, data)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Phone number must contain exactly 12 digits.")
#         self.assertTemplateUsed(response, "customer/add_customer.html")



class AddBookingViewTest(TestCase):
    def setUp(self):
        self.room_type = RoomType.objects.create(
            room_type="Single",
            number_of_beds=1,
            room_type_description="Single room with one bed"
        )
        self.room = Room.objects.create(
            room_number=101,
            room_type=self.room_type,
            price_per_night=100.00
        )
        self.customer = Customer.objects.create(
            customer_name="John",
            customer_surname="Doe",
            phone_number="123456789012",
            customer_email="johndoe@example.com"
        )
        self.service = Service.objects.create(
            service_name="Breakfast",
            service_description="Morning breakfast",
            price=20.00
        )
        self.url = reverse("add_booking")

    def test_successful_booking_creation(self):
        in_date = datetime.now().date()
        out_date = in_date + timedelta(days=2)
        post_data = {
            'troom_number': self.room.room_number,
            'tname': self.customer.customer_name,
            'tsurname': self.customer.customer_surname,
            'tphone_number': self.customer.phone_number,
            'tin_date': in_date.strftime('%Y-%m-%d'),
            'tout_date': out_date.strftime('%Y-%m-%d'),
            'tservices': [self.service.id]
        }

        response = self.client.post(self.url, data=post_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Booking.objects.filter(customer=self.customer, room=self.room).exists())
        booking = Booking.objects.get(customer=self.customer, room=self.room)
        self.assertEqual(booking.total_price, 220.00)

    def test_customer_not_found(self):
        in_date = datetime.now().date()
        out_date = in_date + timedelta(days=2)
        post_data = {
            'troom_number': self.room.room_number,
            'tname': "Alice",
            'tsurname': "Smith",
            'tphone_number': "111111111111",
            'tin_date': in_date.strftime('%Y-%m-%d'),
            'tout_date': out_date.strftime('%Y-%m-%d'),
            'tservices': [self.service.id]
        }

        response = self.client.post(self.url, data=post_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There is no customer with such data")
        self.assertTemplateUsed(response, "booking/add_booking.html")

    def test_room_occupied(self):
        in_date = datetime.now().date()
        out_date = in_date + timedelta(days=2)

        Booking.objects.create(
            room=self.room,
            customer=self.customer,
            in_date=in_date,
            out_date=out_date,
            total_price=200.00,
            booking_status="pending"
        )

        post_data = {
            'troom_number': self.room.room_number,
            'tname': self.customer.customer_name,
            'tsurname': self.customer.customer_surname,
            'tphone_number': self.customer.phone_number,
            'tin_date': in_date.strftime('%Y-%m-%d'),
            'tout_date': out_date.strftime('%Y-%m-%d'),
            'tservices': [self.service.id]
        }

        response = self.client.post(self.url, data=post_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"Room {self.room.room_number} is occupied for the selected dates.")
        self.assertTemplateUsed(response, "booking/add_booking.html")
