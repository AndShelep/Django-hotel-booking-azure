from django.contrib import admin
from rest_framework import routers
from django.urls import path, include
from hotel_booking import views, views_plotly, views_bokeh

router = routers.DefaultRouter()
router.register(r'api/customers', views.CustomerAPI)
router.register(r'api/room_types', views.RoomTypeAPI)
router.register(r'api/room', views.RoomAPI)
router.register(r'api/bookings', views.BookingAPI)
router.register(r'api/services', views.ServiceAPI)
router.register(r'api/payments', views.PaymentAPI)
router.register(r'api/booking_services', views.BookingServiceAPI)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),

    path('customers/add/', views.add_customer, name='add_customer'),
    path('customers/', views.list_customers, name='list_customers'),
    path('customers/get/', views.get_customer, name='get_customer'),
    path('customers/update/<int:id>/', views.update_customer, name='update_customer'),
    path('customers/delete/<int:id>/', views.delete_customer, name='delete_customer'),

    path('room_types/add/', views.add_room_type, name='add_room_type'),
    path('room_types/get', views.get_room_type, name='get_room_type'),
    path('room_types/', views.list_room_types, name='list_room_types'),

    path('add_service/', views.add_service, name='add_service'),
    path('list_services/', views.list_services, name='list_services'),
    path('get_service/', views.get_service, name='get_service'),
    path('update_service/<int:id>/', views.update_service, name='update_service'),
    path('delete_service/<int:id>/', views.delete_service, name='delete_service'),

    path('rooms/add/', views.add_room, name='add_room'),
    path('list_rooms/', views.list_rooms, name='list_rooms'),
    path('room/get/', views.get_room, name='get_room'),
    path('rooms/update/<int:id>', views.update_room, name='update_room'),

    path('api/bookings/add_booking/', views.BookingAPI.as_view({'post': "add_booking"})),
    path('add_booking/', views.add_booking, name='add_booking'),
    path('list_bookings/', views.list_bookings, name='list_bookings'),
    path('get_booking/', views.get_booking, name='get_booking'),
    path('delete_booking/<int:id>', views.delete_booking, name='delete_booking'),

    path('add_payment/', views.add_payment, name='add_payment'),
    path('get_payment/', views.get_payment, name='get_payment'),

    path('customer_bookings/', views.CustomerBookingsAPIView.as_view(), name='customer_bookings'),
    path('services_bookings/', views.BookingServicesAPIView.as_view(), name='service-bookings'),
    path('bookings_monthly/', views.MonthlyBookingsAPIView.as_view(), name='monthly-bookings'),
    path('rooms_income/', views.RoomIncomeAPIView.as_view(), name='room-income'),
    path('income_monthly/', views.MonthlyIncomeAPIView.as_view(), name='monthly-income'),
    path('customers_income/', views.CustomerIncomeAPIView.as_view(), name='customer-income'),
    path('booking_statistics/', views.BookingStatisticsAPIView.as_view(), name='booking-statistics'),

    path('dashboard_v1/', views_plotly.graphic, name='dashboard_v1'),
    path('dashboard_v2/', views_bokeh.graphic, name='dashboard_v2'),
]
