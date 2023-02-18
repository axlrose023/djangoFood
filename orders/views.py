from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from marketplace.context_processors import get_cart_amount
from marketplace.models import Cart
from orders.forms import OrderForm
from orders.models import Order, Payment, OrderedFood
import simplejson as json

from orders.utils import generate_order_number
from accounts.utils import send_notification


@login_required(login_url='login')
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    subtotal = get_cart_amount(request)['subtotal']
    total_tax = get_cart_amount(request)['tax']
    grand_total = get_cart_amount(request)['grand_total']
    tax_data = get_cart_amount(request)['tax_dict']
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.total = grand_total
            order.tax_data = json.dumps(tax_data)
            order.total_tax = total_tax
            order.payment_method = request.POST.get('payment_method')
            order.user = request.user
            order.save()
            order.order_number = generate_order_number(order.id)
            order.save()
            context = {
                'order': order,
                'cart_items': cart_items,
            }
            return render(request, 'orders/place_order.html', context)
        else:
            print(form.errors)
    return render(request, 'orders/place_order.html')


@login_required(login_url='login')
def payments(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        order_number = request.POST.get('order_number')
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')

        order = Order.objects.get(user=request.user, order_number=order_number)
        payment = Payment(
            user=request.user,
            transaction_id=transaction_id,
            payment_method=payment_method,
            amount=order.total,
            status=status
        )
        payment.save()
        order.payment = payment
        order.is_ordered = True
        order.save()

        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            ordered_food = OrderedFood()
            ordered_food.order = order
            ordered_food.payment = payment
            ordered_food.user = request.user
            ordered_food.fooditem = item.fooditem
            ordered_food.quantity = item.quantity
            ordered_food.price = item.fooditem.price
            ordered_food.amount = item.fooditem * item.quantity
            ordered_food.save()

        mail_subject = 'Thank you for ordering with us.'
        mail_template = 'orders/order_confirmation_email.html'
        context = {
            'user': request.user,
            'order': order
        }
        send_notification(mail_subject, mail_template, context)
        mail_subject = 'You have received a new order.'
        mail_template = 'orders/new_order_received.html'
        to_emails = []
        for i in cart_items:
            if i.fooditem.vendor.user.email not in to_emails:
                to_emails.append(i.fooditem.vendor.user.email)
        context = {'order': order, 'to_email': to_emails}
        send_notification(mail_subject, mail_template, context)
        cart_items.delete()
        response = {
            'order_number': order_number,
            'transaction_id': transaction_id,
        }
        return JsonResponse(response)
    return HttpResponse("Payments View")


def order_complete(request):
    order_number = request.GET.get("order_no")
    transaction_id = request.GET.get("trans_id")
    print(order_number, transaction_id)
    try:
        order = Order.objects.get(order_number=order_number, payment__transaction_id=transaction_id, is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order)
        context = {
            'order': order,
            'order_food': ordered_food,
        }
        return render(request, 'orders/order_complete.html', context)
    except:
        return redirect('home')
