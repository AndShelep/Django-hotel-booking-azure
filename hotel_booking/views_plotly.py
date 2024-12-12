from datetime import date, datetime
from django.db.models import Count, Sum
from django.shortcuts import render
import plotly.express as px
import pandas as pd
from django.db.models.functions import TruncMonth

from hotel_booking.views import hotelBookingManager

def graphic(request):
    queryset1 = hotelBookingManager.customer_repository.get_all().annotate(
        total_bookings=Count('booking')
    ).values('customer_name', 'customer_surname', 'phone_number', 'total_bookings')
    df = pd.DataFrame(list(queryset1))
    df['customer_info'] = df['customer_name'] + " " + df['customer_surname'] + " (" + df['phone_number'] + ")"
    fig = px.bar(
        df,
        x='customer_info',
        y='total_bookings',
        title='Count bookings by customer',
        labels={
            'customer_info': 'Customer Info',
            'total_bookings': 'Total Bookings',
        }
    )

    graph1 = fig.to_html(full_html=False)

    queryset2 = hotelBookingManager.booking_service_repository.get_all().annotate(
        total_bookings=Count('booking')
    ).values('service__service_name', 'total_bookings')
    df = pd.DataFrame(list(queryset2))
    fig2 = px.pie(
        df,
        values='total_bookings',
        names='service__service_name',
        title='Booking services',
        labels={
            'service__service_name': 'Service',
            'total_bookings': 'Total Bookings',
        }
    )

    graph2 = fig2.to_html(full_html=False)

    start_month = int(request.GET.get('start_month', 11))
    start_year = int(request.GET.get('start_year', 2024))
    end_month = int(request.GET.get('end_month', 2))
    end_year = int(request.GET.get('end_year', 2025))
    start_date = date(start_year, start_month, 1)
    end_date = date(end_year, end_month, 30) if end_month != 2 else date(end_year, end_month, 29) if (
    end_year % 4 == 0 and (end_year % 100 != 0 or end_year % 400 == 0)) else date(end_year, end_month, 28)
    queryset3 = hotelBookingManager.booking_repository.get_all().filter(
        in_date__gte=start_date,
        in_date__lte=end_date
    ).annotate(
        month=TruncMonth('in_date')
    ).values('month').annotate(
        total_bookings=Count('id')
    ).order_by('month')

    df = pd.DataFrame(list(queryset3))

    all_months = pd.date_range(start=start_date, end=end_date, freq='MS').to_pydatetime().tolist()
    df['month'] = pd.to_datetime(df['month'])
    all_months = pd.date_range(start=start_date, end=end_date, freq='MS')
    df_all = pd.DataFrame({'month': all_months})
    df = df_all.merge(df, on='month', how='left').fillna({'total_bookings': 0})
    df['month_year'] = df['month'].dt.strftime('%Y-%m')
    df['total_bookings'] = df['total_bookings'].astype(int)

    fig3 = px.line(
        df,
        x='month_year',
        y='total_bookings',
        title='Number of bookings per month',
        labels={
            'month_year': 'Month-Year',
            'total_bookings': 'Number of Bookings',
        },
        markers=True
    )
    fig3.update_layout(
        xaxis=dict(
            type='category',
        )
    )

    graph3 = fig3.to_html(full_html=False)


    queryset4 = hotelBookingManager.booking_repository.get_all().values('room__room_number').annotate(
        total_income=Sum('total_price')
    )

    df = pd.DataFrame(list(queryset4))
    df['room__room_number'] = df['room__room_number'].astype(str)

    fig4 = px.bar(
        df,
        x='room__room_number',
        y='total_income',
        title='Income by Room',
        labels={
            'room__room_number': 'Room Number',
            'total_income': 'Total Income'
        }
    )

    fig4.update_layout(
        xaxis=dict(
            type='category',
        )
    )

    graph4 = fig4.to_html(full_html=False)


    queryset5 = hotelBookingManager.booking_repository.get_all().annotate(
        month=TruncMonth('in_date')
    ).values('month').annotate(
        total_income=Sum('total_price')
    ).order_by('month')

    df = pd.DataFrame(list(queryset5))
    df['month'] = pd.to_datetime(df['month']).dt.strftime('%Y-%m')
    print(df)
    fig5 = px.line(
        df,
        x='month',
        y='total_income',
        title='Monthly Income',
        labels={
            'month': 'Month',
            'total_income': 'Total Income'
        },
        markers=True
    )
    fig5.update_layout(
        xaxis=dict(
            type='category',
        )
    )

    graph5 = fig5.to_html(full_html=False)

    queryset6 = hotelBookingManager.booking_repository.get_all().values(
        'customer__customer_name', 'customer__customer_surname', 'customer__phone_number'
    ).annotate(
        total_income=Sum('total_price')
    ).order_by('-total_income')

    df = pd.DataFrame(list(queryset6))
    df['customer'] = df['customer__customer_name'] + ' ' + df['customer__customer_surname'] + ' ' + df['customer__phone_number']
    fig6 = px.bar(
        df,
        y='total_income',
        x='customer',
        title='Income by Customer',
        labels={
            'customer': 'Customer',
            'total_income': 'Total Income'
        }
    )

    graph6 = fig6.to_html(full_html=False)

    return render(request, 'dashboard/dashboard_v1.html', context={
        'graph1': graph1,
        'graph2': graph2,
        'graph3': graph3,
        'graph4': graph4,
        'graph5': graph5,
        'graph6': graph6,})