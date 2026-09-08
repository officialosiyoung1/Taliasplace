from rest_framework import generics
from .models import Booking
from .serializers import BookingSerializer
from rest_framework.response import Response

class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class CreateBookingView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        print("Request data:", request.data)  # Debugging line to print the incoming request data
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
