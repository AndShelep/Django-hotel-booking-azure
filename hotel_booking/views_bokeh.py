import decimal
from datetime import date

from bokeh.palettes import Category20c, Category20b
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import ColumnDataSource
import pandas as pd
from bokeh.transform import cumsum
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render

from hotel_booking.views import hotelBookingManager

def convert_decimal_to_float(data, fields):
    for row in data:
        for field in fields:
            if isinstance(row.get(field), decimal.Decimal):
                row[field] = float(row[field])
    return data

def graphic(request):
    queryset1 = hotelBookingManager.customer_repository.get_all().annotate(
        total_bookings=Count('booking')
    ).values('customer_name', 'customer_surname', 'phone_number', 'total_bookings')

    df = pd.DataFrame(list(queryset1))
    df['customer_info'] = df['customer_name'] + " " + df['customer_surname'] + " (" + df['phone_number'] + ")"

    source = ColumnDataSource(df)

    p = figure(
        x_range=df['customer_info'],
        title="Count bookings by customer",
        toolbar_location=None,
        tools=""
    )

    p.vbar(
        x='customer_info',
        top='total_bookings',
        width=0.9,
        source=source,
        legend_field="customer_info"
    )

    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.xaxis.axis_label = "Customer Info"
    p.yaxis.axis_label = "Total Bookings"
    p.xaxis.major_label_orientation = 1

    script1, div1 = components(p)

    queryset2 = hotelBookingManager.booking_service_repository.get_all().values('service__service_name') \
        .annotate(total_bookings=Count('booking'))

    df = pd.DataFrame(list(queryset2))
    df['total_bookings'] = df['total_bookings'].astype(int)
    total = df['total_bookings'].sum()
    df['angle'] = df['total_bookings'] / total * 2 * 3.14159
    colors = [
        '#f4a261', '#2a9d8f', '#e76f51', '#264653', '#e9c46a',
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
        '#f39c12', '#e74c3c', '#9b59b6', '#3498db', '#2ecc71'
    ]
    df['color'] = colors[:len(df)]
    source = ColumnDataSource(df)

    p2 = figure(
        title="Booking Services",
        toolbar_location=None,
        tools="",
        x_range=(-1, 1),
        y_range=(-1, 1)
    )

    p2.wedge(
        x=0, y=0, radius=0.4,
        start_angle=cumsum('angle', include_zero=True),
        end_angle=cumsum('angle'),
        line_color="white",
        fill_color='color',
        legend_field='service__service_name',
        source=source
    )
    p2.legend.title = "Services"
    script2, div2 = components(p2)


    start_date = date(2024, 11, 1)
    end_date = date(2025, 2, 28)
    queryset3 = hotelBookingManager.booking_repository.get_all().filter(
        in_date__gte=start_date,
        in_date__lte=end_date
    ).annotate(
        month=TruncMonth('in_date')
    ).values('month').annotate(
        total_bookings=Count('id')
    ).order_by('month')

    df = pd.DataFrame(list(queryset3))
    df['month'] = pd.to_datetime(df['month']).dt.strftime('%Y-%m')

    source = ColumnDataSource(df)

    p3 = figure(
        x_range=df['month'],
        title="Number of bookings from November 2024 to February 2025",
        toolbar_location=None,
        tools=""
    )
    p3.line(x='month', y='total_bookings', source=source, line_width=2)
    p3.circle(x='month', y='total_bookings', source=source, size=8)
    p3.xaxis.axis_label = "Month-Year"
    p3.yaxis.axis_label = "Total Bookings"

    script3, div3 = components(p3)

    queryset4 = hotelBookingManager.booking_repository.get_all().values('room__room_number').annotate(
        total_income=Sum('total_price')
    )

    data = convert_decimal_to_float(list(queryset4), ['total_income'])
    df = pd.DataFrame(data)
    df['room__room_number'] = df['room__room_number'].astype(str)

    source = ColumnDataSource(df)

    p4 = figure(
        x_range=df['room__room_number'],
        title="Income by Room",
        toolbar_location=None,
        tools=""
    )
    p4.vbar(x='room__room_number', top='total_income', width=0.9, source=source)
    p4.xaxis.axis_label = "Room Number"
    p4.yaxis.axis_label = "Total Income"

    script4, div4 = components(p4)

    queryset5 = hotelBookingManager.booking_repository.get_all().annotate(
        month=TruncMonth('in_date')
    ).values('month').annotate(
        total_income=Sum('total_price')
    ).order_by('month')

    data = convert_decimal_to_float(list(queryset5), ['total_income'])
    df = pd.DataFrame(list(data))
    df['month'] = pd.to_datetime(df['month']).dt.strftime('%Y-%m')

    source = ColumnDataSource(df)

    p5 = figure(
        x_range=df['month'],
        title="Monthly Income",
        toolbar_location=None,
        tools=""
    )
    p5.line(x='month', y='total_income', source=source, line_width=2)
    p5.circle(x='month', y='total_income', source=source, size=8)
    p5.xaxis.axis_label = "Month"
    p5.yaxis.axis_label = "Total Income"

    script5, div5 = components(p5)

    queryset6 = hotelBookingManager.booking_repository.get_all().values(
        'customer__customer_name', 'customer__customer_surname', 'customer__phone_number'
    ).annotate(
        total_income=Sum('total_price')
    ).order_by('-total_income')

    data = convert_decimal_to_float(list(queryset6), ['total_income'])
    df = pd.DataFrame(data)
    df['customer'] = df['customer__customer_name'] + ' ' + df['customer__customer_surname'] + ' ' + df[
        'customer__phone_number']

    source = ColumnDataSource(df)

    p6 = figure(
        y_range=df['customer'],
        title="Income by Customer",
        toolbar_location=None,
        tools=""
    )
    p6.hbar(y='customer', right='total_income', height=0.9, source=source)
    p6.xaxis.axis_label = "Total Income"
    p6.yaxis.axis_label = "Customer"

    script6, div6 = components(p6)

    return render(request, 'dashboard/dashboard_v2.html', context={
        'script1': script1, 'div1': div1,
        'script2': script2, 'div2': div2,
        'script3': script3, 'div3': div3,
        'script4': script4, 'div4': div4,
        'script5': script5, 'div5': div5,
        'script6': script6, 'div6': div6,
    })