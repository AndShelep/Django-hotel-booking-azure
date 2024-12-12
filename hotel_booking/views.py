from datetime import datetime, date
import pandas as pd
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.db.models import Avg, Max, Min
from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
import re

from .forms import CustomerForm
from .models import Customer, RoomType, Room, Booking, Payment, Service, BookingService
from .repositories import HotelBookingManager
from .serializers import CustomerSerializer, RoomTypeSerializer, RoomSerializer, ServiceSerializer, BookingSerializer, \
    PaymentSerializer, BookingServiceSerializer

hotelBookingManager = HotelBookingManager()

def admin_page(request):
    return render(request, 'admin_page.html')

def home(request):
    return render(request, 'home.html')


def add_customer(request):
    if request.method == "POST":
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        if not re.fullmatch(r"\d{12}", phone):
            error_message = "Phone number must contain exactly 12 digits."
            return render(request, "customer/add_customer.html", {"error_message": error_message})

        customer = hotelBookingManager.customer_repository.create(customer_name=name, customer_surname=surname, phone_number=phone, customer_email=email)
        return redirect('list_customers')

    return render(request, "customer/add_customer.html")

def list_customers(request):
    customers = hotelBookingManager.customer_repository.get_all()
    return render(request, "customer/list_customers.html", {"customers": customers})

def get_customer(request):
    customer = None
    error_message = None
    if request.method == "POST":
        id = request.POST.get('tid')
        try:
            customer = hotelBookingManager.customer_repository.get_by_id(id)
        except Customer.DoesNotExist:
            error_message = "There is no payment with such ID."

    return render(request, "customer/get_customer.html", {"customer": customer, "error_message": error_message})

def update_customer(request, id):
    customer = hotelBookingManager.customer_repository.get_by_id(id)
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_surname = request.POST.get('customer_surname')
        phone_number = request.POST.get('phone_number')
        customer_email = request.POST.get('customer_email')
        hotelBookingManager.customer_repository.update(id, customer_name=customer_name, customer_surname=customer_surname, phone_number=phone_number, customer_email=customer_email)
        return redirect('list_customers')
    return render(request, 'customer/update_customer.html', {'customer': customer})

def delete_customer(request, id):
    if request.method == 'POST':
        hotelBookingManager.customer_repository.delete(id)
    return redirect('list_customers')


def add_room_type(request):
    if request.method == "POST":
        room_type = request.POST.get('troom_type')
        number_of_beds = request.POST.get('tnumber_of_beds')
        room_type_description = request.POST.get('tdescription')

        room_type = hotelBookingManager.room_type_repository.create(
            room_type_description=room_type_description,
            room_type=room_type,
            number_of_beds=number_of_beds
        )

        return redirect("list_room_types")

    return render(request, "room_type/add_room_type.html")

def list_room_types(request):
    room_types = hotelBookingManager.room_type_repository.get_all()
    return render(request, "room_type/list_room_types.html", {"room_types": room_types})

def get_room_type(request):
    room_type = None
    if request.method == "POST":
        id = request.POST.get('tid')
        room_type = hotelBookingManager.room_type_repository.get_by_id(id)
    return render(request, "room_type/get_room_type.html", {"room_type": room_type})


def add_service(request):
    if request.method == "POST":
        service_name = request.POST.get('tname')
        service_description = request.POST.get('tdescription')
        price = request.POST.get('tprice')

        service = hotelBookingManager.service_repository.create(
            service_name=service_name,
            service_description=service_description,
            price=price
        )

        return redirect("list_services")
    return render(request, "service/add_service.html")

def list_services(request):
    services = hotelBookingManager.service_repository.get_all()
    return render(request, "service/list_services.html", {"services": services})

def get_service(request):
    serivce = None
    error_message = None
    if request.method == "POST":
        id = request.POST.get('tid')
        try:
            service = hotelBookingManager.service_repository.get_by_id(id)
        except Service.DoesNotExist:
            error_message = "There is no service with such ID."

    return render(request, "service/get_service.html", {"service": service, "error_message": error_message})

def update_service(request, id):
    service = hotelBookingManager.service_repository.get_by_id(id)
    if request.method == "POST":
        service_name = request.POST.get('service_name')
        service_description = request.POST.get('description')
        price = request.POST.get('price')

        hotelBookingManager.service_repository.update(id=id, service_name=service_name, service_description=service_description, price=price)
        return redirect('list_services')
    return render(request, "service/update_service.html", {"service": service})

def delete_service(request, id):
    service = hotelBookingManager.service_repository.get_by_id(id)
    hotelBookingManager.service_repository.delete(id)
    return redirect('list_services')

def add_room(request):
    if request.method == "POST":
        room_number = request.POST.get('tnumber')
        type = request.POST.get('troom_type')
        price = request.POST.get('tprice')

        room_type = hotelBookingManager.room_type_repository.get_by_id(type)

        room = hotelBookingManager.room_repository.create(
            room_number=room_number,
            room_type=room_type,
            price_per_night=price
        )

        return redirect("list_rooms")
    room_types = hotelBookingManager.room_type_repository.get_all()
    return render(request, "room/add_room.html", {"room_types": room_types})

def list_rooms(request):
    rooms = hotelBookingManager.room_repository.get_all()
    return render(request, "room/list_rooms.html", {"rooms": rooms})

def get_room(request):
    room = None
    error_message = None
    if request.method == "POST":
        id = request.POST.get('tnumber')
        try:
            room = hotelBookingManager.room_repository.get_by_id(id)
        except Room.DoesNotExist:
            error_message = "There is no room with such number."

    return render(request, "room/get_room.html", {"room": room, "error_message": error_message})

def update_room(request, id):
    room = hotelBookingManager.room_repository.get_by_id(id)
    room_types = hotelBookingManager.room_type_repository.get_all()
    if request.method == "POST":
        room_number = request.POST.get('number')
        room_type_id = request.POST.get('room_type')
        price_per_night = request.POST.get('price')

        room_type = hotelBookingManager.room_type_repository.get_by_id(room_type_id)

        hotelBookingManager.room_repository.update(id=id, room_number=room_number, room_type=room_type, price_per_night=price_per_night)
        return redirect("list_rooms")
    return render(request, "room/update_room.html", {"room": room, "room_types": room_types})


def add_booking(request):
    if request.method == "POST":
        room_number = request.POST.get('troom_number')
        name = request.POST.get('tname')
        surname = request.POST.get('tsurname')
        phone_number = request.POST.get('tphone_number')
        in_date = datetime.strptime(request.POST.get('tin_date'), '%Y-%m-%d').date()
        out_date = datetime.strptime(request.POST.get('tout_date'), '%Y-%m-%d').date()
        services_id = request.POST.getlist('tservices')

        try:
            customer = Customer.objects.get(customer_name=name, customer_surname=surname, phone_number=phone_number)
        except Customer.DoesNotExist:
            rooms = hotelBookingManager.room_repository.get_all()
            services = hotelBookingManager.service_repository.get_all()
            return render(
                request,
                "booking/add_booking.html",
                {
                    "rooms": rooms,
                    "services": services,
                    "error_message": "There is no customer with such data",
                },
            )
        room = hotelBookingManager.room_repository.get_by_id(room_number)
        bookings = Booking.objects.filter(room=room)
        if bookings:
            for book in bookings:
                if book.out_date > in_date and book.in_date < out_date:
                    rooms = hotelBookingManager.room_repository.get_all()
                    services = hotelBookingManager.service_repository.get_all()
                    return render(
                        request,
                        "booking/add_booking.html",
                        {
                            "rooms": rooms,
                            "services": services,
                            "error_message": f"Room {room_number} is occupied for the selected dates.",
                        },
                    )
        price = room.price_per_night * (out_date - in_date).days
        services = Service.objects.filter(id__in=services_id)

        booking = hotelBookingManager.booking_repository.create(
            room=room,
            customer=customer,
            in_date=in_date,
            out_date=out_date,
            total_price=price,
            booking_status="pending"
        )

        if services:
            for service in services:
                hotelBookingManager.booking_service_repository.create(booking=booking, service=service)
                booking.total_price += service.price
            booking.save()

        return redirect("list_bookings")
    rooms = hotelBookingManager.room_repository.get_all()
    services = hotelBookingManager.service_repository.get_all()
    return render(request, "booking/add_booking.html", {"rooms": rooms, "services": services})

def delete_booking(request, id):
    booking = hotelBookingManager.booking_repository.get_by_id(id)
    payment = Payment.objects.filter(booking=booking)
    if payment:
        payment.payment_status = "refunded"
    hotelBookingManager.booking_repository.delete(id)
    return redirect("list_bookings")

def list_bookings(request):
    bookings = hotelBookingManager.booking_repository.get_all()
    for booking in bookings:
        booking.services = Service.objects.filter(bookingservice__booking=booking)
    return render(request, "booking/list_bookings.html", {"bookings": bookings})

def get_booking(request):
    booking = None
    error_message = None
    if request.method == "POST":
        id = request.POST.get('tid')
        try:
            booking = hotelBookingManager.booking_repository.get_by_id(id)
        except Booking.DoesNotExist:
            error_message = "There is no booking with such ID."

    return render(request, "booking/get_booking.html", {"booking": booking, "error_message": error_message})


def add_payment(request):
    if request.method == "POST":
        booking_id = request.POST.get('booking_id')
        method = request.POST.get('payment_method')
        date_time = datetime.strptime(request.POST.get('datetime'), '%Y-%m-%dT%H:%M')

        booking = hotelBookingManager.booking_repository.get_by_id(booking_id)

        payment = hotelBookingManager.payment_repository.create(
            booking=booking,
            payment_method=method,
            payment_date=date_time,
            total_price=booking.total_price,
            payment_status="completed"

        )

        if payment:
            booking.booking_status = "accepted"
            booking.save()

        return redirect("list_bookings")
    return render(request, "payment/add_payment.html")

def get_payment(request):
    payment = None
    error_message = None
    if request.method == "POST":
        id = request.POST.get('tid')
        try:
            payment = hotelBookingManager.payment_repository.get_by_id(id)
        except Payment.DoesNotExist:
            error_message = "There is no payment with such ID."

    return render(request, "payment/get_payment.html", {"payment": payment, "error_message": error_message})

class CustomerAPI(viewsets.ModelViewSet):
    queryset = hotelBookingManager.customer_repository.get_all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class RoomTypeAPI(viewsets.ModelViewSet):
    queryset = hotelBookingManager.room_type_repository.get_all()
    serializer_class = RoomTypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class RoomAPI(viewsets.ModelViewSet):
    queryset = hotelBookingManager.room_repository.get_all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookingAPI(viewsets.ModelViewSet):
    queryset = hotelBookingManager.booking_repository.get_all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['post'], url_path='add_booking')
    def add_booking(self, request):
        data = request.data
        room_number = data.get('room_number')
        name = data.get('name')
        surname = data.get('surname')
        phone_number = data.get('phone_number')
        in_date = datetime.strptime(data.get('in_date'), '%Y-%m-%d').date()
        out_date = datetime.strptime(data.get('out_date'), '%Y-%m-%d').date()
        services_id = data.get('services', [])

        try:
            customer = Customer.objects.get(
                customer_name=name, customer_surname=surname, phone_number=phone_number
            )
        except Customer.DoesNotExist:
            return Response(
                {"error": "There is no customer with such data."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            room = hotelBookingManager.room_repository.get_by_id(room_number)
        except Room.DoesNotExist:
            return Response(
                {"error": "The selected room does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        overlapping_bookings = Booking.objects.filter(
            room=room,
            in_date__lt=out_date,
            out_date__gt=in_date,
        )
        if overlapping_bookings.exists():
            return Response(
                {"error": f"Room {room_number} is occupied for the selected dates."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        price = room.price_per_night * (out_date - in_date).days
        services = Service.objects.filter(id__in=services_id)

        booking = hotelBookingManager.booking_repository.create(
            room=room,
            customer=customer,
            in_date=in_date,
            out_date=out_date,
            total_price=price,
            booking_status="pending",
        )

        if services:
            for service in services:
                hotelBookingManager.booking_service_repository.create(
                    booking=booking, service=service
                )
                booking.total_price += service.price
            booking.save()

        return Response(
            {
                "message": "Booking created successfully.",
                "booking_id": booking.id,
                "total_price": booking.total_price,
            },
            status=status.HTTP_201_CREATED,
        )

class ServiceAPI(viewsets.ModelViewSet):
    queryset = hotelBookingManager.service_repository.get_all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class PaymentAPI(viewsets.ModelViewSet):
    queryset = hotelBookingManager.payment_repository.get_all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookingServiceAPI(viewsets.ModelViewSet):
    queryset = hotelBookingManager.booking_service_repository.get_all()
    serializer_class = BookingServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]



class CustomerBookingsAPIView(APIView):
    def get(self, request):
        queryset = hotelBookingManager.customer_repository.get_all().annotate(
            total_bookings = Count('booking')
        ).values('customer_name', 'customer_surname', 'phone_number', 'total_bookings')
        df = pd.DataFrame(list(queryset))
        return Response(df.to_dict(orient='records'))


class BookingServicesAPIView(APIView):
    def get(self, request):
        queryset = hotelBookingManager.booking_service_repository.get_all().annotate(
            total_bookings=Count('booking')
        ).values('service__service_name', 'total_bookings')
        df = pd.DataFrame(list(queryset))
        return Response(df.to_dict(orient='records'))


class MonthlyBookingsAPIView(APIView):
    def get(self, request):
        start_date = date(2024, 11, 1)
        end_date = date(2025, 2, 28)
        queryset = hotelBookingManager.booking_repository.get_all().filter(
            in_date__gte=start_date,
            in_date__lte=end_date
        ).annotate(
            month=TruncMonth('in_date')
        ).values('month').annotate(
            total_bookings=Count('id')
        ).order_by('month')

        df = pd.DataFrame(list(queryset))
        df['month'] = pd.to_datetime(df['month'])
        all_months = pd.date_range(start=start_date, end=end_date, freq='MS')
        df_all = pd.DataFrame({'month': all_months})
        df = df_all.merge(df, on='month', how='left').fillna({'total_bookings': 0})
        df['month_year'] = df['month'].dt.strftime('%Y-%m')
        df['total_bookings'] = df['total_bookings'].astype(int)
        return Response(df.to_dict(orient='records'))


class RoomIncomeAPIView(APIView):
    def get(self, request):
        queryset = hotelBookingManager.booking_repository.get_all().values('room__room_number').annotate(
            total_income=Sum('total_price')
        )
        df = pd.DataFrame(list(queryset))
        df['room__room_number'] = df['room__room_number'].astype(str)
        return Response(df.to_dict(orient='records'))


class MonthlyIncomeAPIView(APIView):
    def get(self, request):
        queryset = hotelBookingManager.booking_repository.get_all().annotate(
            month=TruncMonth('in_date')
        ).values('month').annotate(
            total_income=Sum('total_price')
        ).order_by('month')

        df = pd.DataFrame(list(queryset))
        df['month'] = pd.to_datetime(df['month']).dt.strftime('%Y-%m')
        return Response(df.to_dict(orient='records'))

class CustomerIncomeAPIView(APIView):
    def get(self, request):
        queryset = hotelBookingManager.booking_repository.get_all().values(
            'customer__customer_name', 'customer__customer_surname', 'customer__phone_number'
        ).annotate(
            total_income=Sum('total_price')
        ).order_by('-total_income')

        df = pd.DataFrame(list(queryset))
        df['customer'] = df['customer__customer_name'] + ' ' + df['customer__customer_surname'] + ' (' + df[
            'customer__phone_number'] + ')'
        return Response(df.to_dict(orient='records'))

class BookingStatisticsAPIView(APIView):
    def get(self, request):
        queryset = hotelBookingManager.booking_repository.get_all().annotate(
            month=TruncMonth('in_date')
        ).values('month').annotate(
            avg_price=Avg('total_price'),
            min_price=Min('total_price'),
            max_price=Max('total_price')
        ).order_by('month')

        df = pd.DataFrame(list(queryset))

        if df.empty:
            return Response({'message': 'No data available'}, status=404)

        all_data = hotelBookingManager.booking_repository.get_all().annotate(
            month=TruncMonth('in_date')
        ).values('month', 'total_price')

        all_data_df = pd.DataFrame(list(all_data))
        if not all_data_df.empty:
            medians = (
                all_data_df.groupby('month')['total_price']
                .median()
                .reset_index()
                .rename(columns={'total_price': 'median_price'})
            )
            df = df.merge(medians, on='month', how='left')

        df['month'] = pd.to_datetime(df['month']).dt.strftime('%Y-%m')

        return Response(df.to_dict(orient='records'))