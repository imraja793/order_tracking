from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from math import sin, cos, sqrt, atan2, radians
import time
import random
import datetime


# Create your views here.
from django.views.generic import ListView

from delivery.models import UserProfile, ProductTable, DelDetails


def create_api(request):
    user = User.objects.create_user(
        username="delivery_guy",
        email='deliveryguy@email.com',
        password='testpass123'
    )
    UserProfile.objects.create(user_id=user.id, lat_long='22.527053,88.326099')
    ProductTable.objects.create(item='item1')
    return HttpResponse("done")


def calculate_distance(latitude1, longitude1, latitude2, longitude2):

    # approximate radius of earth in km
    R = 6373.0
    lat1 = radians(latitude1)
    lon1 = radians(longitude1)
    lat2 = radians(latitude2)
    lon2 = radians(longitude2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return(str(distance)[:5])


def delivery_details(request):
    unique_delivery_id = random.randint(1, 9999999999)
    address_dict = {
                    "Khidderpore": [22.5372, 88.3231],
                    "Taratala": [22.514090, 88.322090],
                    "NewAlipore": [22.5105326, 88.3354264],
                    "AjantaCinema": [22.5081116, 88.3202281],
                    "Majerhat": [22.5187, 88.3224]
                    }
    delivery_date = datetime.datetime.now() + datetime.timedelta(days=1)
    initial_latitude = 22.527053
    initial_longitude = 88.326099
    rounds = 1
    delivery_delayed_item = False
    delivery_delay_reason = "no delay"
    message = ""
    initially_mins = 0
    previous_position = 'central'
    for address, lat_long in address_dict.items():
        next_lat = lat_long[0]
        next_long = lat_long[1]
        distance_travelled = calculate_distance(initial_latitude, initial_longitude, next_lat, next_long)
        time_taken = float(distance_travelled)/40
        mins_taken = (time_taken * 60) + 5
        initially_mins = mins_taken + initially_mins
        if initially_mins > 30:
            delivery_delay_reason = 'delayed delivery on the way'
            delivery_delayed_item = True
        message = message + (
            f"on {delivery_date} order placed at {datetime.datetime.now()} Delivery guy  having max order of "
            f"5 going for round {rounds} started from the position'{previous_position} \n "
            f" [{initial_latitude, initial_longitude}] travelling towards destination {address}[{next_lat, next_long}]'"
            f"time taken by him for travelling {distance_travelled} km in {mins_taken} mins {delivery_delay_reason}\n\n"
        )

        DelDetails.objects.create(lat_long_initial=[initial_latitude, initial_longitude],
                                  destination_lat_long=[next_lat, next_long],
                                  address=address,
                                  itemdetails_id=ProductTable.objects.first().id,
                                  time_spent=mins_taken,
                                  assigned_delivery_guy_id=UserProfile.objects.first().id,
                                  delivery_delayed=delivery_delayed_item,
                                  delivery_number=rounds,
                                  distance_travelled=distance_travelled,
                                  delivery_details=delivery_delay_reason,
                                  unique_delivery_id=unique_delivery_id,
                                  previous_address=previous_position,
                                  delivery_date=delivery_date,
                                  )
        initial_latitude = next_lat
        initial_longitude = next_long
        rounds += 1
        previous_position = address

    with open('output_file.txt', 'w') as newfile:
        newfile.write(message)
    return HttpResponse(str(message))


def delete_items_data(request):
    ProductTable.objects.all().delete()
    UserProfile.objects.all().delete()
    User.objects.filter(username='delivery_guy').delete()
    return HttpResponse("deleted")


def get_unique_delivery_key(request):

    obj = DelDetails.objects.distinct("unique_delivery_id").values_list("unique_delivery_id", flat=True)
    url_list = []
    for ids in obj:
        url_list.append(f'localhost:8000/get_unique_delivery_data/{ids} , ')

    return HttpResponse(url_list)


def get_unique_delivery_data(request, unique_delivery_id):
    try:
        obj = DelDetails.objects.filter(unique_delivery_id=unique_delivery_id).order_by("delivery_number")
        message = ""
        for data in obj:
            message = message + f"Delivery guy having max order of 5 going for round {data.delivery_number} started from " \
                                f"the position'[{data.lat_long_initial}] travelling towards destination " \
                                f"[{data.address}{data.destination_lat_long}]'time taken by him for travelling " \
                                f"{data.distance_travelled} km in {data.time_spent} mins with {data.delivery_details}\n\n "
        with open('unique_delivery_file.txt', 'w') as newfile:
            newfile.write(message)
        return HttpResponse("Kindly check unique_delivery_file.txt for the output")

    except:
        return HttpResponse("id not found kindly localhost:8000/get_unique_delivery_key hit this url to get the"
                            " desired url for checking")


def place_order(request):
    try:
        create_api(request)
    except:
        pass
    delivery_details(request)
    return HttpResponse('Done kindly check output_file.txt all the output has been saved there')
