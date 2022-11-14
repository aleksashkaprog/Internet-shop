from rest_framework.response import Response
from rest_framework.views import APIView

from payment.services import check_cart_number, get_exc_to_pay


class PaymentAPIView(APIView):
    """Метод обработки запросов фиктивной оплаты"""

    def get(self, request, card_number: int, cost: str):
        return_data = {
            'cost': cost
        }

        if not check_cart_number(card_number=card_number):
            return_data['error'] = get_exc_to_pay()
            return Response(return_data, status=400)

        return Response(return_data, status=201)