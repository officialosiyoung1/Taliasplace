from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status, permission 
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response 
from Users.models import CustomUser
from makeupProduct.models import makeupProduct 
from .models import Payment 
from .serializers import PaymentSerializer



# Create your views here.
