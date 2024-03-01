from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from channels.layers import get_channel_layer

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.http import HttpRequest
from django.shortcuts import render
from django.db.models import Q

from apps.parking.models import Parking, ParkingType, ParkingSize
from apps.parking.forms import ParkingForm
from apps.parking.serializers import ParkingSerializer
from apps.parking.filters import ParkingFilter
from apps.parking.coordenates import Coordenates
from apps.parking.validators import ParkingValidator

from django.contrib.auth.decorators import login_required


channel_layer = get_channel_layer()

# Create your views here.
def index(request):
    return render(request, "parking/index.html")

def room(request, room_name):
    return render(request, "parking/room.html", {"room_name": room_name})

@api_view(['POST'])
@login_required
def get_parking_near(request: HttpRequest):
    filter = ParkingFilter.from_request(request)
    near = filter.get_queryset()
    serializer = ParkingSerializer(near, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@login_required
def create_parking(request: HttpRequest):
    data = request.POST.copy()
    coordenates = Coordenates.from_request(request)
    data["location"] = coordenates.get_point() 
    parking = Parking(
        location=data["location"],
        size=ParkingSize[data["size"]],
        parking_type=ParkingType[data["parking_type"]],
        is_transfer=False,
        is_asignment=False,
        notified_by=request.user       
    )
    if parking:
        errors = ParkingValidator(parking).validate()
        if len(errors) > 0:
            return Response({'error': errors}, status=status.HTTP_409_CONFLICT)
        parking = parking.save()
        return Response(ParkingSerializer(parking).data, status=status.HTTP_201_CREATED)
    return Response({'error': parking.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@login_required
def assign_parking(request: HttpRequest, room_name):
    return None

