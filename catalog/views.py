from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
# Create your views here.
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from .models import (
    Item, OrderItem, Order,Brand,ProductReview,Bills,BillsDetail)
from .forms import CheckoutForm,ReviewForm
class HomeView(ListView):


    def get(self, *args, **kwargs):
        brand = Brand.objects.all()[0:5]
        item=Item.objects.all()[0:]
        shirts = Item.objects.filter(status='N')
        context = {
            'brands': brand,
            'products':item,
            'shirts': shirts,
            # 'new_products': new_products
        }
        return render(self.request, 'index.html', context)

def ProductDetail(request, slug):
    items = get_object_or_404(Item, slug=slug)
    review=ProductReview.objects.filter(item=items.id)
    context={
        'object':items,
        'items': Item.objects.all().order_by('id')[0:3],
        'review':review
    }

    return render(request,'product.html',context)


def addProductReview(request, slug):
    items = get_object_or_404(Item, slug=slug)
    review=ProductReview.objects.filter(item=items.id)
    form = ReviewForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            name=form.cleaned_data.get('name')
            message=form.cleaned_data.get('message')
            email=form.cleaned_data.get('email')
            ratting=form.cleaned_data.get('ratting')
        productReview=ProductReview(item=items,email=email,name=name,message=message,ratting=ratting)
        productReview.save()
        form = ReviewForm()
    context={
        'object':items,
        'items': Item.objects.all().order_by('id')[0:3],
        'review':review
    }
    return HttpResponseRedirect(reverse('add_productReview_success', args=(slug,)))

def home(request):
    return render(request,'index.html')


def checkout(request):
    return render(request,'checkout.html')


def product(request):
    return render(request,'product.html')


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context={
                'form':form,
                'order': order,
            }
            return render(self.request,'checkout.html',context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You don't have an active order")
            return redirect('order_summary')
    def post(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm(self.request.POST or None)
            if form.is_valid():
                address = form.cleaned_data.get('address')
                name=form.cleaned_data.get('name')
                phone=form.cleaned_data.get('phone')
                email=form.cleaned_data.get('email')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                bill=Bills(
                    user=self.request.user,
                    address=address,
                    name=name,
                    phone=phone,
                    email=email,
                    country=country,
                    zip=zip,
                    total=order.get_total(),
                    quantity=order.get_quantity(),
                    checkout_date=datetime.now()
                )

                bill.save()
                for order_item in order.items.all() :
                    item = get_object_or_404(Item, pk=order_item.item.id)
                    billDetail = BillsDetail(
                        user=self.request.user,
                        bill=bill,
                        item=item,
                        quantity=order_item.quantity,
                        total=order_item.get_item_final_price(),
                    )
                    billDetail.save()
                order.ordered = True
                order.save()
                order.delete()


                # order_item = OrderItem.getALl()
                # order_item.delete()
                # try :
                #     order_item=OrderItem.objects.get(user=self.request.user, ordered=False)
                #     order_item.item.ordered=True
                #     order_item.item.delete()
                #     order_item.save()
                #     return redirect('checkout_success')
                # except :
                #     return redirect('checkout_success')
                return redirect('checkout_success')
            else :
                return redirect('checkout')
        except ObjectDoesNotExist:
            return redirect('checkout')


def checkout_success(request):
    return render(request,'checkout_success.html')


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, f"{item}'s quantity was updated")
            return redirect('order_summary')
        else:
            order.items.add(order_item)
            messages.success(request, f"{item} was added to your cart")
            return redirect('product',slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered=False , ordered_date=ordered_date)
        order.items.add(order_item)
        messages.success(request, f"{item} was added to your cart")
        return redirect('product',slug=slug)


@login_required
def remove_single_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order_item.delete()
                order.save()
            messages.success(request, f"{item}'s quantity was updated!")
            return redirect('order_summary')

        else:
            messages.success(request, f"{item} was not in your cart")
            return redirect('detail', slug=slug)
    else:
        messages.success(request, "You do not have an active order")
        return redirect('detail', slug=slug)

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False)[0]

            order.items.remove(order_item)
            order_item.delete()
            messages.success(request, f"{item} was removed from your cart!")
            return redirect('order_summary')

        else:
            messages.success(request, f"{item} was not in your cart")
            return redirect('order_summary')
    else:
        messages.success(request, "You do not have an active order")
        return redirect('order_summary')


class OrderSummaryView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context={
                'order':order
            }
            return render(self.request,'order_summary.html',context)
        except ObjectDoesNotExist:
            # order=None
            return render(self.request,'order_summary.html')
            # return False


# class login_user(View):
#     def get(self, *args, **kwargs):
#         context={
#         }
#         return render(self.request,'account/login.html',context)




def Brand_search(request,name):
    brand=Brand.objects.get(name=name)
    item = Item.objects.filter(brand=brand.id)
    context = {

        'products':item,

    }
    return render(request,'Brand.html',context)