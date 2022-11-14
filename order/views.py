from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView, DetailView
import datetime
from .models import Order, OrderGood
from .forms import StepOneForm, StepTwoForm, StepThreeForm
from cart.models import ProductInCart


class OrderHistory(View):
    template_name = "order/historyorder.html"

    def get(self, request, *args, **kwargs):
        orders = Order.objects.all().filter(consumer=request.user)
        return render(request, self.template_name, {"orders": orders})


class OrderView(DetailView):
    template_name = "order/order.html"

    def get(self, request, *args, **kwargs):
        goods_in_order = Order.objects.get(pk=kwargs["order_pk"])
        return render(request, self.template_name, {"goods_in_order": goods_in_order})


class StepOne(View):
    template_name = "order/step_one.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = StepOneForm
            return render(request, self.template_name, {"form": form})
        else:
            return redirect("users:register")

    def post(self, request, *args, **kwargs):
        form = StepOneForm(request.POST)
        order = Order.objects.create(consumer=request.user, order_in=False)
        q = ProductInCart.objects.filter(user=request.user).select_related("shop_product__product")
        for good in q:
            OrderGood.objects.create(good_in_order=order, good_in_cart=good)
        if form.is_valid():
            order.first_second_names = form.cleaned_data["first_second_names"]
            order.email = form.cleaned_data["email"]
            order.phone = form.cleaned_data["phone"]
            order.save()
            return redirect("order-step-two")
        return render(request, self.template_name, {"form": form})


class StepTwo(View):
    template_name = "order/step_two.html"

    def get(self, request, *args, **kwargs):
        form = StepTwoForm
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = StepTwoForm(request.POST)
        order = Order.objects.filter(consumer=request.user, order_in=False).first()
        if form.is_valid():
            order.delivery = form.cleaned_data["delivery"]
            order.city = form.cleaned_data["city"]
            order.address = form.cleaned_data["address"]
            order.save()
            return redirect("order-step-three")
        return render(request, self.template_name, {"form": form})


class StepThree(TemplateView):
    template_name = "order/step_three.html"

    def get(self, request, *args, **kwargs):
        form = StepThreeForm
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = StepThreeForm(request.POST)
        order = Order.objects.filter(consumer=request.user, order_in=False).first()
        if form.is_valid():
            order.payment = form.cleaned_data["payment"]
            order.order_in = True
            order.ordered = datetime.datetime.today()
            order.save()
            return redirect("order-step-four")
        return render(request, self.template_name, {"form": form})


class StepFour(View):
    template_name = "order/step_four.html"

    def get(self, request, *args, **kwargs):
        order = Order.objects.filter(consumer=request.user, order_in=True).first()
        return render(request, self.template_name, {"order": order})


class PaymentView(View):
    template_name = "payment/payment.html"

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(consumer=request.user, pk=kwargs["order_pk"])
        return render(request, self.template_name, {"order": order})


class PaymentProcess(View):
    template_name = "payment/payment_process.html"

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs["order_pk"])
        return render(request, self.template_name, {"order": order})
