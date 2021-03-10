from django.urls import path, include
from .views import (create_api, delivery_details, delete_items_data, get_unique_delivery_key, get_unique_delivery_data,
                    place_order)
urlpatterns = [
    path('create_api/', create_api, name='create_api'),
    path('place_order/', place_order, name='place_order'),
    path('delivery_details/', delivery_details, name='delivery_details'),
    path('delete_items_data/', delete_items_data, name='delete_items_data'),
    path('get_unique_delivery_key/', get_unique_delivery_key, name='get_unique_delivery_key'),
    path('get_unique_delivery_data/<slug:unique_delivery_id>/', get_unique_delivery_data, name='get_unique_delivery_data'),
]