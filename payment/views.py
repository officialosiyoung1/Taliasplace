from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status, permission 
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from urllib3 import request 
from Users.models import CustomUser
from makeupProduct.models import makeupProduct 
from .models import Payment
from .serializers import PaymentSerializer


class InitiatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, MakeupProduct_id):
        user = request.user
        MakeupProduct_id = request.data.get('product_id')
        amount = request.data.get('amount')
        refrence = f"PAY-{user.id}-{MakeupProduct_id}-{amount}"
        callback_url = request.build_absolute_url('/payment/callback/')

        if not MakeupProduct_id or not amount:
            return Response({"error": "Product ID and amount are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        product = get_object_or_404(makeupProduct, id=MakeupProduct_id)

        payload = {
            'email': request.user.email,
            'amount': amount,
            'reference': reference,
            'callback_url': callback_url,
            'metadata': {
                'MakeupProduct.id': MakeupProduct.id,
                'MakeupProduct.name': MakeupProduct.name,

            },
        }

        



# Create your views here.
